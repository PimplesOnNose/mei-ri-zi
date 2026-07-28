# 每日字 · Měi Rì Zì

> *A word a day, like a daily vitamin for your Chinese.*

**[Live Demo](https://pimplesonnose.github.io/mei-ri-zi/)** — Try it now.

A static HSK 3.0 vocabulary learning app rooted deeply in traditional Chinese design 
and color philosophy — where Wu Xing (五行), the Ten Heavenly Stems (十天干), 
the Five-Colored Earth (五色土), and named traditional pigments are not decoration 
but the actual architecture of the app itself.

---

Crafted with 🤖 [Pi](https://pi.dev) · [DeepSeek](https://deepseek.com)

---

## The Idea

Take one HSK word per day, like a vitamin. Swallow it in a single sitting. 
Build fluency slowly — 一日一字，积少成多 ("one character a day; the small accumulates into the great").

The app is a quiet, daily ritual — not a flashcard grind. Calm, intentional, beautiful.

## Cultural Architecture

### HSK Levels → Wu Xing (Five Elements)

The learner walks the generative cycle (相生) from sprouting to mastery:

| HSK Level | Element | Color | Named Pigment |
|-----------|---------|-------|---------------|
| Prep | 天水 Heavenly Water | `#e8e8ec` | 月白 yuèbái |
| HSK 1 | 木 Wood | `#4a9e8a` | 青草 qīngcǎo |
| HSK 2 | 木→火 | `#6db3a4` | 翠微 cuìwēi |
| HSK 3 | 火 Fire | `#c4452d` | 朱砂 zhūshā |
| HSK 4 | 火→土 | `#c9a96e` | 赭石 zhěshí |
| HSK 5 | 土→金 | `#d4b878` | 缃色 xiāngsè |
| HSK 6 | 金 Metal | `#8faacc` | 月白银 |
| HSK 7-9 | 水 Water | `#3a6e8e` | 天青 tiānqīng |

### Days → Ten Heavenly Stems (天干)

Days are counted using the 十天干 (Ten Heavenly Stems) — 甲乙丙丁戊己庚辛壬癸 — 
cycling every ten days. Progress isn't an anxious count-up; it's a wheel turning.

### Tone Marks → Five-Colored Pinyin

Each pinyin tone maps to an element color, building visual intuition for tone classes:

| Tone | Element | Color |
|------|---------|-------|
| 1st ā | 金 Metal | `#c8c8d0` |
| 2nd á | 木 Wood | `#5fb388` |
| 3rd ǎ | 土 Earth | `#c9a96e` |
| 4th à | 火 Fire | `#d4654d` |
| Neutral a | 水 Water | `#5a7898` |

### The Five-Colored Earth Altar (五色土)

The progress bar at the bottom of every screen is modeled after the 社稷坛 
(Altar of Earth and Harvest) in Beijing — five bands of colored soil from
the five directions: green East, red South, yellow Center, white West, black North.

## Features

### Daily Learning

- **One word per day** — auto-advancing by personal local date; timeline is yours alone
- **Daily 识写习 loop** — Card (识) → Writing (写) → Review (习), flowing as a single ritual
- **Tone-colored pinyin** — rendered in five Wu Xing colors for visual tone intuition
- **Hanzi-writer practice** — 米字格 rice-grid canvas with Animate/Trace/Reveal modes
- **SM-2 spaced repetition** — words auto-enrolled on first view; 会了/需要再背 adjusts intervals
- **Edge TTS audio** — zh-CN-XiaoxiaoNeural (晓晓) voice, slowed 5% for learners

### Progress & Tracking

- **Heavenly-stem cycle counter** — 60-day 甲子 cycle replaces the linear streak
- **Five-Colored Earth mastery bar** — shows element-tier completion at a glance
- **Seasonal atmosphere** — background shifts subtly with the 24 solar terms (节气)
- **Weekly vitamin pack review** — every 7 days, review the past week's words
- **Missed-day catch-up** — gentle 补上/跳过 flow for skipped days

### Tone Practice (NEW!)

- **Microphone-based tone contour practice** — speak into your mic and see your pitch
  visualized in real time on an SVG grid, compared against the expected tone contour
- Supports all five tones (一声 high-level, 二声 rising, 三声 falling-rising, 四声 falling, 轻声 neutral)
- Per-character practice for multi-syllable words

### Export & Share

- **One-tap backup** — JSON export/import for full progress
- **Sync URL** — base64-gzipped state in the URL fragment; bookmark it, scan it, email it
- **Share card as image** — export today's word card as a PNG
- **Printable practice sheet** — opens a formatted A4 page with 米字格 grids for paper handwriting
- **甲子 celebration report** — printable one-pager showing cycle stats, altar progress, and memorable words

### Search & Review

- **Search** — across all vocabulary by Chinese, pinyin, or English, filtered by HSK level
- **Favorites** — save and browse favorite words
- **Quiz mode** — character→meaning and meaning→character quizzes with SRS feedback

### Platform

- **PWA installable** — add to home screen for near-native experience
- **Service Worker** — full offline support for core app and cached vocabulary
- **Keyboard shortcuts** — ← → navigation, space for audio, s for save, / for search, t for tone practice, and more

## Tech Stack

- **Static site** — plain HTML + CSS + JS, no build step, no server
- **Wu Xing design system** — scholar's ink-night palette with named traditional pigments
- **Hanzi-writer** — stroke animation and tracing for writing practice
- **Web Audio API** — real-time pitch detection for tone practice
- **localStorage** — all progress lives on device (~5KB per learner)
- **Edge TTS** — free neural TTS via Python `edge-tts` library

## Getting Started

```bash
# Clone or copy the project
cd mei-ri-zi

# Start a local server
./start.sh
# Or: python3 -m http.server 8080

# Open in browser
open http://localhost:8080
```

### Generating Audio (Optional)

```bash
pip install edge-tts
python3 scripts/generate_audio.py
```

### Downloading Stroke Data (Optional — enables fully offline writing practice)

```bash
python3 scripts/download_stroke_data.py
```

### Regenerating Vocabulary Data

```bash
# Download and build the full HSK 3.0 vocabulary
python3 scripts/generate_data.py

# For a quick test with only HSK 1-2:
python3 scripts/generate_data.py --enriched-only
```

## Project Structure

```
mei-ri-zi/
├── index.html              # Entry point — all HTML in one file
├── css/app.css             # Full Wu Xing design system
├── js/
│   ├── app.js              # Main application logic
│   ├── progress.js         # State management, personal timeline, export/import
│   ├── srs.js              # SM-2 spaced repetition algorithm
│   └── celebrations.js     # Yellow Dragon & Four Symbols guardian SVGs
├── data/
│   ├── hsk_daily.json      # Master word list (11,032 words)
│   ├── levels/             # Per-level vocabulary files
│   ├── char_strokes/       # Local hanzi-writer stroke data (run script)
│   └── _cache/             # Cached downloads
├── audio/
│   ├── index.json          # Audio path map
│   └── word_audio/         # Generated MP3 files
├── scripts/
│   ├── generate_data.py      # Build vocabulary from HSK 3.0 data
│   ├── generate_audio.py     # Edge TTS audio generation
│   └── download_stroke_data.py  # Download hanzi-writer stroke data
├── sw.js                   # Service Worker for offline support
├── manifest.json           # PWA manifest
└── start.sh                # Dev server launcher
```

## Data Sources

HSK 3.0 vocabulary lists sourced from [krmanik/HSK-3.0](https://github.com/krmanik/HSK-3.0) — 
11,032 words across all 7 HSK levels. Every word has AI-generated example sentences 
(DeepSeek), radical/glyph breakdowns for all characters, and Edge TTS audio (晓晓) 
for all HSK levels.

## License

MIT
