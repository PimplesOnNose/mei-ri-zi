/* ============================================================
   SRS — SM-2 Spaced Repetition Algorithm
   ============================================================ */

/* SRSItem schema:
   {
     id: string,            // word ID e.g. "hsk1_0001"
     word: string,          // Chinese characters
     pinyin: string,        // pinyin with marks
     english: string,       // English meaning
     level: number,         // HSK level (1-9)
     ease: number,          // SM-2 ease factor, min 1.3
     interval: number,      // days until next review
     nextReview: number,    // timestamp (ms) of next review
     repetitions: number,   // consecutive correct reviews
     lastWritingScore: number | null // totalMistakes from last writing quiz
   }
*/

const SRS_DEFAULTS = {
  ease: 2.5,
  interval: 0,
  repetitions: 0,
  lastWritingScore: null
};

const MIN_EASE = 1.3;
const MS_PER_DAY = 86400000;
const MAX_REVIEWS_PER_SESSION = 4;

let srsCache = null;

/* ---- Load / Save ---- */
function loadSRS() {
  if (srsCache) return srsCache;
  try {
    const raw = STORAGE.get('mei-ri-zi/srs');
    srsCache = raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.warn('Failed to load SRS data:', e);
    srsCache = [];
  }
  return srsCache;
}

function saveSRS(items) {
  srsCache = items;
  try {
    STORAGE.set('mei-ri-zi/srs', JSON.stringify(items));
  } catch (e) {
    console.warn('Failed to save SRS data:', e);
  }
}

/* ---- Ensure Enrolled (insert-if-absent) ---- */
function ensureEnrolled(words) {
  const items = loadSRS();
  const known = new Set(items.map(i => i.id));
  let changed = false;

  for (const w of words) {
    if (known.has(w.id)) continue;
    items.push({
      id: w.id,
      word: w.word,
      pinyin: w.pinyin_text || '',
      english: w.english || '',
      level: w.hsk_level || 1,
      ease: SRS_DEFAULTS.ease,
      interval: SRS_DEFAULTS.interval,
      nextReview: Date.now(),  // immediately due on first enrollment
      repetitions: SRS_DEFAULTS.repetitions,
      lastWritingScore: SRS_DEFAULTS.lastWritingScore
    });
    known.add(w.id);
    changed = true;
  }

  if (changed) saveSRS(items);
  return items;
}

/* ---- Get Due Items ---- */
function getDueItems() {
  const now = Date.now();
  const items = loadSRS();
  return items
    .filter(item => item.nextReview <= now)
    .sort((a, b) => a.nextReview - b.nextReview)
    .slice(0, MAX_REVIEWS_PER_SESSION);
}

/* ---- Record Result (SM-2 core) ---- */
/*
  quality: 1 = "需要再背" (need to revisit)
           4 = "会了" (I remember)
*/
function recordResult(wordId, quality) {
  const items = loadSRS();
  const idx = items.findIndex(i => i.id === wordId);
  if (idx === -1) return null;

  const item = items[idx];

  if (quality >= 3) {
    // Correct response
    item.repetitions += 1;
    if (item.repetitions === 1) {
      item.interval = 1;
    } else if (item.repetitions === 2) {
      item.interval = 6;
    } else {
      item.interval = Math.round(item.interval * item.ease);
    }
  } else {
    // Incorrect response — reset
    item.repetitions = 0;
    item.interval = 1;
  }

  // Update ease factor
  item.ease = Math.max(MIN_EASE, item.ease + (0.1 - (5 - quality) * 0.08));

  // Set next review date
  item.nextReview = Date.now() + item.interval * MS_PER_DAY;

  items[idx] = item;
  saveSRS(items);

  return item;
}

/* ---- Record Writing Score ---- */
function recordWritingScore(wordId, totalMistakes) {
  const items = loadSRS();
  const idx = items.findIndex(i => i.id === wordId);
  if (idx === -1) return;

  items[idx].lastWritingScore = totalMistakes;
  saveSRS(items);
}

/* ---- Get Item by ID ---- */
function getSRSItem(wordId) {
  const items = loadSRS();
  return items.find(i => i.id === wordId) || null;
}

/* ---- Due Count ---- */
function getDueCount() {
  const now = Date.now();
  const items = loadSRS();
  return items.filter(item => item.nextReview <= now).length;
}
