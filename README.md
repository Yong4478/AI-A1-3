# AI-A1-3
# 날짜별 인기뉴스 AI 큐레이션 웹서비스 개발 진행 보고서

https://daily-hot-news-ai.vercel.app/

## 1. 프로젝트 개요

본 프로젝트는 사용자가 **날짜와 키워드**를 입력하면 해당 조건에 맞는 뉴스를 수집하고, 수집된 기사 내용을 바탕으로 **AI가 핵심 내용을 요약**해주는 웹서비스를 개발하는 것을 목표로 한다.

서비스의 핵심 기능은 다음과 같다.

- 날짜 기반 뉴스 검색
- 키워드 기반 뉴스 필터링
- 외부 뉴스 API 연동
- AI 요약 생성
- 웹 브라우저 기반 사용자 인터페이스 제공
- 백엔드와 프론트엔드 간 API 통신

---

## 2. 개발 목표

### 2.1 사용자 관점 목표

사용자는 웹페이지에서 다음 정보를 입력한다.

- 날짜
- 검색 키워드

이후 `뉴스 검색` 버튼을 클릭하면 다음 결과를 확인할 수 있어야 한다.

- 관련 뉴스 목록
- 각 뉴스의 제목, 설명, 링크
- AI가 생성한 요약문

### 2.2 기술적 목표

본 프로젝트의 기술적 목표는 다음과 같다.

- FastAPI 기반 백엔드 서버 구축
- HTML, CSS, JavaScript 분리 구조 적용
- 외부 뉴스 API와 연동
- OpenAI API를 활용한 뉴스 요약 처리
- 프론트엔드에서 비동기 API 요청 처리
- 에러 상황에 대한 사용자 안내 및 서버 로그 확인 가능 구조 구현

---

## 3. 사용 기술 스택

| 구분 | 기술 |
|---|---|
| 백엔드 | FastAPI |
| 프론트엔드 | HTML, CSS, JavaScript |
| 서버 실행 | Uvicorn |
| 뉴스 데이터 | GDELT News API |
| AI 요약 | OpenAI API |
| 환경 변수 관리 | `.env` |
| 정적 파일 제공 | FastAPI StaticFiles |

---

## 4. 프로젝트 구조

현재 프로젝트는 다음과 같은 형태로 구성되었다.

```text
project/
├─ app/
│  └─ main.py
├─ static/
│  ├─ css/
│  │  └─ style.css
│  └─ js/
│     └─ main.js
├─ templates/
│  └─ index.html
├─ .env
└─ requirements.txt
```

각 파일의 역할은 다음과 같다.

| 파일 또는 폴더 | 역할 |
|---|---|
| `app/main.py` | FastAPI 서버 실행, 라우팅, API 처리 |
| `templates/index.html` | 메인 웹페이지 화면 구성 |
| `static/css/style.css` | 웹페이지 디자인 |
| `static/js/main.js` | 버튼 클릭 이벤트 및 API 요청 처리 |
| `.env` | OpenAI API 키 등 민감 정보 관리 |
| `requirements.txt` | 필요한 Python 패키지 목록 |

---

## 5. 현재까지 완료된 작업

### 5.1 FastAPI 백엔드 구축

FastAPI를 활용하여 웹서버를 구성하였다.

구현된 주요 기능은 다음과 같다.

- 메인 페이지 렌더링
- 정적 파일 제공
- 뉴스 검색 API 엔드포인트 구성
- favicon 요청 처리
- 외부 뉴스 API 요청 처리
- OpenAI API 연동을 위한 환경 변수 설정

브라우저에서 메인 페이지 접근 시 서버가 정상적으로 응답하는 것을 확인하였다.

예시 로그:

```text
GET / HTTP/1.1 200 OK
```

---

### 5.2 프론트엔드 화면 구현

사용자 입력 화면을 구성하였다.

현재 화면에는 다음 요소가 포함되어 있다.

- 서비스 제목
- 설명 문구
- 날짜 입력창
- 키워드 입력창
- 뉴스 검색 버튼
- AI 요약 영역
- 뉴스 목록 영역

화면 구성은 정상적으로 브라우저에 표시되고 있다.

---

### 5.3 HTML, CSS, JavaScript 분리

초기 구조에서 기능별 파일을 분리하였다.

- HTML: 화면 구조 담당
- CSS: 스타일 담당
- JavaScript: 사용자 이벤트 및 서버 통신 담당

이를 통해 유지보수성과 확장성을 높였다.

---

### 5.4 OpenAI API 키 환경 변수 관리

OpenAI API 키를 코드에 직접 작성하지 않고 `.env` 파일을 통해 관리하도록 설정하였다.

이는 보안상 적절한 방식이며, API 키 노출 위험을 줄일 수 있다.

---

### 5.5 GDELT 뉴스 API 연동

뉴스 데이터를 가져오기 위해 GDELT API 연동을 진행하였다.

다만 GDELT API는 무료로 사용할 수 있다는 장점이 있으나, 요청 제한이 강하게 적용되는 문제가 확인되었다.

이에 따라 다음과 같은 보완 로직이 논의되었다.

- 요청 간격 제한
- 캐싱 처리
- 에러 핸들링
- 대체 뉴스 API 검토

---

## 6. 발생한 주요 문제와 해결 과정

## 6.1 터미널 위치 문제

### 문제

명령어 실행 시 프로젝트 경로가 맞지 않아 서버 실행 또는 파일 접근이 정상적으로 되지 않는 문제가 있었다.

### 해결

터미널에서 현재 위치를 확인하고, 프로젝트 루트 디렉터리로 이동한 후 명령어를 실행하도록 정리하였다.

---

## 6.2 favicon 요청 로그

### 발생 로그

```text
INFO: 127.0.0.1:57714 - "GET /favicon.ico HTTP/1.1" 204 No Content
```

### 원인

브라우저는 웹페이지 접속 시 자동으로 `/favicon.ico` 파일을 요청한다.

해당 프로젝트에서는 별도의 favicon 파일을 제공하지 않았기 때문에 서버가 `204 No Content`를 반환하였다.

### 판단

이 로그는 오류가 아니며, 서비스 동작에는 문제가 없다.

`204 No Content`는 다음 의미이다.

```text
요청은 정상적으로 처리했지만, 반환할 콘텐츠는 없다.
```

따라서 검색 버튼 미작동 문제와는 관련이 없는 정상 로그로 판단하였다.

---

## 6.3 검색 버튼 미작동 문제

### 문제

메인 페이지는 정상적으로 표시되었으나, 사용자가 파란색 `뉴스 검색` 버튼을 클릭해도 아무 동작이 발생하지 않았다.

### 확인 내용

버튼 클릭 시 서버 터미널에 다음과 같은 API 요청 로그가 나타나야 한다.

```text
GET /api/news?date=2025-01-02&keyword=AI HTTP/1.1
```

그러나 버튼 클릭 후 `/api/news` 요청 로그가 나타나지 않는다면, 이는 백엔드 문제가 아니라 프론트엔드 이벤트 연결 문제일 가능성이 높다.

### 원인

HTML 코드에 JavaScript가 찾는 버튼 ID인 `searchButton`이 존재하지 않았다.

JavaScript에서는 다음 코드로 버튼을 찾도록 작성되어 있었다.

```javascript
const searchButton = document.getElementById("searchButton");
```

하지만 HTML 버튼에 다음 속성이 없었기 때문에 클릭 이벤트가 연결되지 않았다.

```html
id="searchButton"
```

### 해결 방향

HTML의 버튼 태그에 `id="searchButton"`을 추가하고, JavaScript에서 클릭 이벤트를 등록하도록 수정해야 한다.

---

## 7. 수정이 필요한 핵심 코드

## 7.1 `index.html`의 검색 영역

검색 버튼에는 반드시 `id="searchButton"`이 포함되어야 한다.

```html
<div class="search-area">
  <input
    type="date"
    id="dateInput"
    value="2025-01-02"
  />

  <input
    type="text"
    id="keywordInput"
    value="AI"
    placeholder="키워드를 입력하세요"
  />

  <button id="searchButton" type="button">
    뉴스 검색
  </button>
</div>
```

또한 AI 요약과 뉴스 목록을 표시할 영역도 JavaScript에서 접근할 수 있도록 ID를 지정해야 한다.

```html
<section class="summary-section">
  <h2>AI 요약</h2>
  <div id="summaryBox">
    아직 검색하지 않았습니다.
  </div>
</section>

<section class="news-section">
  <h2>뉴스 목록</h2>
  <div id="newsList"></div>
</section>
```

그리고 HTML 문서의 `body` 하단에 JavaScript 파일을 연결해야 한다.

```html
<script src="/static/js/main.js"></script>
```

---

## 7.2 `main.js`의 버튼 이벤트 처리

JavaScript에서는 페이지 로딩이 끝난 후 버튼을 찾아 클릭 이벤트를 등록해야 한다.

```javascript
document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("searchButton");
  const dateInput = document.getElementById("dateInput");
  const keywordInput = document.getElementById("keywordInput");
  const summaryBox = document.getElementById("summaryBox");
  const newsList = document.getElementById("newsList");

  console.log("main.js 로드됨");

  if (!searchButton) {
    console.error("searchButton을 찾을 수 없습니다.");
    return;
  }

  searchButton.addEventListener("click", async () => {
    console.log("뉴스 검색 버튼 클릭됨");

    const date = dateInput.value;
    const keyword = keywordInput.value.trim();

    if (!date || !keyword) {
      alert("날짜와 키워드를 모두 입력해주세요.");
      return;
    }

    summaryBox.innerHTML = "뉴스를 검색하고 AI 요약을 생성하는 중입니다...";
    newsList.innerHTML = "";

    searchButton.disabled = true;
    searchButton.textContent = "검색 중...";

    try {
      const url = `/api/news?date=${encodeURIComponent(date)}&keyword=${encodeURIComponent(keyword)}`;
      const response = await fetch(url);
      const data = await response.json();

      console.log("API 응답:", data);

      if (!response.ok) {
        summaryBox.innerHTML = "서버에서 오류가 발생했습니다.";
        return;
      }

      summaryBox.innerHTML = data.summary || "요약 결과가 없습니다.";

      const articles = data.articles || data.news || [];

      if (articles.length === 0) {
        newsList.innerHTML = "<p>검색된 뉴스가 없습니다.</p>";
        return;
      }

      articles.forEach((article) => {
        const item = document.createElement("div");
        item.className = "news-item";

        const title = article.title || "제목 없음";
        const description = article.description || article.summary || "";
        const link = article.url || article.link || "#";

        item.innerHTML = `
          <h3>${title}</h3>
          <p>${description}</p>
          <a href="${link}" target="_blank" rel="noopener noreferrer">
            기사 보기
          </a>
        `;

        newsList.appendChild(item);
      });
    } catch (error) {
      console.error("요청 실패:", error);
      summaryBox.innerHTML = "서버 요청 중 오류가 발생했습니다.";
    } finally {
      searchButton.disabled = false;
      searchButton.textContent = "뉴스 검색";
    }
  });
});
```

---

## 8. 디버깅 방법

현재 단계에서 가장 중요한 확인 방법은 브라우저 개발자 도구와 서버 터미널 로그를 함께 확인하는 것이다.

### 8.1 브라우저 Console 확인

브라우저에서 `F12`를 누른 뒤 `Console` 탭을 확인한다.

페이지 새로고침 시 다음 로그가 출력되어야 한다.

```text
main.js 로드됨
```

버튼 클릭 시 다음 로그가 출력되어야 한다.

```text
뉴스 검색 버튼 클릭됨
```

만약 `main.js 로드됨`이 출력되지 않는다면 JavaScript 파일 연결이 잘못된 것이다.

---

### 8.2 서버 터미널 확인

버튼 클릭 후 서버 터미널에는 다음과 같은 요청 로그가 출력되어야 한다.

```text
GET /api/news?date=2025-01-02&keyword=AI HTTP/1.1
```

이 로그가 출력된다면 프론트엔드에서 백엔드로 요청이 정상 전달되고 있다는 의미이다.

반대로 이 로그가 없다면 버튼 클릭 이벤트 또는 JavaScript 연결에 문제가 있는 것이다.

---

### 8.3 강력 새로고침

JavaScript 파일 수정 후에는 브라우저 캐시 때문에 변경사항이 바로 반영되지 않을 수 있다.

따라서 수정 후 다음 단축키로 강력 새로고침을 수행하는 것이 좋다.

```text
Ctrl + F5
```

---

## 9. 현재 상태

현재 프로젝트 상태는 다음과 같다.

## 프로젝트 작동 확인 결과

<img width="2017" height="780" alt="날짜별 인기뉴스 AI 큐레이션" src="https://github.com/user-attachments/assets/068b383d-8972-40bc-a374-fd1754566a44" />


https://ai-a1-3-k4cr-phi.vercel.app/

## 10. 주요 리스크

### 10.1 GDELT API 요청 제한

GDELT API는 무료 사용이 가능하지만 요청 제한이 강한 편이다.  
짧은 시간에 반복 요청하면 응답이 실패하거나 지연될 수 있다.

따라서 다음 보완이 필요하다.

- 요청 간격 제한
- 동일 검색 결과 캐싱
- 실패 시 사용자 안내 메시지 표시
- 대체 뉴스 API 검토

---

### 10.2 프론트엔드와 백엔드 응답 형식 불일치

프론트엔드 JavaScript는 백엔드 응답에서 다음 값을 기대한다.

```javascript
data.summary
data.articles
```

또는 일부 호환을 위해 다음 형태도 처리하고 있다.

```javascript
data.news
```

따라서 백엔드 `/api/news` 응답은 다음과 같은 구조로 통일하는 것이 좋다.

```json
{
  "summary": "AI 요약 내용",
  "articles": [
    {
      "title": "뉴스 제목",
      "description": "뉴스 설명",
      "url": "뉴스 링크"
    }
  ]
}
```

응답 구조가 다르면 화면에 결과가 표시되지 않을 수 있다.

---

## 11. 개선 제안

### 11.1 뉴스 API 변경 검토

현재 사용 중인 GDELT API는 요청 제한 및 안정성 측면에서 불편함이 있을 수 있다.

대안으로 다음 API를 검토할 수 있다.

- 네이버 뉴스 검색 API
- NewsAPI.org

특히 한국어 뉴스 중심 서비스라면 네이버 뉴스 API가 더 적합할 가능성이 있다.

---

### 11.2 사용자 경험 개선

현재는 기본 기능 구현 단계이므로, 추후 다음 기능을 추가할 수 있다.

- 검색 중 로딩 애니메이션 표시
- 검색 실패 시 상세 오류 메시지 출력
- 검색 결과가 없을 때 안내 문구 제공
- 날짜 기본값을 오늘 날짜로 자동 설정
- Enter 키 입력 시 검색 실행
- 기사 출처와 발행일 표시
- 뉴스 카드를 더 보기 좋게 스타일링

---

### 11.3 코드 안정성 강화

추후 다음과 같은 안정성 개선이 필요하다.

- 백엔드 API 응답 구조 표준화
- 외부 API 실패 시 예외 처리 강화
- OpenAI API 호출 실패 처리
- API 키 누락 시 명확한 오류 메시지 제공
- 프론트엔드 입력값 검증 강화
- 동일 요청 캐싱 처리

---

## 12. 다음 작업 계획

다음 단계에서는 검색 버튼 클릭 이벤트를 정상 연결하는 것이 최우선이다.

### 1단계: HTML 수정

`뉴스 검색` 버튼에 다음 속성을 추가한다.

```html
id="searchButton"
```

### 2단계: JavaScript 연결 확인

`index.html` 하단에 다음 코드가 있는지 확인한다.

```html
<script src="/static/js/main.js"></script>
```

### 3단계: 브라우저 Console 확인

새로고침 후 다음 로그를 확인한다.

```text
main.js 로드됨
```

### 4단계: 버튼 클릭 확인

버튼 클릭 후 다음 로그를 확인한다.

```text
뉴스 검색 버튼 클릭됨
```

### 5단계: 서버 API 요청 확인

터미널에서 다음과 유사한 로그를 확인한다.

```text
GET /api/news?date=2025-01-02&keyword=AI HTTP/1.1
```

### 6단계: 응답 데이터 화면 출력 확인

API 요청이 정상적으로 발생하면 다음을 확인한다.

- AI 요약이 `summaryBox` 영역에 표시되는지
- 뉴스 목록이 `newsList` 영역에 표시되는지
- 기사 링크가 정상 작동하는지

---

## 13. 결론

현재 프로젝트는 백엔드 서버 구성, 메인 페이지 출력, 정적 파일 구조, 외부 API 연동, 환경 변수 관리까지 주요 기반 작업이 완료된 상태이다.

현재 발생한 핵심 문제는 백엔드 서버 문제가 아니라, 프론트엔드에서 검색 버튼에 클릭 이벤트가 연결되지 않은 문제로 판단된다. 구체적으로는 HTML 버튼에 `id="searchButton"`이 없어서 JavaScript가 해당 버튼을 찾지 못한 것이 원인이다.

따라서 다음 수정이 필요하다.

```html
<button id="searchButton" type="button">
  뉴스 검색
</button>
```

이후 `main.js`에서 버튼 클릭 이벤트가 정상적으로 등록되면 `/api/news` 요청이 발생하고, 그 결과를 바탕으로 뉴스 목록과 AI 요약을 화면에 출력할 수 있다.

현재까지의 진행 상황은 전반적으로 양호하며, 남은 핵심 과제는 **프론트엔드 이벤트 연결과 API 응답 표시 검증**이다. 이 단계를 완료하면 서비스의 기본적인 사용자 흐름이 완성될 것으로 판단된다.
