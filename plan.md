# 每日字 · Měi Rì Zì — Plan

> *A word a day, like a daily vitamin for your Chinese.*
>
> A static HSK 3.0 vocabulary learning app rooted deeply in traditional Chinese design and color philosophy — where Wu Xing, the Ten Heavenly Stems, Five-Colored Earth, and named traditional pigments are not decoration but the actual architecture of the app itself.

---

## 1. The Idea

Take one HSK word per day, like a vitamin. Swallow it in a single sitting. Build fluency slowly, the way tradition says everything worth having is built — 一日一字，积少成多 ("one character a day; the small accumulates into the great").

The app is a quiet, daily ritual — not a flashcard grind. Calm, intentional, beautiful. The traditional Chinese design is not a costume; it is the structure of the app. Every visual decision maps to a real Chinese cultural system: Wu Xing (五行 五色), the Ten Heavenly Stems (十天干), the Four Symbols (四象), the Twenty-Four Solar Terms (二十四节气), and the traditional named pigments used in Chinese silk dyeing and ink-wash painting for two thousand years.

---

## 2. The Cultural Architecture (this is the "truly unique" part)

Most "Chinese-themed" apps slap red lanterns and gold trim onto a generic UI. This app does the opposite. Every structural decision is sourced from a real Chinese system and applied faithfully.

### 2.1 HSK Levels → Wu Xing (Five Elements)

The HSK 3.0 standard (2021 revised, finalized 2025 by China's Ministry of Education) has **9 levels** plus a learner's "preparation" tier. The traditional 五行 has **5 elements**. We resolve the mismatch honestly using the **intermediary colors** of the Wu Xing system (the same resolution used in Tang dynasty court color theory):

| HSK Level | Element | Named Color | Hex | Phase | Cultural Meaning |
|-----------|---------|-------------|------|-------|------------------|
| **Prep · 入门** | 天水 Tian-Shui (heavenly water) | 月白 yuèbái | `#e8e8ec` | New Yin | The seed — water waiting to sprout |
| **HSK 1** | 木 Wood | 青草 qīngcǎo | `#4a9e8a` | New Yang | Sprouting — first green shoots |
| **HSK 2** | 木→火 Wood→Fire | 翠微 cuìwēi | `#6db3a4` | Yang rising | Growing toward kindling |
| **HSK 3** | 火 Fire | 朱砂 zhūshā | `#c4452d` | Full Yang | Blooming — the language is alive |
| **HSK 4** | 火→土 Fire→Earth | 赭石 zhěshí | `#c9a96e` | Balancing Yang | Ripening — fruit on the branch |
| **HSK 5** | 土→金 Earth→Metal | 缃色 xiāngsè | `#d4b878` | Balance | Harvest — grain stored |
| **HSK 6** | 金 Metal | 月白银 yuèbái-yín | `#8faacc` | New Yin | Refining — metal hammered |
| **HSK 7–9** | 水 Water | 天青 tiānqīng | `#3a6e8e` | Full Yin | Depth — flowing freely, mastery |

This is the generative cycle (相生): Wood → Fire → Earth → Metal → Water. The learner literally walks the elemental wheel from sprouting to mastery. We earn the metaphor — we don't borrow it.

This is also how `yueli` codes its event types — so the visual language is consistent across your projects, and a learner who has used `yueli` will recognize the same Yellow-Earth gold (地球 / 节气) here.

### 2.2 Days → Ten Heavenly Stems (天干)

The Chinese world was counted in ten for three thousand years before any contact with the Gregorian calendar. The **Ten Heavenly Stems (十天干)** — 甲乙丙丁戊己庚辛壬癸 — cycle every ten days. Our "vitamin" app has exactly one entry per day for 10 days = a *jiazi*-mini-cycle.

So:
- Day 1 starts on 甲 (jiǎ) — the first stem, associated with East, Wood, new Yang
- Day 10 lands on 癸 (guǐ) — the last stem, North, Water, full Yin — the cycle completes
- Day 11 returns to 甲 — a new 小旬 (ten-day week) begins

The heavenly-stem badge replaces the meaningless "Day 47" with 甲·初七 ("Stem 甲, third week, day seven") — a cyclical, culturally-grounded marker instead of a linear streak. Progress isn't an anxious count-up; it's a wheel turning.

**Why this matters:** a learner who keeps a streak for 60 days has completed a full **甲子 (jiǎzǐ)** cycle — the most auspicious unit in the Chinese calendar. We celebrate that as the "完成的甲子" — the completed cycle. This is materially deeper than Duolingo's flame.

### 2.3 Tone Marks → Five-Colored Pinyin

Chinese tones map beautifully onto the five elements because tones are themselves five-fold in modern Mandarin — the four lexical tones plus the neutral tone (五声). We color the pinyin so that the learner absorbs the Wu Xing through the act of reading:

| Tone | Pinyin mark | Element | Color | Name | Why |
|------|-------------|---------|-------|------|-----|
| **1st** | `ā` | Metal (金) | Silver | `#c8c8d0` | High and steady, like polished metal struck and ringing |
| **2nd** | `á` | Wood (木) | Green | `#5fb388` | Rising tone, like a tree growing upward |
| **3rd** | `ǎ` | Earth (土) | Ochre | `#c9a96e` | Falling-rising, like soil heaving up then settling |
| **4th** | `à` | Fire (火) | Vermilion | `#c4452d` | Falling and decisive, like a struck match |
| **Neutral** | `a` | Water (水) | Ink | `#3a4858` | Calm, depthless, like still water |

So the pinyin **nǐ hǎo** renders as **nǐ** (earth-ochre) **hǎo** (earth-ochre). A rising **má** is green. A sharp **bù** is vermillion. Each sentence becomes a small painting of color — and over days, the learner builds a *visual* intuition for tone classes, not just an auditory one. This is genuinely grounded pedagogy, not decoration.

### 2.4 The Seasons → 24 Solar Terms (节气)

The "vitamin" calendar moves through the year. The background atmosphere of the app shifts subtly with the 24 traditional solar terms — the same system already implemented in `yueli` and visible on almanacs across China for two millennia.

- 立春 Lìchūn (Feb 4): the lightest green whisper enters the background
- 夏至 Xiàzhì (Jun 21): the warmest tones
- 立秋 Lìqiū (Aug 7): the air cools to gold
- 冬至 Dōngzhì (Dec 22): the deepest night blue / ink

The HSK level of the day's word still determines the card accent — but the surrounding "air" of the page breathes with the season. A learner opening 每日字 on 冬至 sees a different sky than on 夏至, even if the day's word is the same level.

This is not animated wallpaper — it is the calendar-as-context that `yueli` already established.

### 2.5 The Four Symbols (四象) — Level Guardians

Each HSK tier gets a guardian drawn from the deep mythic pattern of the Four Symbols + Yellow Dragon:

| Level Range | Guardian | Direction | Element | Where it appears |
|-------------|----------|-----------|---------|------------------|
| Prep–HSK 2 | 青龙 Azure Dragon | East | Wood | On the intro / onboarding card |
| HSK 3–4 | 朱雀 Vermilion Bird | South | Fire | On the "level-up to Fire" celebration |
| HSK 5–6 | 玄武 Black Tortoise (Water) + 白虎 White Tiger (Metal) | North / West | Water / Metal | On the level-up to Metal/Water |
| Mastery (HSK 7-9 complete) | 黄龙 Yellow Dragon | Center | Earth | On the *jiazi*-completed celebration |

These appear sparingly — only on transitions and celebrations, never cluttering the daily card. They are SVG ink-wash illustrations drawn in a single stroke weight, traditional brushwork, not cute mascot art.

### 2.6 The Five-Colored Earth (五色土)

The famous 社稷坛 (Altar of Earth and Harvest) in Beijing is built from soil gathered in the five directions: green from the East, red from the South, white from the West, black from the North, yellow from the Center. This is the most material expression of Wu Xing in the actual landscape.

Our "level mastery" visualization uses the metaphor: a horizontal altar strip at the bottom of the app shows five earth bands. Each band fills as the corresponding HSK element tier is completed. The altar itself is the progress bar.

---

## 3. The Vitamin Card

The daily card is one screen, one word, no overwhelm.

```
┌──────────────────────────────────────────────┐
│  每日字 · 甲子初七 · 立春                ☆ ★  │   ← stem-cycle badge, solar term, save
│   Day 47 · HSK 2 · 木                        │   ← simple English fallbacks too
├──────────────────────────────────────────────┤
│                                               │
│              一起                              │   ← the character, serif, breathing room
│              yī  qǐ                            │   ← pinyin, tone-colored
│                                               │
│   adverb · "together"                          │
│                                               │
│   ─── 例句 Example ─────────                  │
│   我们一起去学校。                              │
│   Wǒmen yīqǐ qù xuéxiào.                      │
│   "Let's go to school together."               │
│                                               │
│   ─── 字形 Glyph ▸ ────                       │
│   一 = one   起 = to rise up                   │   ← expandable, tap to open
│   起: semantic 走 (walk) + phonetic 己         │
│                                               │
│   ─── 音声 Audio ────                         │
│   ▶ 听 · 晓晓 (Edge TTS, zh-CN female)          │   ← slowed 5% for learner clarity
│                                               │
│   ← 上一日    今日    下一日 →                │   ← nav
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━                  │
│   五色土 altar · ●●●○○                         │   ← mastery progress as earth bands
└──────────────────────────────────────────────┘
```

The hierarchy:
1. The character itself — biggest, most breath
2. Pinyin, tone-colored — supporting, not competing
3. Meaning — quiet, lowercase next to a part-of-speech tag
4. Example sentence — the vitamin in context, with translation hidden by default (tap to reveal)
5. Glyph breakdown — tucked away, expands on tap
6. Audio — single play button, one voice (晓晓 / zh-CN-XiaoxiaoNeural, Edge TTS), slowed 5% for learner clarity
7. Navigation
8. The five-colored earth altar — persistent mastery bar, always at the bottom

---

## 4. Features

### 4.1 MVP (v1) — the vitamin itself

1. **One word per day**, auto-advancing by **personal** local date — first visit sets `start_date` and shows "Day 1 · 甲子初一日"; each following calendar day advances one word in the master HSK sequence. Returning visitors land on today's word. See §4.4 for the personal-timeline model.
2. **The daily 识写习 sequence** — Card (识) → Writing (写) → Review (习), flowing as a single daily ritual, each phase skippable. See §4.6.
3. **Tone-colored pinyin** rendered in five element colors.
4. **Edge TTS audio**, voice = zh-CN-XiaoxiaoNeural (Chinese female, 晓晓), slowed 5% for learner clarity — generated offline once per word, cached as MP3.
5. **Save / favorite** (★) — saved word list view.
6. **Arrow-key navigation** between days. Home = today. This pattern already lives in `yueli` and `modern_chengyu`.
7. **Streak / cycle counter** using the heavenly-stem cycle rather than a numeric streak. Completion of 甲子 (60 days) is a small celebration. Streak is **personal** — counted from the learner's own `start_date`, not a global epoch.
8. **Search** across all words (input field toggled from header), filtered by HSK level.
9. **Five-colored earth mastery bar** at the bottom showing element-tier completion.
10. **Seasonal atmosphere** following 二十四节气 (computed locally, no server).
11. **One-tap backup file** (`备份` button in settings) — downloads `每日字-progress-YYYY-MM-DD.json`. `恢复` button restores from a previously selected file. See §4.5.
12. **Sync URL** (`链接同步` button in settings) — creates a self-contained URL fragment containing a base64-gzipped state blob. Open on a new device to restore state. Fragment stays client-side; no server ever receives it. See §4.5.
13. **Writing practice with hanzi-writer** — 米字格 rice-grid canvas, animate/quiz/show modes, multi-character support, quiz result feedback. Ported from `xuehanyu`'s proven implementation. See §4.7.
14. **SM-2 spaced repetition** — words auto-enrolled on first open; review queue surfaces 1-4 due words daily; 会了/需要再背 buttons adjust ease. Ported from `xuehanyu`'s `srs.ts`. See §4.6 (习 Review phase).

### 4.2 v2 — the regimen

15. **Quiz mode** — character → meaning, meaning → character, audio → meaning. Builds on the SRS already present in v1.
16. **Printable practice sheet export** — PDF with the day's word in 米字格 for paper practice.
17. **Weekly vitamin pack review** — Sunday is a review of the 7 words you took that week.
18. **Printable 甲子 celebration sheet** (Option C in §4.5) — a one-page PDF newsletter showing start date, words seen, levels completed, the five-colored earth altar fully drawn, sample memorable characters, and next 7 days in 米字格 grids. A learner prints one every completed 甲子 cycle as a tangible record of their practice.
19. **Tone contour practice** — microphone-based tone production exercise with SVG pitch visualization (adapted from `xuehanyu`'s `ToneVisualizer.tsx`).

### 4.3 v3 — the regimen becomes a long practice

20. **PWA install** — works offline, add to home screen.
21. **Animation of the four guardians** — short ink-wash motion tweens only on level transitions.
22. **Share card** — export the day's card as a square image for sharing.
23. **Optional anonymous cloud sync** (only if user demand warrants) — a tiny serverless backend (Cloudflare Workers) that stores state blobs keyed by a sync token, with TTL. Still static-app at heart; cloud is an optional convenience layer.

---

### 4.4 Personal Timeline Tracking

The "one vitamin a day" metaphor only works if each learner's timeline is their own. This is the opposite of Wordle (where everyone gets the same word on the same calendar day) and the opposite of Duolingo's global streak-counter — both of which assume a *shared* calendar. For sequential language learning, a shared calendar is wrong: people start on different days, learn at different paces, and may switch levels.

#### The personal-timeline principle

- On a learner's **first ever visit**, we set `learner.start_date = today` (local date, ISO format).
- Every following calendar day advances `current_word_index` by exactly 1.
- "Day N" displayed in the badge is `today - start_date + 1`.
- The heavenly-stem badge is `HEAVENLY_STEMS[N % 10]` where N is personal offset, and the weekly subcycle is `floor(N / 10) + 1` (初一, 初二, … 初十) — also personal.
- Two learners opening the app for the first time on different calendar dates both see "Day 1 · 甲子初一日" on their respective first days, and both walk the same HSK 3.0 master sequence (just offset in time).
- The **content** each "Day N" is shared with every other learner on their "Day N" — see §6.2 Scheduling.
- The **date** you arrive at that content is personal.

This avoids the entire class of "what day is everyone on?" synchronization problems and keeps the streak — the甲子 cycle — meaningful as a *personal* ritual milestone.

#### What we track (full state schema)

A single JSON object, ~5KB per learner, lives in `localStorage` under the key `mei-ri-zi/state`:

```json
{
  "version": 1,
  "schema": "mei-ri-zi/state",
  "created_at": "2026-03-15T08:12:00Z",
  "learner": {
    "start_date": "2026-03-15",
    "start_offset": 0
  },
  "progress": {
    "last_opened_date": "2026-05-04",
    "current_hsk_level": 2,
    "words_seen": ["hsk1_0001", "hsk1_0002", "hsk1_0197"],
    "levels_completed": [],
    "completed_jiazi_cycles": 0,
    "daily_pillar_completed": { "shi": false, "xie": false, "xi": false }
  },
  "favorites": ["hsk1_0003", "hsk2_0197"],
  "srs": [
    {
      "id": "hsk1_0001",
      "word": "你好",
      "pinyin": "nǐhǎo",
      "english": "hello",
      "level": 1,
      "ease": 2.5,
      "interval": 0,
      "nextReview": 1711929600000,
      "repetitions": 0,
      "lastWritingScore": null
    }
  ],
  "writing_cursor": {
    "word_id": "hsk2_0197",
    "char_idx": 0
  },
  "settings": {
    "audio_speed": 0.95,
    "tone_colors": true,
    "seasonal_atmosphere": true,
    "reveal_translation": false,
    "write_all_chars": true,
    "language": "en"
  }
}
```

- **`learner.start_date`** — never changes after first run; the anchor for "Day N" and for all heavenly-stem / 甲子 calculations.
- **`learner.start_offset`** — lets a learner skip forward ("I already know HSK 1, start me at HSK 2") without breaking the schedule; default 0.
- **`progress.words_seen`** — list of word IDs the learner has opened at least once. Basis for the Five-Colored Earth altar.
- **`progress.daily_pillar_completed`** — `{ shi, xie, xi }` booleans, reset on app load when the date changes.
- **`progress.completed_jiazi_cycles`** — incremented at personal Day 60, 120, 180...
- **`srs`** — full SRS deck as array of `SRSItem` objects (per spec §6.1).
- **`writing_cursor`** — `{ word_id, char_idx }`. Persists 写 phase position across reloads. Uses `word_id` (not day offset) so navigating between days doesn't leave stale cursor data. Only applies when current day's word matches the stored `word_id`.
- **`settings`** — audio speed, tone-color toggle, seasonal-töggle, reveal-translation toggle, write-all-chars toggle, language.

#### Why localStorage is sufficient

The `yueli` calendar needed AES-256-GCM encryption because it stores **encrypted personal events** — appointments, reminders, real sensitive data. HSK vocab progress is **not sensitive**: there is nothing embarrassing about which 500 Chinese words you know.

- **No password** — saves the entire account-recovery flow.
- **No server** — saves auth, sessions, GDPR data-residency, hosting costs.
- **No sync unless the learner wants it** — see §4.5.
- **State is ~5KB** — trivially small, fits many years of vocabulary progress.

---

### 4.5 Export / Import / Sync

Vocabulary schedules accumulate; losing 200 days of progress to a browser reset would be heartbreaking. So we ship **defense-in-depth**: three export options, each serving a different use case.

#### Option A — One-tap backup file (.json), MVP

A button in settings: `备份 · Backup`. Downloads a single `.json` file named `每日字-progress-YYYY-MM-DD.json`. No encryption — there is no sensitive content. Structure is the entire state object from §4.4 wrapped in a small envelope with `schema_version` and `exported_at`.

To restore: `恢复 · Restore` → file picker → state loaded into `localStorage`. Implementation cost: ~30 lines of code, ships in v1.

```json
{
  "schema": "mei-ri-zi/export",
  "schema_version": 1,
  "exported_at": "2026-05-04T18:22:00Z",
  "app_version": "1.0.0",
  "state": { /* the entire localStorage state object */ }
}
```

#### Option B — Sync URL, MVP — the genuinely novel one

A progress blob of ~5KB compresses to ~2KB. We can:

1. Serialize the state JSON to a string.
2. gzip to compress, then base64-encode the resulting bytes.
3. Put the resulting string as a **URL fragment**: `https://mei-ri-zi.app/#sync=<encoded-blob>`.
4. Learner saves this URL as their personal sync token — bookmark it, "Add to Home Screen" it, generate a QR code, email it to themselves.

To sync to a second device: open the URL once on the new device. The fragment loads the state into `localStorage`, the page reloads without the fragment, and you're caught up. The URL fragment is never sent to the server (everything after `#` is client-side only), so our own static host never sees the state — not even encrypted.

**Why this is genuinely good:**
- "Static-only" constraint honored: server still needs zero state.
- No account, no email, no password recovery flow.
- QR-code-shareable — print the QR, scan from a new phone, restored.
- No encryption — HSK vocabulary progress is not sensitive data. Skipping the encryption layer keeps the round-trip code simple (~20 lines) and removes the entire class of passphrase-loss / forgotten-password failure modes.
- Works offline after first load (state lives in localStorage once decoded).
- The fragment is durable: the same bookmark works for any future device.

This matches the *vitamin / personal ritual* aesthetic: your entire practice lives in one bookmark. Slip it in your wallet.

#### Option C — Printable甲子 celebration sheet (PDF), v2

A printable export that gives the learner a *tangible* record of progress — not as data, but as a ritual artifact. A one-page PDF showing:

- The learner's start date.
- Number of words seen, by HSK tier.
- Current HSK level and named Wu Xing color.
- The Five-Colored Earth altar, fully drawn, with completed tiers tinted and incomplete tiers outlined.
- A small sampling (6–9) of favorite or memorable characters from the journey, rendered large in serif type.
- The upcoming 7 daily words, in 米字格 (rice-grid) practice squares — usable for handwriting practice on paper.
- The 甲子 stamp (`甲子 #2 · 完成`) and date.

Generated entirely client-side with `jsPDF` or equivalent. A learner could print one per completed 甲子 (every 60 days) and watch their practice deepen on paper over a year. Deeply on-brand: this is the *letter from the app* celebrating the learner, not a sterile data dump.

#### Sync scenario matrix

| Scenario | Worked solution |
|----------|---------------|
| Same browser, daily use | `localStorage` (zero friction) |
| Cleared cookies / browser reset | Restore from last Backup `.json` (Option A) |
| New phone, same learner, one-time | Open the sync URL once (Option B), or restore `.json` (Option A) |
| Two devices, ongoing | Re-export sync URL after each session (small friction); or accept partial sync via Option C weekly PDFs |
| No data at all after a year | Nothing — there is nothing for a server to recover, because no server ever had it |

#### The honest limitation

Static-only means **no automatic background sync**. A learner using the app on phone and desktop without exchanging a sync URL will accumulate independent state on each device. This is a real limitation, and we surface it honestly in onboarding ("Vitamin progress lives on this device. Back up with the bookmark if you want it elsewhere") rather than hide it.

The trade-off is intentional: **privacy → simplicity → no-account friction**. A learner can start in under one second. No signup, no email, no password. That ritual cleanliness is part of the design philosophy — and the union of Option A + Option B means a lost-device scenario never forfeits real progress, as long as the learner created a sync URL or a backup file at least once.

If user demand warrants, **v3 can add** a tiny optional anonymous cloud sync layer (Cloudflare Workers KV storing state blobs keyed by a sync token, with TTL) — but the static app at its core never depends on it.

---

### 4.6 The Daily 识写习 Loop

The three pillars — **Card (识)**, **Writing (写)**, **Review (习)** — flow as a single daily sequence, not a free-floating menu. This preserves the "vitamin" feeling (one session, one sitting, ~5 minutes) while honoring the classical Chinese learning loop. The sequence label 识写习 comes from Confucius's 学而时习之 — "learn and practice it regularly" — which names the same cycle two thousand five hundred years ago.

#### Daily flow

```
Day N opens
│
├─ 识 Card (auto, ~2 min)
│   character · tone-colored pinyin · English · pos
│   example sentence (tap to reveal translation)
│   audio: 晓晓 (Edge TTS) · ▶ button
│   glyph breakdown (expandable)
│   [Skip to 写 →]   [Mark 会了 / 需要再背]
│
├─ 写 Writing (auto-advance or skip, ~2 min)
│   米字格 rice-grid canvas with hanzi-writer
│   [▶ 示范]  [✍ 临摹]  [👁 现出]
│   quiz result: ✓ 14/14 strokes  or  11/14
│   [Skip 写 →]   [Next →]
│
├─ 习 Review (only if SRS has due words, ~3 min)
│   1-4 due words — character first, then full reveal
│   character only (no pinyin, no meaning) → tap to reveal
│   revealed: pinyin + meaning + example sentence + audio
│   ▶ 听词 + ▶ 听例句 → then 会了 / 需要再背
│   [Skip 习 →]   [Done →]
│
└─ ✓ 今日完成
    streak +1 · 甲子 cycle +1
    五色土 altar notch fills
```

#### Skippability

Each pillar has a Skip button. Skipping 识 is unusual (why open the app?) but possible. Skipping 写 is common on busy days — the word is still recorded as "seen" and enrolled in SRS. Skipping 习 happens when there are no due words (common in the first week when the SRS queue is still filling).

#### SRS integration

- On opening 识 for the first time, the day's new word is auto-enrolled into SRS via `ensureEnrolled()` (insert-if-absent pattern from `xuehanyu`'s `srs.ts`). The word starts with `ease: 2.5, interval: 0, nextReview: now` — immediately "due" until its first real review.
- Completing the 习 phase calls `recordResults()` with the learner's 会了/需要再背 decisions. SM-2 adjusts ease and interval. The next review date is computed and stored.
- On subsequent days, the 习 phase pulls from `getDueItems()` — words where `nextReview <= now`. If no words are due, 习 is skipped automatically with a gentle "今日无复习" (No reviews due today) message.
- The writing quiz result (`totalMistakes` from hanzi-writer's `onComplete`) is stored alongside the SRS item as `lastWritingScore`. Low-mistake writing can bump ease slightly; high-mistake writing can flag the word for extra review.

#### Missed days

On return after missing 1+ calendar days, a gentle notice appears at the top of the card: "你没有打开每日字 2 天" ("You didn't open 每日字 for 2 days") with two buttons:
- **补上** (make up) — walks through those missed days sequentially, showing each day's 识 card but auto-skipping 写 and 习 (too many to catch up on). The learner still sees the words.
- **跳过** (jump) — advances straight to today's word. The missed days count as elapsed time in the personal timeline. No guilt, no penalty.

See spec.md §5.8 for the full catch-up state machine, including `catchup_days_remaining` lifecycle and the `cleanupCatchupState()` guard for interrupted sessions.

#### Navigation between days

Arrow keys (← →) or swipe move between calendar days. Each day shows its own 识→写→习 sequence. Home key jumps to today. The pattern is the same as `modern_chengyu`'s idioms navigation and `yueli`'s calendar navigation — consistent UX across your projects.

---

### 4.7 Writing with hanzi-writer

The 写 (Writing) phase is powered by [hanzi-writer](https://hanziwriter.org) v3.x — the same library already proven in `xuehanyu`'s `writing/page.tsx`. We port the core patterns to vanilla JS and add the 米字格 rice-grid background and Wu Xing stroke colors.

#### Two practice modes + reveal utility

**示范 (Demonstrate) — animate mode**
hanzi-writer's `animateCharacter()` draws each stroke in order, with the day's HSK level color as `strokeColor` (e.g., HSK 3 = 朱砂 vermillion `#c4452d`) and Wood green as `radicalColor` (`#4a9e8a`). Speed is controlled by `strokeAnimationSpeed: 1.2` and `delayBetweenStrokes: 300ms` — slower than xuehanyu's default, giving the learner time to watch each stroke. The 米字格 grid is drawn behind the strokes using hanzi-writer's SVG custom-background feature (the docs show exactly this pattern).

**临摹 (Trace) — quiz mode**
hanzi-writer's `quiz()` takes over. The learner traces strokes with mouse/touch/finger. Key settings (matching xuehanyu's proven values):
- `showHintAfterMisses: 3` — highlight the correct stroke after 3 misses
- `drawingColor`: the HSK level's accent color (the learner's trace is in the level's named pigment)
- `drawingWidth: 6` — generous, visible on mobile
- `highlightOnComplete: true` — character flashes on completion
- `highlightColor: '#50FA7B'` — green shimmer for success

Callbacks: `onCorrectStroke`, `onMistake`, `onComplete(totalMistakes)`. On completion, record `lastWritingScore` into the SRS state. The quiz result badge shows `✓ 14/14 strokes` or `11/14 — keep practicing!` — the same pattern xuehanyu uses.

**现出 (Show) — reveal utility**
`showCharacter()` reveals the full character if hidden. Not a practice mode — a helper for when the learner wants to study the character before attempting the quiz.

#### Multi-character words

HSK 2+ has many multi-character words (一起, 学校, 笔记本电脑). Hanzi-writer quizzes one character at a time. Our approach (matching xuehanyu's pattern):
- Each character in the word gets its own hanzi-writer instance
- Character dots below the canvas show progress (charIdx 0 → 1 → 2...)
- The active character is highlighted; completed characters are marked green
- Arrow keys or dots navigate between characters within the word
- After all characters are practiced, the 写 phase completes

A settings toggle "写所有字 / Write all characters" (default on) controls whether all characters are practiced or only the head character of compound words. This gives learners a quick option for busy days.

#### The 米字格 rice grid

The traditional practice grid for Chinese characters — 8 divisions formed by the horizontal, vertical, and diagonal lines of the character 米. Drawn as an SVG background behind the hanzi-writer canvas:

```svg
<svg width="200" height="200">
  <rect width="200" height="200" fill="none" stroke="#2A2A4A" stroke-width="1"/>
  <line x1="100" y1="0" x2="100" y2="200" stroke="#2A2A4A" stroke-width="0.5"/>
  <line x1="0" y1="100" x2="200" y2="100" stroke="#2A2A4A" stroke-width="0.5"/>
  <line x1="0" y1="0" x2="200" y2="200" stroke="#2A2A4A" stroke-width="0.5"/>
  <line x1="200" y1="0" x2="0" y2="200" stroke="#2A2A4A" stroke-width="0.5"/>
</svg>
```

This is one of hanzi-writer's documented examples — the library supports rendering into an existing SVG element directly.

#### Responsive canvas

xuehanyu's `writing/page.tsx` solves this well: a `ResizeObserver` on a wrapper div measures `clientWidth`, caps at 320px, and re-initializes hanzi-writer when the size changes. We port this exact pattern to vanilla JS.

#### Writing cursor persistence

xuehanyu persists the writing cursor (wordIdx, charIdx) per level so a reload resumes where the learner left off. We adapt this: persist `(word_id, charIdx)` in the state — using the word ID instead of day offset so navigation between days doesn't leave stale cursor data. Only applies when `writing_cursor.word_id` matches the current day's word.

---

### 4.8 xuehanyu — Reference Architecture

The project at `/home/ai/Projects/xuehanyu/` is a fully working Next.js 16 / React 19 HSK 1-6 learning platform. It is the proven reference for several of 每日字's core features. We port patterns from its TypeScript/React implementation to vanilla HTML/CSS/JS, and replace its Dracula dark-magenta aesthetic with our Wu Xing design system (inspired by Qinglu's dark-theme base architecture but with all custom tokens).

#### What we port from xuehanyu

| Feature | xuehanyu file | Port to | Notes |
|---------|---------------|---------|-------|
| SM-2 SRS algorithm | `src/lib/srs.ts` | `js/srs.js` | Same algorithm, same ease/clamp logic, same batch `recordResults()`. Add `lastWritingScore` field to `SRSItem`. |
| Writing page (hanzi-writer) | `src/app/writing/page.tsx` | 写 phase in `js/app.js` | Port the dynamic import, ResizeObserver canvas, animate/quiz/show controls, quiz result feedback, multi-char dots. Add 米字格 SVG background and Wu Xing stroke colors. |
| Export/Import JSON | `src/lib/progress.ts` (`exportAllData`/`importAllData`) | `js/progress.js` | Same `v: 1` schema pattern. Extend with personal timeline fields. |
| Progress tracking (streak, daily counters, bookmarks) | `src/lib/progress.ts` | `js/progress.js` | Same patterns. Adapt streak to use 甲子 cycle. Add `start_date`, `completed_jiazi_cycles`. |
| Writing cursor persistence | `src/lib/progress.ts` (`loadWritingCursor`/`saveWritingCursor`) | `js/progress.js` | Adapt to persist `(word_id, charIdx)` instead of `(level, wordIdx, charIdx)`. Uses word ID so cursor doesn't get stale when navigating between days. |
| Tone color palette | `src/components/ToneVisualizer.tsx` | CSS tone classes | xuehanyu's 4 colors (green/cyan/gold/red) are close to our Wu Xing mapping. We refine to 5 colors (Metal/Wood/Earth/Fire/Water) and add the neutral tone. |
| Speak button pattern | `src/components/SpeakButton.tsx` | Inline in `app.js` | Same UX: small circular button next to every Chinese text, plays audio on click. |
| Audio naming convention | `public/audio/` | `audio/word_audio/` | xuehanyu uses hex-encoded Unicode filenames. We use simpler `hsk2_0197/word.mp3` paths. |
| Daily word picker | `src/lib/daily.ts` | **NOT ported** | xuehanyu's picker is global (date-seeded hash). Our personal-timeline model (§4.4) is fundamentally different. |
| Server sync | `src/lib/sync.ts` | **NOT ported** | xuehanyu uses pull/push API with auth. We use the sync-URL pattern (§4.5) instead. No server needed. |
| Design system | `DESIGN.md` + Tailwind CSS | **NOT ported** | Completely different aesthetic. We use Wu Xing (Qinglu-inspired dark base, custom everything else). |

#### Why static HTML/CSS/JS instead of Next.js

xuehanyu needs Next.js because it has server-side routes (auth, sync API, data serving via `better-sqlite3`). 每日字 has no server. The entire app is a single `index.html` + `app.js` + `srs.js` + `progress.js` — no build step, no bundler, no node_modules. This matches the `modern_chengyu` architecture and keeps the app deployable to GitHub Pages with zero configuration.

The porting cost is real but manageable: React hooks become vanilla DOM manipulation; Tailwind classes become our custom CSS (inspired by Qinglu's variable architecture); `useSearchParams` becomes URL hash parsing; `next/dynamic` import becomes a plain `import()` call. The core logic (SM-2, hanzi-writer setup, progress tracking) is framework-agnostic.

---

## 5. Audio — Edge TTS

We use **Microsoft Edge TTS** with the **zh-CN-XiaoxiaoNeural (晓晓)** Chinese female voice — a free, high-quality neural TTS voice well-suited for language learning.

- **Voice:** `zh-CN-XiaoxiaoNeural` (晓晓)
- **Speed:** `0.95` (5% slower — better for language learners to catch each syllable)
- **Format:** MP3 (generated via the `edge-tts` Python library)
- **Cost:** Free (no API key needed; uses the same backend as the Edge browser "Read Aloud" feature)

Each word produces up to **three audio files** in `audio/word_audio/<hsk_level>/<word_id>/`:
1. `word.mp3` — the word itself, isolated (e.g., "一起")
2. `sentence.mp3` — the example sentence ("我们一起去学校。")
3. (optional) `breakdown.mp3` — the radical + component reading

The generate script (Python, ~`scripts/generate_audio.py`) walks `data/hsk_daily.json`, runs `edge-tts` once per file, saves into the structured directory, and writes a small `audio/index.json` mapping `(word_id, file)` → `relative_path`. The frontend loads audio paths from that index so we never request audio we don't have cached.

Because Edge TTS is free, we generate audio eagerly for all words in a single batch — no lazy generation needed. Unknown words simply show "audio 未生成" with a note that the batch generation script hasn't been run yet for that word.

---

## 6. Data

### 6.1 Source

The HSK 3.0 vocabulary list (10,896 words across 9 levels, finalized 2025 by China's Ministry of Education). We fetch an open-source JSON version (e.g., from `pinyin-club/HK-Vocab-List` or a similar CC-licensed GitHub repo). The `scripts/generate_data.py` script:

1. Downloads the HSK 3.0 word list (cached in `data/_cache/`)
2. Enriches each word with:
   - Pinyin (with tone numbers + tone marks) — generated via AI (LLM per word, context-aware for 多音字)
   - English translation — generated via AI (LLM per word)
   - Part of speech — generated via AI (LLM per word)
   - Radical + component breakdown — using the `Unihan` database or `hanzidentifier`
   - Stroke count — from Unihan
   - Example sentence — generated via AI (LLM per word, graded to HSK level)
3. Schedules one word per day **per level** (or in a recommended default order — see below)
4. Writes `data/hsk_daily.json` — the master file the frontend reads

### 6.2 Scheduling strategy

The default daily sequence follows the elemental cycle of progression — the learner walks through HSK 1 (all 300 words, ~300 days) before encountering HSK 2 words, and so on. But a learner can also:

- **Pick a level** ("Today I'm starting HSK 4") — the daily sequence jumps to HSK 4 entry #1, then walks HSK 4 sequentially
- **Start "from today"** — recommended for new users
- **Resume** — pick up where they left off

Sequence-per-level is just 0-indexed frequency ordering. Each level list is shuffled deterministically (seeded by the word's hash) so words don't come in pure-alphabetical order — feels more curated, but is reproducible.

### 6.3 Word object schema

```json
{
  "id": "hsk2_0197",
  "hsk_level": 2,
  "word": "一起",
  "pinyin_text": "yīqǐ",
  "pinyin_tones": [1, 3],
  "pinyin_parts": ["yī", "qǐ"],
  "pos": "adverb",
  "english": "together",
  "radicals": ["一", "走"],
  "components": [
    {"char": "一", "role": "semantic", "meaning": "one"},
    {"char": "起", "role": "compound", "meaning": "to rise", "breakdown": "走 (walk) + 己 (phonetic)"}
  ],
  "stroke_count": 14,
  "example": {
    "zh": "我们一起去学校。",
    "pinyin": "Wǒmen yīqǐ qù xuéxiào.",
    "pinyin_parts": ["Wǒ", "men", "yī", "qǐ", "qù", "xué", "xiào"],
    "pinyin_tones": [3, 0, 1, 3, 4, 2, 4],
    "en": "Let's go to school together."
  }
},
"meta": {
  "title": "每日字",
  "title_en": "Mei Ri Zi",
  "version": "1.0",
  "hsk_revision": "3.0 (2021)",
  "total_words": 10898,
  "levels": [...],
  "stems": ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
}
```

---

## 7. Tech Stack

- **Static site** — plain HTML + CSS + JS, no build step, no server (matches `modern_chengyu`'s architecture exactly)
- **Qinglu design system** — used as architectural guide for CSS variable organization
- **eight-flavors** (`../eight-flavors/`) — primary dark-mode design inspiration: scholar's ink-night palette (warm parchment `#f0e8d5` on deep ink `#0a0a14`), radial atmosphere glows, grain texture, gold accents. **All visual tokens, typography, and components are custom** to 每日字's Wu Xing identity (named pigments replace jade/azure; Ma Shan Zheng / Cormorant Garamond / Inter replace Noto fonts; all components built from scratch for the vitamin-card pattern)
- **localStorage** for all progress (streak, saved words, completed levels, settings)
- **Python 3.12 + venv** for the two generator scripts (`generate_data.py`, `generate_audio.py`)
- **Python libraries:** `requests`, `edge-tts` (audio generation only — data enrichment is handled by LLM directly)
- **Fonts:** Ma Shan Zheng (Chinese display — idiom/word characters, brush calligraphy), Noto Serif SC (Chinese body — examples, breakdown), Cormorant Garamond (English display and body — headings, translations, pinyin), Inter (UI — buttons, labels, nav). Same font stack as `yueli`.
- **Deploy:** GitHub Pages (static)

---

## 8. Project Structure

```
/home/ai/Projects/mei-ri-zi/
├── index.html                  # single entry, header + daily card + modals
├── js/
│   ├── app.js                   # daily scheduling, 识写习 flow, nav, favorites, search, audio
│   ├── srs.js                   # SM-2 spaced repetition (ported from xuehanyu srs.ts)
│   └── progress.js              # state tracking, streak, daily counters, export/import
├── css/
│   └── app.css                  # all styles — dark base, Wu Xing colors, tone colors, altar, card, writing canvas
├── data/
│   ├── hsk_daily.json           # generated — the master word list
│   ├── char_strokes/            # bundled hanzi-writer stroke data per character
│   ├── word_breakdown.json      # radical/component lookup, optional
│   └── _cache/                  # cache of downloaded HSK lists
├── audio/
│   ├── index.json               # word_id → audio paths
│   └── word_audio/
│       └── <hsk_level>_<id>/
│           ├── word.mp3
│           └── sentence.mp3
├── scripts/
│   ├── generate_data.py         # build hsk_daily.json from HSK 3.0 lists
│   └── generate_audio.py        # Edge TTS — voice zh-CN-XiaoxiaoNeural (晓晓)
├── README.md
├── spec.md                      # detailed handover spec, like yueli's
├── plan.md                      # this file
├── start.sh / restart.sh / stop.sh   # simple static-server helpers
└── LICENSE                      # MIT
```

---

## 9. Build Order

1. **Foundation** — create project files (index.html, css/, js/), write custom CSS starting from the scholar's ink-night palette (inspired by eight-flavors: deep ink `#0a0a14`, warm parchment `#f0e8d5`, elevated surfaces `#171a2e`, gold accent `#d4a93b`), build static skeleton HTML, add hanzi-writer CDN script tag
2. **Data pipeline** — `generate_data.py` downloads HSK 3.0 from `ivankra/hsk30` or `krmanik/HSK-3.0`, enriches with pinyin/breakdown/examples, writes `hsk_daily.json` (start with HSK 1–2 only for lean iteration)
3. **Progress & SRS modules** — port `progress.ts` and `srs.ts` from `xuehanyu` to vanilla JS. Establish personal-timeline model (§4.4): on first visit set `start_date`, compute "Day N" and heavenly-stem badge. Implement export/import JSON, streak tracking, daily counters.
4. **Skeleton app + 识 Card** — wire `index.html` + `app.js` to read `hsk_daily.json`, render the daily card with tone-colored pinyin, arrow-key nav, favorite, search, audio playback
5. **Cultural color system** — implement Wu Xing HSK palette, tone-colored pinyin CSS classes, five-colored earth mastery bar, heavenly-stem day badge, seasonal atmosphere
6. **写 Writing phase** — port hanzi-writer integration from `xuehanyu`'s `writing/page.tsx` to vanilla JS. Add 米字格 SVG background, Wu Xing stroke colors, responsive canvas (ResizeObserver), multi-char dots, quiz result feedback, writing cursor persistence
7. **习 Review phase** — wire `getDueItems()` from SRS module into the daily loop. Implement flash-recall cards (character only → tap to reveal → full details: pinyin + meaning + example sentence with tone-colored pinyin + audio buttons for word and sentence → 会了/需要再背). Auto-enroll daily words via `ensureEnrolled()`. Handle empty-queue case ("今日无复习").
8. **Audio pipeline** — `generate_audio.py` using Edge TTS (zh-CN-XiaoxiaoNeural), speed 0.95. Generate for HSK 1–2 first, then expand in a single batch. Wire audio index into the app.
9. **Backup & sync (Option A + B)** — one-tap backup `.json`, sync URL with base64-gzipped state in the URL fragment. Onboarding nudges learner to create a sync URL after their first session.
10. **Missed-day handling** — detect gaps, show "你没有打开每日字 N 天" notice, offer 补上/跳过 buttons
11. **Celebrations** — 甲子 completion (Yellow Dragon), HSK-level transitions (Four Symbols guardians)
12. **README + spec.md** — document the cultural systems deeply so a future reader (you, or another agent, or a contributor) understands why each color, name, and stem was chosen, not just what
13. **Polish pass** — typography, animations, accessibility, mobile
14. **Ship** — publish to GitHub Pages

---

## 10. Risks / Open Questions

- **HSK 3.0 data availability** — confirmed: `ivankra/hsk30` and `krmanik/HSK-3.0` both provide clean JSON with pinyin/POS/definitions. 10,896 words across 9 levels. Data risk closed.
- **Porting from xuehanyu (React/Next.js → vanilla JS)** — the core logic (SM-2, hanzi-writer setup, progress tracking) is framework-agnostic, but the port is non-trivial. React hooks become vanilla DOM manipulation; Tailwind becomes custom CSS (inspired by Qinglu's variable architecture). Mitigation: port one module at a time, test each in isolation.
- **Hanzi-writer data bundling** — we need stroke data for ~5,000 unique HSK characters. The `hanzi-writer-data` repo has per-character JSON files (~2KB each, ~10MB total). We bundle only the characters in `hsk_daily.json` to keep the app lightweight. The CDN fallback (hanzi-writer's default behavior) handles anything we don't bundle.
- **AI data quality** — all English translations, parts of speech, and example sentences are LLM-generated (one prompt per word). Requires a careful prompt with HSK-level-aware grading. Quality should be spot-checked across levels before shipping.
- **Edge TTS audio generation** — 10,896 words × 2 files = ~22K generations. Free to generate in a single batch; no per-request cost.
- **Cultural sensitivity audit** — before ship, run the color choices and any mythic imagery through the taboo checklist in the `traditional-chinese-design` skill. Specifically: never use green headwear motifs, never write names in red, never white-dominant celebrations.
- **Accessibility** — tone colors cannot be the only signal. Tone numbers and pinyin marks also always render. Colorblind-safe palette should be tested.
- **Tone color × HSK color conflicts** — pinyin sits on top of the HSK-tier-colored card accents. Carefully test contrast — the pinyin color is the primary signalizing channel; the HSK tier color is on the *card accent*, not behind the pinyin itself.
- **xuehanyu content scope** — xuehanyu covers HSK 1-6 from HSK Standard Course textbooks (lessons of 12 words, with dialogues and grammar). 每日字 uses HSK 3.0 (2021) with 9 levels and 10,896 words. The datasets overlap at HSK 1-6 but are structured differently. We don't reuse xuehanyu's content files; we build our own from the open HSK 3.0 lists.
- **HSK 7-9 tier length** — HSK 7-9 contains 5,562 words (~51% of the total). At one word per day, a learner would spend ~15 years in the Water tier alone. This is the correct progression per the HSK 3.0 standard, but consider subdividing hsk79 into three sub-atmospheres (HSK 7, 8, 9) in v2 so the learner experiences visual progression within the longest tier rather than a single Water atmosphere for over a decade.
- **Hanzi-writer stroke data** — the plan estimates ~5,000 unique characters at ~2KB each (~10MB bundled). The actual unique character count across HSK 3.0's 10,896 words (many multi-character compounds) should be verified against the dataset before committing to the bundle-everything approach. The CDN fallback in spec §5.5's `charDataLoader` handles any characters we don't bundle, so starting CDN-only and adding a bundle later is a viable strategy (no blocking dependency).

---

## 11. The "truly unique" credential

What makes this not-another-Chinese-themed-app:

1. **The Heavenly Stems count the days.** No Duolingo-style linear streak. The streak is a wheel that completes every 60 days as a 甲子 — and we honor that completion with the Yellow Dragon. This is hundreds of years of cultural literacy baked into the act of showing up daily.
2. **The five elements map the learning journey.** Wood-fire-earth-metal-water isn't a logo. It's why HSK 3 is red and HSK 6 is silver-blue. The learner physically walks the generative cycle from sprouting toward mastery.
3. **Tone colors are Wu Xing.** Reading pinyin is reading the five elements. Visual learning + cultural absorption + tone intuition — all in the same glance.
4. **The Five-Colored Earth altar is the progress bar.** Inspired by the 600-year-old 社稷坛 in Beijing. The bar at the bottom of every screen is literally the same soil colors the Ming emperor used to honor the harvest. Mastery is harvest.
5. **The seasons move through the page.** The 24 solar terms already run in `yueli`. We share that calendar code so the date system across both apps is coherent — a learner using both sees the same 立春 in the calendar and in the language of the day.
6. **Edge TTS 晓晓 tells the words.** A clear, natural Chinese female voice slowed by 5% — giving each word the clarity a learner needs without sacrificing warmth.

This is a Chinese literacy app that is Chinese — not Western-shaped with a Chinese lacquer on top.

---

## 12. Next step

When you approve this plan (or your edits to it), I'll write `spec.md` next, the longer-form design and engineering spec, then start building from foundation upward.
