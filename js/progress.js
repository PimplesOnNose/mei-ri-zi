/* ============================================================
   Progress — State tracking, personal timeline, export/import
   ============================================================ */

/* ---- Storage abstraction (with memory fallback) ---- */
const STORAGE = (() => {
  let memory = {};
  let available = false;
  try {
    localStorage.setItem('__test__', '1');
    localStorage.removeItem('__test__');
    available = true;
  } catch (e) {}

  function get(key) {
    if (available) { try { return localStorage.getItem(key); } catch (e) {} }
    return memory[key] ?? null;
  }

  function set(key, value) {
    if (available) { try { localStorage.setItem(key, value); return; } catch (e) {} }
    memory[key] = String(value);
  }

  function remove(key) {
    if (available) { try { localStorage.removeItem(key); return; } catch (e) {} }
    delete memory[key];
  }

  return { get, set, remove };
})();

/* ============================================================
   Constants
   ============================================================ */

const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
const STEM_ELEMENTS  = ['木', '木', '火', '火', '土', '土', '金', '金', '水', '水'];
const STEM_COLORS    = ['#4a9e8a', '#4a9e8a', '#c4452d', '#c4452d', '#c9a96e', '#c9a96e', '#8faacc', '#8faacc', '#3a6e8e', '#3a6e8e'];

const STATE_KEY   = 'mei-ri-zi/state';
const STREAK_KEY  = 'mei-ri-zi/streak';
const DAILY_KEY   = 'mei-ri-zi/daily';
const VERSION_KEY = 'mei-ri-zi/version';

const STATE_VERSION = 1;

/* Default state for a first-time learner */
function defaultState() {
  const today = getLocalDate();
  return {
    version: STATE_VERSION,
    schema: 'mei-ri-zi/state',
    created_at: new Date().toISOString(),
    learner: {
      start_date: today,
      start_offset: 0,
      timezone: 'auto'
    },
    progress: {
      last_opened_date: today,
      words_seen: [],
      completed_jiazi_cycles: 0,
      daily_pillar_completed: { shi: false, xie: false, xi: false },
      // catchup_days_remaining is transient — set only during catch-up
    },
    favorites: [],
    writing_cursor: {
      word_id: null,
      char_idx: 0
    },
    settings: {
      audio_speed: 0.95,
      tone_colors: true,
      seasonal_atmosphere: true,
      reveal_translation: false,
      write_all_chars: true,
      language: 'en'
    }
  };
}

/* ============================================================
   Personal Timeline
   ============================================================ */

function getLocalDate() {
  return new Date().toLocaleDateString('sv-SE');  // "YYYY-MM-DD" in local tz
}

function dateDiffInDays(dateA, dateB) {
  const a = new Date(dateA + 'T00:00:00');
  const b = new Date(dateB + 'T00:00:00');
  return Math.floor((b - a) / 86400000);
}

function getDayOffset(state) {
  const today = getLocalDate();
  const startDate = state.learner.start_date;
  const daysDiff = dateDiffInDays(startDate, today);
  return Math.max(0, daysDiff + state.learner.start_offset);
}

/* ============================================================
   Heavenly Stem Badge
   ============================================================ */

function getStemBadge(dayOffset) {
  const stemIndex = dayOffset % 10;
  const weekNumber = Math.floor(dayOffset / 10) + 1;
  return {
    stem: HEAVENLY_STEMS[stemIndex],
    week: weekNumber,
    label: `${HEAVENLY_STEMS[stemIndex]}·初${weekNumber}`,
    element: STEM_ELEMENTS[stemIndex],
    color: STEM_COLORS[stemIndex]
  };
}

/* ============================================================
   HSK Level Resolution
   ============================================================ */

const LEVEL_BOUNDARIES = [
  { level: 'hsk1',  start: 0,    end: 496 },
  { level: 'hsk2',  start: 497,  end: 1257 },
  { level: 'hsk3',  start: 1258, end: 2223 },
  { level: 'hsk4',  start: 2224, end: 3216 },
  { level: 'hsk5',  start: 3217, end: 4283 },
  { level: 'hsk6',  start: 4284, end: 5416 },
  { level: 'hsk79', start: 5417, end: 11031 }
];

function getHSKLevel(dayOffset) {
  for (const b of LEVEL_BOUNDARIES) {
    if (dayOffset >= b.start && dayOffset <= b.end) return b;
  }
  return LEVEL_BOUNDARIES[LEVEL_BOUNDARIES.length - 1];
}

function getHSKLevelNum(dayOffset) {
  const level = getHSKLevel(dayOffset);
  const map = { 'hsk1': 1, 'hsk2': 2, 'hsk3': 3, 'hsk4': 4,
                'hsk5': 5, 'hsk6': 6, 'hsk79': 7 };
  return map[level.level] || 0;
}

/* Tier mapping for Five-Colored Earth */
function levelToTier(hskLevel) {
  if (hskLevel <= 2) return 'wood';
  if (hskLevel <= 4) return 'fire';
  if (hskLevel === 5) return 'earth';
  if (hskLevel === 6) return 'metal';
  return 'water';
}

/* ============================================================
   State CRUD
   ============================================================ */

let stateCache = null;

function loadState() {
  if (stateCache) return stateCache;

  try {
    const raw = STORAGE.get(STATE_KEY);
    if (raw) {
      stateCache = JSON.parse(raw);
      // Run migrations if needed
      if (stateCache.version < STATE_VERSION) {
        stateCache = migrateState(stateCache, STATE_VERSION);
        saveStateInternal(stateCache);
      }
      return stateCache;
    }
  } catch (e) {
    console.warn('Failed to load state, starting fresh:', e);
  }

  // First visit
  stateCache = defaultState();
  saveStateInternal(stateCache);
  return stateCache;
}

function saveStateInternal(state) {
  try {
    STORAGE.set(STATE_KEY, JSON.stringify(state));
  } catch (e) {
    console.warn('Failed to save state:', e);
  }
}

/* Debounced save for rapid interactions */
let saveTimer = null;
function saveState() {
  if (saveTimer) clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    if (stateCache) saveStateInternal(stateCache);
    saveTimer = null;
  }, 300);
}

/* Flush on beforeunload — wired in app.js */
function flushState() {
  if (saveTimer) {
    clearTimeout(saveTimer);
    saveTimer = null;
  }
  if (stateCache) saveStateInternal(stateCache);
}

/* Migration framework */
const MIGRATIONS = {
  // version 0 → 1: add writing_cursor
  0: (state) => {
    state.writing_cursor = { word_id: null, char_idx: 0 };
    return state;
  }
};

function migrateState(state, targetVersion) {
  while ((state.version || 0) < targetVersion) {
    const currentVer = state.version || 0;
    if (MIGRATIONS[currentVer]) {
      state = MIGRATIONS[currentVer](state);
    }
    state.version = (state.version || 0) + 1;
  }
  return state;
}

/* ============================================================
   Streak Management
   ============================================================ */

function loadStreak() {
  try {
    const raw = STORAGE.get(STREAK_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) {}
  return { last_active_date: '', current_streak: 0, longest_streak: 0 };
}

function saveStreak(streak) {
  try {
    STORAGE.set(STREAK_KEY, JSON.stringify(streak));
  } catch (e) {
    console.warn('Failed to save streak:', e);
  }
}

function updateStreak() {
  const today = getLocalDate();
  const streak = loadStreak();
  const lastDate = streak.last_active_date;

  if (lastDate === today) return streak; // already counted today

  const diff = lastDate ? dateDiffInDays(lastDate, today) : 1;

  if (diff === 1) {
    // Consecutive day
    streak.current_streak += 1;
  } else if (diff > 1) {
    // Missed days — reset streak
    streak.current_streak = 0;
  } else if (!lastDate) {
    // First ever activity
    streak.current_streak = 1;
  }

  streak.last_active_date = today;
  if (streak.current_streak > streak.longest_streak) {
    streak.longest_streak = streak.current_streak;
  }

  saveStreak(streak);
  return streak;
}

/* ============================================================
   Daily Activity Counter
   ============================================================ */

function loadDaily() {
  try {
    const raw = STORAGE.get(DAILY_KEY);
    if (raw) {
      const data = JSON.parse(raw);
      if (data.date === getLocalDate()) return data;
    }
  } catch (e) {}
  return { date: getLocalDate(), new_words: 0, reviews_done: 0, writing_chars: 0, pillar_completions: 0 };
}

function saveDaily(daily) {
  try {
    STORAGE.set(DAILY_KEY, JSON.stringify(daily));
  } catch (e) {}
}

function incrementDaily(field) {
  const daily = loadDaily();
  daily[field] = (daily[field] || 0) + 1;
  saveDaily(daily);
}

/* ============================================================
   甲子 Completion Check
   ============================================================ */

function checkJiaziCompletion(state, dayOffset) {
  // Day 60 → offset 59 → (59 + 1) % 60 == 0
  if (dayOffset > 0 && (dayOffset + 1) % 60 === 0) {
    state.progress.completed_jiazi_cycles = (state.progress.completed_jiazi_cycles || 0) + 1;
    saveState();
    return true;
  }
  return false;
}

/* ============================================================
   Five-Colored Earth Altar
   ============================================================ */

/* Tier word count derived from LEVEL_BOUNDARIES */
function tierWordCount(tierLevels) {
  let total = 0;
  for (const b of LEVEL_BOUNDARIES) {
    if (tierLevels.includes(b.level) && b.start >= 0) {
      total += (b.end - b.start + 1);
    }
  }
  return total;
}

const TIER_CONFIG = {
  wood:  { levels: ['hsk1', 'hsk2'],     color: '--altar-east' },
  fire:  { levels: ['hsk3', 'hsk4'],     color: '--altar-south' },
  earth: { levels: ['hsk5'],             color: '--altar-center' },
  metal: { levels: ['hsk6'],             color: '--altar-west' },
  water: { levels: ['hsk79'],            color: '--altar-north' }
};

/* Pre-computed word-to-tier map */
let wordTierMap = null;

function ensureTierMap(hskDaily) {
  if (wordTierMap) return;
  wordTierMap = {};
  for (const word of hskDaily.words) {
    wordTierMap[word.id] = levelToTier(word.hsk_level || 1);
  }
}

function getAltarState(wordsSeen) {
  const tiers = {};
  for (const [name, config] of Object.entries(TIER_CONFIG)) {
    tiers[name] = {
      seen: 0,
      total: tierWordCount(config.levels),
      color: config.color
    };
  }

  // Count seen words per tier
  for (const wordId of wordsSeen) {
    const tier = wordTierMap ? wordTierMap[wordId] : null;
    if (tier && tiers[tier]) {
      tiers[tier].seen += 1;
    }
  }

  return tiers;
}

/* ============================================================
   Missed-Day Detection
   ============================================================ */

function detectMissedDays(state) {
  const today = getLocalDate();
  const lastVisit = state.progress.last_opened_date;
  if (!lastVisit) return 0;
  const daysMissed = dateDiffInDays(lastVisit, today) - 1;
  return Math.max(0, daysMissed);
}

function cleanupCatchupState(state) {
  if (state.progress.catchup_days_remaining !== undefined) {
    delete state.progress.catchup_days_remaining;
  }
}

/* ============================================================
   Solar Terms (二十四节气)
   ============================================================ */

const SOLAR_TERMS = [
  { name: '立春', en: 'Start of Spring',   month: 2,  day: 4,  temp: 0.1 },
  { name: '雨水', en: 'Rain Water',        month: 2,  day: 19, temp: 0.15 },
  { name: '惊蛰', en: 'Awakening of Insects', month: 3, day: 6, temp: 0.2 },
  { name: '春分', en: 'Spring Equinox',    month: 3,  day: 21, temp: 0.3 },
  { name: '清明', en: 'Clear and Bright',  month: 4,  day: 5,  temp: 0.35 },
  { name: '谷雨', en: 'Grain Rain',        month: 4,  day: 20, temp: 0.4 },
  { name: '立夏', en: 'Start of Summer',   month: 5,  day: 6,  temp: 0.5 },
  { name: '小满', en: 'Grain Buds',        month: 5,  day: 21, temp: 0.6 },
  { name: '芒种', en: 'Grain in Ear',      month: 6,  day: 6,  temp: 0.7 },
  { name: '夏至', en: 'Summer Solstice',   month: 6,  day: 21, temp: 0.8 },
  { name: '小暑', en: 'Minor Heat',        month: 7,  day: 7,  temp: 0.75 },
  { name: '大暑', en: 'Major Heat',        month: 7,  day: 23, temp: 0.7 },
  { name: '立秋', en: 'Start of Autumn',   month: 8,  day: 7,  temp: 0.6 },
  { name: '处暑', en: 'End of Heat',       month: 8,  day: 23, temp: 0.5 },
  { name: '白露', en: 'White Dew',         month: 9,  day: 8,  temp: 0.4 },
  { name: '秋分', en: 'Autumnal Equinox',  month: 9,  day: 23, temp: 0.35 },
  { name: '寒露', en: 'Cold Dew',          month: 10, day: 8,  temp: 0.3 },
  { name: '霜降', en: 'Frost\'s Descent',  month: 10, day: 23, temp: 0.25 },
  { name: '立冬', en: 'Start of Winter',   month: 11, day: 7,  temp: 0.15 },
  { name: '小雪', en: 'Minor Snow',        month: 11, day: 22, temp: 0.1 },
  { name: '大雪', en: 'Major Snow',        month: 12, day: 7,  temp: 0.05 },
  { name: '冬至', en: 'Winter Solstice',   month: 12, day: 22, temp: 0.0 },
  { name: '小寒', en: 'Minor Cold',        month: 1,  day: 6,  temp: 0.02 },
  { name: '大寒', en: 'Major Cold',        month: 1,  day: 20, temp: 0.05 }
];

function getCurrentSolarTerm() {
  const now = new Date();
  const todayMD = now.getMonth() * 100 + now.getDate();

  let lastTerm = null;
  for (const term of SOLAR_TERMS) {
    const termMD = term.month * 100 + term.day;
    if (termMD <= todayMD) {
      lastTerm = term;
    }
  }

  // If today is before 立春 (Jan 1 – Feb 3), return 大寒
  return lastTerm || SOLAR_TERMS[SOLAR_TERMS.length - 1];
}

/* ============================================================
   Export / Import
   ============================================================ */

function exportBackup() {
  const state = loadState();
  const blob = {
    schema: 'mei-ri-zi/export',
    schema_version: 1,
    app_version: '1.0.0',
    exported_at: new Date().toISOString(),
    state: state
  };
  const json = JSON.stringify(blob, null, 2);
  const filename = `每日字-progress-${getLocalDate()}.json`;

  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([json], { type: 'application/json' }));
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}

function importBackup(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const blob = JSON.parse(e.target.result);
        if (blob.schema !== 'mei-ri-zi/export' || !blob.state) {
          reject(new Error('Invalid backup file: wrong schema'));
          return;
        }
        stateCache = blob.state;
        saveStateInternal(stateCache);
        resolve(true);
      } catch (err) {
        reject(new Error('Failed to parse backup: ' + err.message));
      }
    };
    reader.onerror = () => reject(new Error('Failed to read file'));
    reader.readAsText(file);
  });
}

function createSyncURL() {
  const state = loadState();
  const json = JSON.stringify(state);

  try {
    // Compress with pako (loaded from CDN)
    const compressed = window.pako ? pako.gzip(json) : new TextEncoder().encode(json);
    const bytes = new Uint8Array(compressed);
    let binary = '';
    for (let i = 0; i < bytes.length; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    const encoded = btoa(binary);
    const url = `${location.origin}${location.pathname}#sync=${encoded}`;
    return url;
  } catch (e) {
    console.error('Failed to create sync URL:', e);
    return null;
  }
}

function loadSyncURL() {
  const hash = location.hash;
  if (!hash.startsWith('#sync=')) return false;

  const encoded = hash.slice(6);
  try {
    const binary = atob(encoded);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }

    let json;
    if (window.pako) {
      json = pako.ungzip(bytes, { to: 'string' });
    } else {
      json = new TextDecoder().decode(bytes);
    }

    const state = JSON.parse(json);
    stateCache = state;
    saveStateInternal(state);
    location.hash = '';
    return true;
  } catch (e) {
    console.error('Failed to load sync URL:', e);
    alert('同步链接无效 / Invalid sync URL');
    return false;
  }
}

/* ============================================================
   Word helpers
   ============================================================ */

function renderToneColoredPinyin(pinyinParts, pinyinTones) {
  if (!pinyinParts || !pinyinTones) return '';
  return pinyinParts.map((part, i) => {
    const tone = pinyinTones[i] !== undefined ? pinyinTones[i] : 0;
    return `<span class="tone-${tone}">${escHtml(part)}</span>`;
  }).join(' ');
}

function escHtml(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}
