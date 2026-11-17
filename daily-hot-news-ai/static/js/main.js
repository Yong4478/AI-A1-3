document.addEventListener("DOMContentLoaded", () => {
  console.log("main.js 로드됨");

  const searchButton = document.getElementById("searchButton");
  const dateInput = document.getElementById("dateInput");
  const keywordInput = document.getElementById("keywordInput");
  const summaryBox = document.getElementById("summaryBox");
  const newsList = document.getElementById("newsList");

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

    try {
      const url = `/api/news?date=${encodeURIComponent(date)}&keyword=${encodeURIComponent(keyword)}`;
      console.log("요청 URL:", url);

      const response = await fetch(url);
      const data = await response.json();

      console.log("API 응답:", data);

      if (!response.ok) {
        summaryBox.innerHTML = "서버 오류가 발생했습니다.";
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
    }
  });
});