# img2md

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&style=flat-square)](https://fastapi.tiangolo.com/)
[![Tesseract](https://img.shields.io/badge/Tesseract-OCR-yellow?style=flat-square)](https://github.com/tesseract-ocr/tesseract)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js&style=flat-square)](https://nextjs.org/)
[![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38bdf8?logo=tailwindcss&style=flat-square)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)

A fully local image-to-Markdown converter. Drop in a screenshot, photo, or scan. Get back clean, structured Markdown. Runs entirely on your machine using Tesseract OCR and a heuristic layout parser.

## Why this exists

There's a workflow a lot of people land on without realizing it's a workaround:

You have a screenshot. A system monitor panel, a PDF page, a chart, a receipt. You want to *talk* to an AI about it. So you paste the image into a chat assistant. It works. You start discussing. Then, mid-conversation:

> *You've reached your limit for image uploads. Upgrade to Pro to continue.*

The chat is locked. You lose the thread. Tomorrow you get a few more, then the same wall.

So you stop pasting images into chat assistants. Instead you convert the image to **text** first, because text has no upload limit, no vision-token surcharge, and it fits in any model's context without burning quota. Then you paste the markdown, discuss it freely, and keep your conversation alive.

The problem: the free online converters you use for that have the *exact same business model*. One or two conversions, then:

> *You've used your free conversions for today. Get Premium for unlimited.*

You've just moved the paywall from one place to another. And on the way, you uploaded your screenshot (a receipt, a contract, a dashboard, a medical note) to a server you don't own, under a retention policy you didn't read, with no idea whether it's being logged or used for training.

img2md breaks that loop. It does the conversion locally, on your machine, with no counter running.

**No per-conversion limit.** Convert one image or one thousand. Same result, same speed, no wall.

**No account, no sign-up, no "free tier."** The tool doesn't know who you are and doesn't care. There's nothing to upgrade.

**No upload to a third-party server.** The backend runs on `127.0.0.1`. Your image never leaves your computer.

**No token cost when you take it to a chat assistant.** Once you have the markdown, you can paste it into any LLM (free tier, paid tier, local model), and it costs text tokens instead of vision tokens. A 1,200-token screenshot becomes maybe 400 tokens of markdown. Your chat stays alive longer, your discussion stays on topic, and you're not fighting the image-upload meter every few messages.

**Latency you can reason about.** 1 to 3 seconds per image locally, deterministic. No queue, no cold starts, no load-dependent slowdowns.

**It works offline.** On a plane, in a hotel with bad Wi-Fi, or when the converter site is down because everyone else is using it.

This isn't a claim that local OCR beats a vision model on quality. Vision-language models are genuinely better at handwriting, multi-column layouts, formulas, and complex tables. If your inputs are those, use a VLM. For the common case (screenshots of articles, receipts, book pages, printed text, UI panels), Tesseract gets you 90% of the quality with none of the metering, and it gives you text you can actually take into a chat without hitting the image-upload cap.

## Privacy by construction

The rate limit is what makes people look for a local tool. The privacy is what makes them keep it.

When you upload to any hosted converter (an online PDF tool, an OCR website, a chat window), the image is on someone else's server. From that moment, it's subject to:

- **Their retention policy.** Some delete within hours, some keep for 30 days, some indefinitely. You don't get to choose, and the default is usually not what you'd pick.
- **Their training pipeline.** Uploads to free services frequently become training data or feed internal analytics. Opt-outs are often buried or missing.
- **Their access controls.** Support staff, security teams, and automated classifiers may review the content.
- **Their security perimeter.** A breach on their side is a breach of your data. You have no say in how well they've hardened it.

For a screenshot of a public webpage, none of this matters. For a receipt with the last four digits of your card, a signed contract, a medical test result, a scan of your ID, or an internal dashboard with customer data, it matters a lot. And the people most likely to have those images are exactly the people who shouldn't be pasting them into someone else's queue.

img2md doesn't upload anything anywhere.

- **No external server.** The backend runs on `http://127.0.0.1:8000`. The only network traffic is your browser talking to your own machine.
- **No third-party API calls.** Tesseract is a local binary. No telemetry, no analytics, no crash reporting phoning home.
- **No cloud storage.** Uploads land in `backend/uploads/`, outputs in `backend/outputs/`, both on your disk.
- **Auto-delete after 30 minutes.** A background sweeper runs every minute and removes anything older than the retention window. You can change or disable it in `backend/app/config.py`, but the default is designed so sensitive files don't linger.

You can verify the offline claim by reading the code. There are no hidden network calls. `grep -r "requests\." backend/` returns nothing. `grep -r "http" backend/app/services/` returns nothing. The only `fetch` in the frontend talks to `127.0.0.1`.

## Features

**Structure-aware conversion.** Most OCR tools dump a flat wall of text. img2md parses Tesseract's hOCR output (bounding boxes, line heights, word positions) and reconstructs document structure: headings become `#`, lists become `-`, paragraphs get merged based on vertical gaps. Heuristic, not ML. Deterministic, fast, and effective on printed documents.

**Unlimited usage.** No quotas, no daily caps, no "free tier" that isn't. Convert as many images as you want.

**100% offline.** Tesseract runs on your CPU. The FastAPI backend runs on localhost. Your images never leave your machine.

**Markdown that's cheap to paste into a chat assistant.** The output is compact, structured, and token-efficient. A document screenshot that would cost 1,200 vision tokens becomes a few hundred text tokens. Your chat stays under the limit for longer, and the context stays readable.

**Side-by-side preview.** Image on the left, Markdown on the right. Two tabs: **Preview** (rendered) and **Edit** (raw text you can tweak before copying).

**One-click copy and download.** Copy to clipboard, or download as a `.md` file. No sign-in, no gating.

**Auto-delete after 30 minutes.** A background sweeper removes uploads and outputs past the retention window.

**Dark mode.** Follows your OS preference.

**Multi-format input.** PNG, JPG, WEBP, TIFF. If Tesseract can read it, we can convert it.

## How it works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  Upload     │ ──► │  Tesseract   │ ──► │  hOCR       │ ──► │  Heuristic   │
│  image      │     │  (OCR)       │     │  parser     │     │  structure   │
└─────────────┘     └──────────────┘     └─────────────┘     └──────┬───────┘
                                                                     │
                                                                     ▼
                                                              ┌──────────────┐
                                                              │  Markdown    │
                                                              └──────────────┘
```

1. **Upload:** image saved to a temp folder with a UUID filename
2. **OCR:** Tesseract runs in hOCR mode and returns XML with bounding boxes and per-word confidence scores
3. **Parse:** every line is extracted with its position, height, and word-level data
4. **Infer:** heuristics detect headings (lines taller than the median), lists (bullets, numbers, dashes), and paragraphs (merging lines with small vertical gaps)
5. **Return:** Markdown served as JSON and saved as a `.md` file for download

No ML models. No GPU. No API calls. No tokens consumed.

## What it's good at

| Input | Quality |
|---|---|
| Screenshots of articles, blogs, documentation | Excellent |
| Book pages, receipts, invoices (printed text) | Very good |
| Single-column PDFs exported as images | Very good |
| Handwriting | Hit-or-miss |
| Multi-column UI dashboards | Poor, see below |
| Math formulas | Not supported |

**Known limitation:** multi-column layouts break because Tesseract reads left-to-right, top-to-bottom, and loses column pairing. Fixing this properly requires layout analysis (Surya) or a vision-language model. Both are out of scope for the current offline-only design.

If your inputs are mostly multi-column or handwritten, a VLM will outperform this tool on the conversion step, and that's the honest trade-off. It just comes with a vision-upload quota attached, which is the thing this tool is designed to avoid.

## Getting started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Tesseract OCR: [Windows installer](https://github.com/UB-Mannheim/tesseract/wiki), or:
  - Ubuntu: `sudo apt install tesseract-ocr tesseract-ocr-eng`
  - macOS: `brew install tesseract tesseract-lang`

### Backend

```bash
cd backend
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Runs on `http://127.0.0.1:8000`. Health check at `/health`, API docs at `/docs`.

If Tesseract isn't on your PATH (common on Windows), edit `backend/app/services/ocr.py` and set:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:3000`.

## Project structure

```
img2md/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry + lifespan hooks
│   │   ├── config.py            # paths, size limits, retention window
│   │   ├── routers/
│   │   │   └── convert.py       # POST /api/image-to-markdown
│   │   └── services/
│   │       ├── ocr.py           # Tesseract wrapper (hOCR mode)
│   │       ├── structure.py     # hOCR → Markdown inference
│   │       ├── storage.py       # file I/O
│   │       └── cleanup.py       # background auto-delete
│   └── requirements.txt
│
└── frontend/
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx
    │   └── globals.css
    ├── components/
    │   └── ImageMarkdownPanel.tsx
    ├── lib/
    │   └── api.ts
    └── package.json
```

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| OCR | Tesseract 5 | Mature, fast, offline, free |
| XML parsing | lxml | Fast and robust against malformed hOCR |
| Backend | FastAPI | Async, typed, auto-generated docs |
| Server | Uvicorn | Simple, fast ASGI |
| Frontend | Next.js 14 | App Router, SSR-ready |
| Styling | Tailwind CSS | Fast iteration, no fighting the framework |
| Markdown rendering | react-markdown + remark-gfm | Tables, task lists, strikethrough |
| Icons | lucide-react | Consistent icon set |

## Roadmap

- [x] Image → Markdown (heuristic)
- [x] Auto-delete cleanup
- [x] Preview / Edit tabs
- [x] Copy + Download
- [ ] PDF → Markdown (rasterize pages, reuse pipeline)
- [ ] Batch images → ZIP of `.md` files
- [ ] Language selector (Chinese, French, etc.)
- [ ] Self-hosted layout model (Surya) for hard inputs
- [ ] Docker Compose for one-command startup

## Contributing

Issues and pull requests welcome. If you're adding a feature, please keep it **offline-first** with no cloud API dependencies, no rate limits, no quotas, no telemetry.

## License

MIT.
