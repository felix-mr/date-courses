# Date Courses

둘이 함께 관리하는 데이트 코스 기록.

## 구조

```text
courses/
  YYYY/
    YYYY-MM-DD-지역-짧은-이름/
      README.md
      course-options.html
templates/
  course-readme-template.md
```

## 기록 규칙

1. 새 코스마다 `courses/YYYY/YYYY-MM-DD-지역-짧은-이름/` 생성.
2. 계획 단계에는 `README.md`와 모바일용 공유 HTML을 추가.
3. 다녀온 뒤 같은 `README.md`의 후기만 업데이트하고 원래 계획은 보존.
4. 카테고리는 바다 / 맛집 / 드라이브 / 글램핑 / 1박 / 후보조사처럼 기록.
5. 음식점 메뉴·숙소·운영시간은 수정할 때 웹에서 다시 확인하고, 확인일과 출처를 남긴다. 당일 재고·영업은 확정으로 쓰지 않는다.
6. 새 기록을 추가하거나 기존 날짜를 수정하면 이 목록과 루트 `index.html`도 함께 갱신한다. 기존 기록은 삭제하지 않는다.

## 현재 기록

- [2026-10-01 · 대천 / Hotel Solaire](courses/2026/2026-10-01-daecheon-solaire/) — 숙소 확정 · 대천항 생새우회/활어회 · 상화원 또는 대안 일정
- [2026-09-30 · 태안 / 안면도](courses/2026/2026-09-30-taean-anmyeondo/) — 바다 · 대하 · 회 · 후보조사
- [2026-09-29 · 1박 여행 후보 조사](courses/2026/2026-09-29-one-night-candidates/) — 후보조사 · 바다 · 자연
- [2026-09-19 · 수원 행궁동 / 동탄호수공원](courses/2026/2026-09-19-suwon-tatsumi/)

## 공유

루트 `index.html`은 날짜 최신순과 카테고리로 코스를 탐색하는 GitHub Pages용 홈입니다. Pages 게시 설정은 저장소 Settings → Pages에서 별도로 켜야 합니다.
