# 📚 헤르 도서관 · Hermes Free Books

GitHub Pages에서 완전히 동작하는 무료 도서관 웹앱입니다.

## 🏗 아키텍처

```
100% Static — no backend needed
┌─────────────────────────────────┐
│  GitHub Pages                    │
│  https://justfly32.github.io/   │
│  herbooks/                       │
│  └── index.html                  │
│  └── books/ (24권 캐시)          │
└──────────┬──────────────────────┘
           │ raw.githubusercontent.com (CORS ✅)
           ▼
       책 텍스트 서빙
```

- **프론트엔드**: 순수 HTML/CSS/JS, GitHub Pages에서 정적 호스팅
- **책 데이터**: 저장소 `books/` 폴더에 포함, `raw.githubusercontent.com`으로 CORS 문제 없이 제공
- **사용자 데이터**: 브라우저 `localStorage`에 저장 (캐시 초기화 시 소실)

## 📖 포함된 책 (24권)

| # | Gutenberg ID | 제목 | 저자 |
|---|---|---|---|
| 1 | 1342 | Pride and Prejudice | Jane Austen |
| 2 | 11 | Alice's Adventures in Wonderland | Lewis Carroll |
| 3 | 84 | Frankenstein | Mary Shelley |
| 4 | 1661 | Sherlock Holmes | Arthur Conan Doyle |
| 5 | 43 | Dracula | Bram Stoker |
| 6 | 74 | Tom Sawyer | Mark Twain |
| 7 | 2701 | Moby Dick | Herman Melville |
| 8 | 1260 | Jane Eyre | Charlotte Brontë |
| 9 | 1400 | Great Expectations | Charles Dickens |
| 10 | 158 | Emma | Jane Austen |
| 11 | 1952 | The Yellow Wallpaper | C.P. Gilman |
| 12 | 768 | Wuthering Heights | Emily Brontë |
| 13 | 174 | Dorian Gray | Oscar Wilde |
| 14 | 844 | The Importance of Being Earnest | Oscar Wilde |
| 15 | 36 | War of the Worlds | H.G. Wells |
| 16 | 120 | Treasure Island | R.L. Stevenson |
| 17 | 1998 | The Jungle Book | Rudyard Kipling |
| 18 | 23042 | Siddhartha | Hermann Hesse |
| 19 | 2591 | Grimm's Fairy Tales | Brothers Grimm |
| 20 | 5200 | Metamorphosis | Franz Kafka |
| 21 | 6130 | The Iliad | Homer |
| 22 | 30254 | The Republic | Plato |
| 23 | 5000 | The Art of War | Sun Tzu |
| 24 | 1497 | The Republic | Plato (2nd trans.) |

## 📚 책 추가하는 법

새로운 책을 읽고 싶다면:

1. Gutenberg ID 확인 (예: `https://www.gutenberg.org/ebooks/{ID}`)
2. 텍스트 다운로드: `https://www.gutenberg.org/cache/epub/{ID}/pg{ID}.txt`
3. `books/pg{ID}.txt`로 저장소에 추가
4. `index.html`의 `FEATURED` 배열에 추가 (선택)
5. PR 또는 직접 push

## 🛠 로컬 개발

```bash
python3 -m http.server 8080
# 또는 그냥 브라우저에서 index.html 열기
```

## 🚀 배포

GitHub Pages가 자동 배포합니다.
- `main` 브랜치 루트 → `https://justfly32.github.io/herbooks/`
