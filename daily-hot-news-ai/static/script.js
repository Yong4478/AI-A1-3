const dateInput = document.getElementById("dateInput");
const keywordInput = document.getElementById("keywordInput");
const searchBtn = document.getElementById("searchBtn");
const statusDiv = document.getElementById("status");
const summaryDiv = document.getElementById("summary");
const newsListDiv = document.getElementById("newsList");

searchBtn.addEventListener("click", searchNews);

async function searchNews() {
  const date = dateInput.value;
  const keyword = keywordInput.value.trim();

  if (!date) {
    alert("날짜를 선택하세요.");
    return;
  }

  if (!keyword) {
    alert("키워드를 입력하세요.");
    return;
  }

  searchBtn.disabled = true;
  searchBtn.textContent = "검색 중...";
  statusDiv.textContent = "뉴스를 가져오는 중입니다...";
  summaryDiv.textContent = "";
  newsListDiv.innerHTML = "";

  try {
    const url = `/api/news?date=${encodeURIComponent(date)}&keyword=${encodeURIComponent(keyword)}`;
    const response