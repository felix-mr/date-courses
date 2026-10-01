(() => {
  // Preserve shared links created before the collections had separate pages.
  if (document.body.dataset.view === "upcoming" && location.hash === "#wishlist") {
    location.replace("wishlist.html");
    return;
  }

  const parts = new Intl.DateTimeFormat("en", {
    timeZone: "Asia/Seoul", year: "numeric", month: "2-digit", day: "2-digit"
  }).formatToParts(new Date());
  const part = type => parts.find(item => item.type === type).value;
  const today = `${part("year")}-${part("month")}-${part("day")}`;
  const records = window.travelRecords;
  const view = document.body.dataset.view;
  const groupOf = record => record.group === "scheduled"
    ? (record.end < today ? "history" : "upcoming")
    : record.group;
  const recordById = new Map(records.map(record => [record.id, record]));
  const cards = [...document.querySelectorAll(".course-card")];
  const state = { region: "all", theme: "all" };
  const regionButtons = [...document.querySelectorAll("[data-region-filter]")];
  const themeButtons = [...document.querySelectorAll("[data-theme-filter]")];
  const regionMatches = (region, choice) => choice === "all" || region === choice;
  const inView = record => groupOf(record) === view;

  document.querySelectorAll("[data-view-count]").forEach(count => {
    count.textContent = records.filter(record => groupOf(record) === count.dataset.viewCount).length;
    count.parentElement.setAttribute("aria-label", `${count.previousElementSibling.textContent}, ${count.textContent}개 기록`);
  });
  document.querySelectorAll("[data-region-count]").forEach(count => {
    count.textContent = records.filter(record => inView(record) && regionMatches(record.region, count.dataset.regionCount)).length;
    count.parentElement.setAttribute("aria-label", `${count.parentElement.firstChild.textContent}, ${count.textContent}개 후보`);
  });

  function render() {
    let visible = 0;
    cards.forEach(card => {
      const record = recordById.get(card.dataset.recordId);
      const regionMatch = regionMatches(card.dataset.region, state.region);
      const themeMatch = state.theme === "all" || card.dataset.categories.split(" ").includes(state.theme);
      card.hidden = !(record && inView(record) && regionMatch && themeMatch);
      if (!card.hidden) visible++;
    });
    document.querySelectorAll(".record-group").forEach(group => {
      group.hidden = ![...group.querySelectorAll(".course-card")].some(card => !card.hidden);
    });
    regionButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.regionFilter === state.region)));
    themeButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.themeFilter === state.theme)));
    document.getElementById("result-count").textContent = `${visible}개 ${view === "wishlist" ? "후보" : "기록"}`;
    document.getElementById("empty-state").hidden = visible !== 0;
    if (view === "wishlist") {
      const noOverseas = state.region === "overseas" && !records.some(record => inView(record) && record.region === "overseas");
      document.getElementById("empty-title").textContent = noOverseas ? "아직 해외 여행 후보가 없어요" : "이 조건에 맞는 후보가 없어요";
      document.getElementById("empty-description").textContent = noOverseas ? "해외 여행을 계획할 때 이곳에 추가할게요." : "지역이나 테마를 바꿔서 다른 코스를 찾아보세요.";
    }
  }
  regionButtons.forEach(button => button.addEventListener("click", () => { state.region = button.dataset.regionFilter; render(); }));
  themeButtons.forEach(button => button.addEventListener("click", () => { state.theme = button.dataset.themeFilter; render(); }));
  document.getElementById("reset-filters")?.addEventListener("click", () => {
    state.region = "all"; state.theme = "all"; render(); regionButtons[0].focus();
  });
  render();
})();
