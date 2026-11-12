from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pathlib import Path
from dotenv import load_dotenv
import requests
import os
import time

# .env 파일 불러오기
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()

# static 폴더 연결
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# GDELT 요청 제한 관리
LAST_GDELT_REQUEST_TIME = 0
GDELT_MIN_INTERVAL = 60  # 최소 30초 간격 권장

# 간단 캐시
CACHE = {}
CACHE_TTL = 300  # 5분 캐시


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


def build_gdelt_datetime(date: str):
    """
    입력: 2025-01-02
    출력: 20250102000000, 20250102235959
    """
    clean_date = date.replace("-", "")
    start = clean_date + "000000"
    end = clean_date + "235959"
    return start, end


def fetch_gdelt_news(date: str, keyword: str):
    global LAST_GDELT_REQUEST_TIME

    now = time.time()
    elapsed = now - LAST_GDELT_REQUEST_TIME

    if elapsed < GDELT_MIN_INTERVAL:
        wait_time = int(GDELT_MIN_INTERVAL - elapsed)
        raise RuntimeError(f"GDELT 요청 제한 방지를 위해 {wait_time}초 뒤 다시 시도하세요.")

    start_datetime, end_datetime = build_gdelt_datetime(date)

    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": keyword,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": 10,
        "sort": "HybridRel",
        "startdatetime": start_datetime,
        "enddatetime": end_datetime,
    }

    headers = {
        "User-Agent": "daily-hot-news-ai/1.0"
    }

    LAST_GDELT_REQUEST_TIME = time.time()

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=20
    )

    if response.status_code == 429:
        raise RuntimeError("GDELT 요청 제한에 걸렸습니다. 5분 정도 기다린 뒤 다시 시도하세요.")

    if response.status_code != 200:
        raise RuntimeError(f"GDELT API 오류: status code {response.status_code}")

    data = response.json()
    raw_articles = data.get("articles", [])

    articles = []

    for item in raw_articles[:10]:
        articles.append({
            "title": item.get("title", "제목 없음"),
            "url": item.get("url", ""),
            "domain": item.get("domain", ""),
            "date": item.get("seendate", ""),
            "language": item.get("language", ""),
            "source_country": item.get("sourcecountry", ""),
            "image": item.get("socialimage", ""),
        })

    return articles

def make_summary(keyword: str, articles: list):
    if not articles:
        return "뉴스 데이터를 가져오지 못했습니다."

    api_key = os.getenv("OPENAI_API_KEY")

    # API 키가 없으면 기본 요약 사용
    if not api_key:
        titles = [article["title"] for article in articles[:3]]
        return (
            f"'{keyword}' 관련 뉴스 {len(articles)}개를 찾았습니다.\n"
            f"주요 기사 예시:\n- " + "\n- ".join(titles)
        )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        titles_text = "\n".join(
            [f"- {article['title']}" for article in articles[:10]]
        )

        prompt = f"""
다음은 '{keyword}' 키워드로 수집한 뉴스 제목들입니다.

{titles_text}

이 뉴스들의 공통 흐름을 한국어로 3문장 이내로 요약해 주세요.
과장하지 말고, 제목에서 확인 가능한 내용만 요약해 주세요.
"""

        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 뉴스 큐레이션 도우미입니다."},
                {"role": "user", "content": prompt},
            ],
        )

        return result.choices[0].message.content

    except Exception as e:
        return f"AI 요약 중 오류가 발생했습니다. 기본 뉴스 목록을 확인하세요. 상세: {str(e)}"


@app.get("/api/news")
def get_news(
    date: str = Query(..., description="예: 2025-01-02"),
    keyword: str = Query(..., description="예: AI")
):
    cache_key = f"{date}:{keyword.lower()}"

    now = time.time()

    # 캐시 확인
    if cache_key in CACHE:
        cached = CACHE[cache_key]
        if now - cached["time"] < CACHE_TTL:
            result = cached["data"]
            result["from_cache"] = True
            return result

    try:
        articles = fetch_gdelt_news(date, keyword)
        summary = make_summary(keyword, articles)

        result = {
            "date": date,
            "keyword": keyword,
            "count": len(articles),
            "summary": summary,
            "articles": articles,
            "from_cache": False,
            "error": False,
        }

        CACHE[cache_key] = {
            "time": time.time(),
            "data": result,
        }

        return result

    except Exception as e:
        return {
            "date": date,
            "keyword": keyword,
            "count": 0,
            "summary": (
                "뉴스 데이터를 가져오지 못했습니다.\n\n"
                "가능한 원인:\n"
                "1. GDELT API 요청 제한\n"
                "2. GDELT 서버 일시적 불안정\n"
                "3. 너무 잦은 검색 요청\n\n"
                f"상세 오류: {str(e)}"
            ),
            "articles": [],
            "from_cache": False,
            "error": True,
        }