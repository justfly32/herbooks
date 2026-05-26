# 헤르 도서관 (Her Books)

무료 도서 읽기 플랫폼 — Project Gutenberg + Open Library + PoetryDB 기반

## 실행

```bash
python3 server.py
# → http://localhost:8080
```

## 기능

- **책 찾기** — Open Library 검색 (제목/저자/장르)
- **책 읽기** — Project Gutenberg 전문 오버레이 리더
- **내 책장** — 저장/제거 (파일 기반 영구 저장)
- **서평** — 별점 + 리뷰 작성
- **시 모음** — PoetryDB 검색, 랜덤 시, 즐겨찾기

## 기술

- 단일 HTML + 순수 JavaScript (SPA)
- Python 프록시 서버 (Gutenberg CORS 우회 + 데이터 영속화)