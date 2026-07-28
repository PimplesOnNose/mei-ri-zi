/* ============================================================
   每日字 · Měi Rì Zì — Main Application
   ============================================================ */

/* ---- State ---- */
let HSK_DATA = null;         // hsk_daily.json
let AUDIO_INDEX = null;      // audio/index.json
let currentDayOffset = 0;    // 0-indexed from learner's personal timeline
let currentWord = null;      // today's word object
let currentPhase = 'shi';    // 'shi' | 'xie' | 'xi' | 'complete'
let currentAudio = null;     // active Audio instance
let currentWriter = null;    // active hanzi-writer instance
let currentCharIdx = 0;      // for multi-char words in 写 phase
let reviewQueue = [];        // due SRS items for 习 phase
let reviewIdx = 0;
let DATA_INDEX = null;       // level index for per-level loading           // current position in reviewQueue
let catchupMode = false;     // true when walking through missed days

/* ---- DOM References ---- */
const $ = (id) => document.getElementById(id);

const dom = {
  stemBadge:      $('stem-badge'),
  solarTerm:      $('solar-term'),
  dayLabel:       $('day-label'),
  favBtn:         $('fav-btn'),
  wordChar:       $('word-char'),
  wordPinyin:     $('word-pinyin'),
  wordMeta:       $('word-meta'),
  exampleSection: $('example-section'),
  exampleZh:      $('example-zh'),
  examplePinyin:  $('example-pinyin'),
  exampleEn:      $('example-en'),
  glyphSection:   $('glyph-section'),
  glyphBreakdown: $('glyph-breakdown'),
  btnPlayWord:    $('btn-play-word'),
  btnPlaySentence: $('btn-play-sentence'),
  audioUnavail:   $('audio-unavailable'),
  sentenceAudioUnavail: $('sentence-audio-unavailable'),
  navPrev:        $('nav-prev'),
  navToday:       $('nav-today'),
  navNext:        $('nav-next'),

  // Missed notice
  missedNotice:   $('missed-notice'),
  missedCount:    $('missed-count'),
  btnCatchUp:     $('btn-catch-up'),
  btnSkipAhead:   $('btn-skip-ahead'),
  catchupBadge:   $('catchup-badge'),

  // Pillar tabs
  pillarTabs:     $('pillar-tabs'),

  // Phases
  phaseShi:       $('phase-shi'),
  phaseXie:       $('phase-xie'),
  phaseXi:        $('phase-xi'),
  phaseComplete:  $('phase-complete'),

  // 识 phase
  btnShiContinue: $('btn-shi-continue'),
  btnShiSkip:     $('btn-shi-skip'),

  // 写 phase
  writingCharLabel: $('writing-char-label'),
  writingCanvas:  $('writing-canvas-wrapper'),
  writingProgress:  $('writing-progress'),
  writingResult:    $('writing-result'),
  btnAnimate:     $('btn-animate'),
  btnTrace:       $('btn-quiz'),
  btnShow:        $('btn-show'),
  btnCharPrev:    $('btn-char-prev'),
  btnCharNext:    $('btn-char-next'),
  btnXieContinue: $('btn-xie-continue'),
  btnXieSkip:     $('btn-xie-skip'),

  // 习 phase
  reviewSection:  $('review-section'),
  reviewEmpty:    $('review-empty'),
  reviewCards:    $('review-cards'),
  btnXiDone:      $('btn-xi-done'),
  btnXiSkip:      $('btn-xi-skip'),

  // Completion
  stampStreak:    $('stamp-streak'),
  stampStem:      $('stamp-stem'),

  // Altar
  altarWood:      $('altar-wood-fill'),
  altarFire:      $('altar-fire-fill'),
  altarEarth:     $('altar-earth-fill'),
  altarMetal:     $('altar-metal-fill'),
  altarWater:     $('altar-water-fill'),

  // Modals
  searchModal:    $('search-modal'),
  searchInput:    $('search-input'),
  searchFilters:  $('search-filters'),
  searchResults:  $('search-results'),
  favoritesModal: $('favorites-modal'),
  favoritesList:  $('favorites-list'),
  settingsModal:  $('settings-modal'),
  btnQuizHeader:  $('btn-quiz-header'),
  btnSearch:      $('btn-search'),
  btnFavorites:   $('btn-favorites'),
  btnSettings:    $('btn-settings'),

  // Quiz
  quizModal:      $('quiz-modal'),
  quizQuestion:   $('quiz-question'),
  quizOptions:    $('quiz-options'),
  quizResult:     $('quiz-result'),
  quizStats:      $('quiz-stats'),
  quizNext:       $('quiz-next'),
  quizDone:       $('quiz-done'),
  quizSummary:    $('quiz-summary'),
  quizScore:      $('quiz-score'),
  quizResultsList: $('quiz-results-list'),
  quizClose:      $('quiz-close'),

  // Settings
  settingToneColors:    $('setting-tone-colors'),
  settingSeasonal:      $('setting-seasonal'),
  settingWriteAll:      $('setting-write-all'),
  settingAudioSpeed:    $('setting-audio-speed'),
  settingLanguage:      $('setting-language'),
  settingStartLevel:    $('setting-start-level'),
  btnBackup:      $('btn-backup'),
  btnRestore:     $('btn-restore'),
  btnSyncUrl:     $('btn-sync-url'),

  // Celebration
  celebrationOverlay: $('celebration-overlay'),
  celebrationSvg:     $('celebration-svg'),
  celebrationTitle:   $('celebration-title'),
  celebrationBody:    $('celebration-body'),
  celebrationContinue: $('celebration-continue'),
};

/* ============================================================
   Initialization
   ============================================================ */

async function init() {
  // Load state
  const state = loadState();
  const today = getLocalDate();

  // Check for sync URL on first load
  if (location.hash && location.hash.startsWith('#sync=')) {
    const loaded = loadSyncURL();
    if (loaded) {
      // State was replaced; reload references
      location.reload();
      return;
    }
  }

  // Reset daily pillars if new day
  if (state.progress.last_opened_date !== today) {
    state.progress.daily_pillar_completed = { shi: false, xie: false, xi: false };
    state.progress.last_opened_date = today;
    saveState();
  }

  // Clean up any stale catch-up state
  cleanupCatchupState(state);
  saveState();

  // Load audio index (tiny, always load first)
  try {
    const resp = await fetch('audio/index.json');
    AUDIO_INDEX = await resp.json();
  } catch (e) {
    AUDIO_INDEX = { files: {} };
  }

  // Wire events FIRST so all buttons work immediately
  wireEvents();

  // Load vocabulary data — try per-level files first, fall back to monolithic
  const dayOffset = getDayOffset(state);
  
  // Find which level this day belongs to
  let loadLevel = 'hsk1';
  for (const b of LEVEL_BOUNDARIES) {
    if (dayOffset >= b.start && dayOffset <= b.end) {
      loadLevel = b.level;
      break;
    }
  }
  
  // Try per-level load
  try {
    const resp = await fetch(`data/levels/${loadLevel}.json`);
    if (resp.ok) {
      const levelData = await resp.json();
      levelData._level = loadLevel;
      HSK_DATA = levelData;
      // Load level index for navigation metadata
      try {
        const idxResp = await fetch('data/index.json');
        DATA_INDEX = await idxResp.json();
      } catch (e) { DATA_INDEX = null; }
    } else {
      throw new Error('Level file not found');
    }
  } catch (e) {
    // Fall back to monolithic file
    try {
      const resp = await fetch('data/hsk_daily.json');
      HSK_DATA = await resp.json();
    } catch (err) {
      showError('Failed to load vocabulary data', err);
      return;
    }
  }

  // Pre-compute tier map from the data index (always has all levels)
  if (DATA_INDEX) {
    wordTierMap = {};
    for (const [lk, li] of Object.entries(DATA_INDEX.levels)) {
      const levelNum = parseInt(lk.replace('hsk','').replace('79','7'));
      // We don't have individual word IDs, so we approximate by level
      // The altar counts words_seen per tier, which works with IDs from any source
    }
  }
  ensureTierMap(HSK_DATA);

  // Restore writing cursor if valid
  if (state.writing_cursor && state.writing_cursor.word_id) {
    currentCharIdx = state.writing_cursor.char_idx || 0;
  }

  // Update altar
  updateAltar();

  // Update seasonal atmosphere
  applySeasonalAtmosphere(state);

  // Get current day
  currentDayOffset = getDayOffset(state);
  loadDay(currentDayOffset);

  // Detect missed days AFTER loading current day
  const daysMissed = detectMissedDays(state);
  if (daysMissed > 0) {
    showMissedNotice(daysMissed);
  }

  // First-visit onboarding
  checkFirstVisit(state);

  // Hide loading screen, show app
  const loadingEl = document.getElementById('loading-screen');
  if (loadingEl) {
    loadingEl.classList.add('fade-out');
    setTimeout(() => {
      loadingEl.style.display = 'none';
      document.getElementById('app').hidden = false;
    }, 400);
  } else {
    document.getElementById('app').hidden = false;
  }

  // Schedule state flush on page unload
  window.addEventListener('beforeunload', flushState);
}

/* ---- Load a specific day ---- */
async function loadDay(dayOffset) {
  const state = loadState();
  
  // Convert global dayOffset to local index within the correct level
  let localIdx = dayOffset;
  
  if (DATA_INDEX) {
    // Find which level this day belongs to
    let targetLevel = null;
    let levelStart = 0;
    for (const [lk, li] of Object.entries(DATA_INDEX.levels)) {
      const start = li.start_offset;
      const end = start + li.word_count - 1;
      if (dayOffset >= start && dayOffset <= end) {
        targetLevel = lk;
        levelStart = start;
        break;
      }
    }
    
    if (targetLevel) {
      localIdx = dayOffset - levelStart;
      
      // Load this level's data if we don't have it
      if (!HSK_DATA || !HSK_DATA._level || HSK_DATA._level !== targetLevel) {
        try {
          const resp = await fetch(`data/levels/${targetLevel}.json`);
          if (resp.ok) {
            const levelData = await resp.json();
            levelData._level = targetLevel;
            HSK_DATA = levelData;
            ensureTierMap(HSK_DATA);
          }
        } catch (e) { /* fall through */ }
      }
    }
  }
  
  const words = HSK_DATA ? HSK_DATA.words : [];
  if (localIdx < 0 || localIdx >= words.length) {
    showCompletionMessage();
    return;
  }

  currentWord = words[localIdx];
  currentDayOffset = dayOffset;

  // Apply HSK level theme color
  document.body.className = document.body.className
    .replace(/level-\d+/g, '')
    .trim();
  const level = currentWord ? currentWord.hsk_level : 1;
  document.body.classList.add('level-' + Math.min(level, 7));

  // Update header
  updateHeader(dayOffset);

  // Render 识 card
  renderCard(currentWord);

  // Reset 写 phase state
  currentCharIdx = 0;
  clearWriter();

  // Start at 识 phase
  showPhase('shi');

  // Check if 识 was already completed today
  if (state.progress.daily_pillar_completed.shi) {
    // Show 写 phase or beyond
    if (state.progress.daily_pillar_completed.xie) {
      startReviewPhase();
    } else {
      showPhase('xie');
    }
  }

  // Update fav button
  updateFavButton();

  // Check for level transition celebration
  checkLevelTransition(dayOffset);

  // Show or hide catch-up badge
  dom.catchupBadge.hidden = !catchupMode;

  // In catch-up mode, show progress & auto-register word as seen
  // Catch-up shows 识 cards only — no writing or review
  if (catchupMode) {
    const s = loadState();
    const remaining = s.progress.catchup_days_remaining;
    if (remaining !== undefined) {
      dom.dayLabel.textContent = `补 Day ${dayOffset + 1} (剩余 ${remaining})`;
    }
    // Auto-enroll in SRS and mark as seen
    ensureEnrolled([currentWord]);
    if (!state.progress.words_seen.includes(currentWord.id)) {
      state.progress.words_seen.push(currentWord.id);
    }
    state.progress.daily_pillar_completed.shi = true;
    state.progress.daily_pillar_completed.xie = true;
    state.progress.daily_pillar_completed.xi = true;
    saveState();
  }
}

/* ============================================================
   Level Transition Detection
   ============================================================ */

function checkLevelTransition(dayOffset) {
  const transition = getLevelTransition(dayOffset);
  if (!transition) return;

  const state = loadState();
  // Only show level transition once — check if we've already recorded this word
  if (state.progress.words_seen.includes(currentWord.id)) return;

  // Show the celebration after a brief delay so the card renders first
  setTimeout(() => {
    const levelNames = ['', 'HSK 1', 'HSK 2', 'HSK 3', 'HSK 4', 'HSK 5', 'HSK 6', 'HSK 7-9'];
    const levelNum = currentWord ? currentWord.hsk_level : 1;
    showLevelTransition(transition, levelNames[levelNum] || `HSK ${levelNum}`);
  }, 500);
}

/* ============================================================
   Card Rendering (识)
   ============================================================ */

function renderCard(word) {
  if (!word) return;

  // Word characters
  dom.wordChar.textContent = word.word;

  // Tone-colored pinyin
  dom.wordPinyin.innerHTML = renderToneColoredPinyin(word.pinyin_parts, word.pinyin_tones);

  // Meta (POS + English)
  const posHtml = word.pos ? `<span class="pos">${escHtml(word.pos)}</span> ` : '';
  const enHtml = word.english ? `<span class="english">"${escHtml(word.english)}"</span>` : '';
  dom.wordMeta.innerHTML = posHtml + enHtml;

  // Example sentence
  if (word.example && word.example.zh) {
    dom.exampleSection.hidden = false;
    dom.exampleZh.textContent = word.example.zh;
    dom.examplePinyin.innerHTML = renderToneColoredPinyin(word.example.pinyin_parts, word.example.pinyin_tones);
    dom.exampleEn.textContent = `"${word.example.en || ''}"`;
  } else {
    dom.exampleSection.hidden = true;
  }

  // Glyph breakdown
  if (word.components && word.components.length > 0) {
    dom.glyphSection.hidden = false;
    dom.glyphBreakdown.innerHTML = word.components.map(c => {
      let html = '<div class="glyph-entry">';
      html += `<span class="glyph-char">${escHtml(c.char)}</span>`;
      html += `<span class="glyph-meaning">${escHtml(c.meaning)}</span>`;
      if (c.breakdown) {
        html += `<span class="detail">${escHtml(c.breakdown)}</span>`;
      }
      html += '</div>';
      return html;
    }).join('');
  } else {
    dom.glyphSection.hidden = true;
  }

  // Audio availability
  updateAudioButton(word.id);
  updateSentenceAudioButton(word.id);
}

/* ---- Card accent color ---- */
function updateCardAccent(word) {
  const card = document.querySelector('.card');
  if (!card || !word) return;
  const level = word.hsk_level || 1;
  const colorVar = getLevelColor(level);
  card.style.setProperty('--card-accent', colorVar);
  card.querySelector('::before');
}

function getLevelColor(level) {
  const colors = {
    0: 'var(--hsk-prep)',
    1: 'var(--hsk1)',
    2: 'var(--hsk2)',
    3: 'var(--hsk3)',
    4: 'var(--hsk4)',
    5: 'var(--hsk5)',
    6: 'var(--hsk6)',
    7: 'var(--hsk79)'
  };
  return colors[level] || 'var(--hsk1)';
}

/* ============================================================
   Header Updates
   ============================================================ */

function updateHeader(dayOffset) {
  const state = loadState();
  const stem = getStemBadge(dayOffset);
  dom.stemBadge.textContent = stem.label;

  // Solar term
  const solarTerm = getCurrentSolarTerm();
  dom.solarTerm.textContent = solarTerm ? solarTerm.name : '';

  // Day label
  const level = getHSKLevel(dayOffset);
  const levelNames = { prep: '入门', hsk1: 'HSK 1', hsk2: 'HSK 2', hsk3: 'HSK 3',
    hsk4: 'HSK 4', hsk5: 'HSK 5', hsk6: 'HSK 6', hsk79: 'HSK 7-9' };
  const levelName = levelNames[level.level] || 'HSK 1';
  dom.dayLabel.textContent = `Day ${dayOffset + 1} · ${levelName}`;

  // Card accent color
  if (currentWord) {
    const card = document.querySelector('.card');
    if (card) {
      const levelNum = currentWord.hsk_level || 1;
      const colorKey = Math.min(levelNum, 7);
      card.style.setProperty('--card-accent', getLevelColor(colorKey));
    }
  }
}

/* ============================================================
   Phase Navigation
   ============================================================ */

function showPhase(phase) {
  // Hide all phases
  dom.phaseShi.hidden = true;
  dom.phaseXie.hidden = true;
  dom.phaseXi.hidden = true;
  dom.phaseComplete.hidden = true;

  // Show requested phase
  switch (phase) {
    case 'shi':
      dom.phaseShi.hidden = false;
      currentPhase = 'shi';
      break;
    case 'xie':
      dom.phaseXie.hidden = false;
      currentPhase = 'xie';
      initWritingPhase();
      break;
    case 'xi':
      dom.phaseXi.hidden = false;
      currentPhase = 'xi';
      startReviewPhase();
      break;
    case 'complete':
      dom.phaseComplete.hidden = false;
      currentPhase = 'complete';
      showCompletion();
      break;
  }

  // Update pillar tabs
  dom.pillarTabs.querySelectorAll('.pillar-tab').forEach(t => {
    t.classList.toggle('active', t.dataset.pillar === phase);
  });
}

/* ============================================================
   识 → 写 transition
   ============================================================ */

function onShiContinue() {
  const state = loadState();

  // Auto-enroll word in SRS
  if (currentWord) {
    ensureEnrolled([currentWord]);

    // Add to words_seen if not present
    if (!state.progress.words_seen.includes(currentWord.id)) {
      state.progress.words_seen.push(currentWord.id);
      incrementDaily('new_words');
    }
  }

  state.progress.daily_pillar_completed.shi = true;
  saveState();
  showPhase('xie');
}

function onShiSkip() {
  const state = loadState();
  state.progress.daily_pillar_completed.shi = true;
  saveState();
  showPhase('xie');
}

/* ============================================================
   写 Phase — Hanzi-Writer
   ============================================================ */

function initWritingPhase() {
  if (!currentWord) return;
  const word = currentWord.word;
  const state = loadState();
  const writeAll = state.settings.write_all_chars !== false;

  // Determine which characters to practice
  const chars = writeAll ? [...word] : [word[0]];

  // Validate current char index
  if (currentCharIdx >= chars.length) currentCharIdx = 0;

  // Check for stale writing cursor
  if (state.writing_cursor && state.writing_cursor.word_id !== currentWord.id) {
    currentCharIdx = 0;
  }

  // Show current char label
  dom.writingCharLabel.textContent = chars[currentCharIdx];

  // Render char progress dots
  renderCharProgress(chars, currentCharIdx);

  // Clear previous writer
  clearWriter();

  // Init hanzi-writer
  const char = chars[currentCharIdx];
  initHanziWriter(char, currentWord.hsk_level || 1);

  // Update nav buttons
  dom.btnCharPrev.disabled = currentCharIdx <= 0;
  dom.btnCharNext.disabled = currentCharIdx >= chars.length - 1;

  // Hide result
  dom.writingResult.hidden = true;
}

function renderCharProgress(chars, activeIdx) {
  dom.writingProgress.innerHTML = chars.map((ch, i) => {
    let cls = 'writing-progress-dot';
    if (i === activeIdx) cls += ' active';
    if (i < activeIdx) cls += ' completed';
    return `<span class="${cls}" data-idx="${i}"></span>`;
  }).join('');
}

function initHanziWriter(char, hskLevel) {
  if (typeof HanziWriter === 'undefined') {
    dom.writingCanvas.innerHTML = '<p style="text-align:center;color:var(--fg-dim);padding:2rem;">Hanzi Writer 加载中…</p>';
    return;
  }

  const canvasSize = Math.min(dom.writingCanvas.clientWidth || 320, 320);
  dom.writingCanvas.innerHTML = '';

  // Create a container div for hanzi-writer
  const container = document.createElement('div');
  container.className = 'hw-container';
  container.style.cssText = `
    width: ${canvasSize}px;
    height: ${canvasSize}px;
    position: relative;
    margin: 0 auto;
    background-image:
      linear-gradient(to right, #2A2A4A 1px, transparent 1px),
      linear-gradient(to bottom, #2A2A4A 1px, transparent 1px),
      linear-gradient(to bottom right, transparent calc(50% - 0.5px), #2A2A4A calc(50% - 0.5px), #2A2A4A calc(50% + 0.5px), transparent calc(50% + 0.5px)),
      linear-gradient(to bottom left, transparent calc(50% - 0.5px), #2A2A4A calc(50% - 0.5px), #2A2A4A calc(50% + 0.5px), transparent calc(50% + 0.5px));
    background-size:
      100% 100%,
      100% 100%,
      100% 100%,
      100% 100%;
    border: 1px solid #2A2A4A;
    border-radius: 4px;
  `;
  dom.writingCanvas.appendChild(container);

  // Color based on HSK level
  const colors = ['#4a9e8a', '#4a9e8a', '#6db3a4', '#c4452d', '#c9a96e', '#d4b878', '#8faacc', '#3a6e8e'];
  const strokeColor = colors[hskLevel] || colors[1];

  try {
    currentWriter = HanziWriter.create(container, char, {
      width: canvasSize,
      height: canvasSize,
      padding: 5,
      showCharacter: true,
      showOutline: true,
      strokeColor: strokeColor,
      radicalColor: '#4a9e8a',
      strokeAnimationSpeed: 1.2,
      delayBetweenStrokes: 300,
      outlineColor: '#2a2a4a',
      drawingColor: strokeColor,
      drawingWidth: 6,
      highlightOnComplete: true,
      highlightColor: '#50fa7b',
      showHintAfterMisses: 3,
      charDataLoader: function(ch, onComplete, onError) {
        HanziWriter.loadCharacterData(ch).then(onComplete).catch(onError);
      }
    });
  } catch (e) {
    console.warn('Hanzi-writer init error:', e);
    dom.writingCanvas.innerHTML = '<p style="text-align:center;color:var(--fg-dim);padding:2rem;">笔画数据加载失败</p>';
  }
}

function clearWriter() {
  if (currentWriter) {
    currentWriter = null;
  }
}

/* ---- Writing mode buttons ---- */
function onAnimate() {
  if (currentWriter) {
    currentWriter.showCharacter({ duration: 0 });
    currentWriter.animateCharacter({
      strokeAnimationSpeed: 1.2,
      delayBetweenStrokes: 300
    });
  }
}

function onQuiz() {
  if (!currentWriter || !currentWord) return;
  dom.writingResult.hidden = true;

  currentWriter.quiz({
    showHintAfterMisses: 3,
    onComplete: function(summary) {
      // hanzi-writer v3.x returns { totalStrokes, correctStrokes, missedStrokes }
      // Older versions may use different property names — handle both
      const total = summary.totalStrokes || summary.strokes || 0;
      const correct = (summary.correctStrokes !== undefined ? summary.correctStrokes : summary.correct) || 0;
      const totalMistakes = summary.missedStrokes !== undefined ? summary.missedStrokes : (summary.mistakes || 0);

      // Record writing score
      recordWritingScore(currentWord.id, totalMistakes);

      // Show result
      dom.writingResult.hidden = false;
      if (totalMistakes === 0 && total > 0) {
        dom.writingResult.className = 'writing-result good';
        dom.writingResult.textContent = `✓ ${correct}/${total} strokes`;
      } else if (total > 0) {
        dom.writingResult.className = 'writing-result keep-practicing';
        const msg = totalMistakes <= 3
          ? `${correct}/${total} — 不错！`
          : `${correct}/${total} — keep practicing!`;
        dom.writingResult.textContent = msg;
      } else {
        dom.writingResult.className = 'writing-result good';
        dom.writingResult.textContent = '✓ Complete!';
      }
    }
  });
}

function onShowChar() {
  if (currentWriter) {
    currentWriter.showCharacter();
  }
}

/* ---- Character navigation ---- */
function onCharNext() {
  if (!currentWord) return;
  const chars = [...currentWord.word];
  if (currentCharIdx < chars.length - 1) {
    currentCharIdx++;
    // Update cursor persistence
    const state = loadState();
    state.writing_cursor = { word_id: currentWord.id, char_idx: currentCharIdx };
    saveState();
    initWritingPhase();
  }
}

function onCharPrev() {
  if (currentCharIdx > 0) {
    currentCharIdx--;
    const state = loadState();
    state.writing_cursor = { word_id: currentWord.id, char_idx: currentCharIdx };
    saveState();
    initWritingPhase();
  }
}

/* ---- 写 → 习 transition ---- */
function onXieContinue() {
  const state = loadState();
  state.progress.daily_pillar_completed.xie = true;
  saveState();
  showPhase('xi');
}

function onXieSkip() {
  const state = loadState();
  state.progress.daily_pillar_completed.xie = true;
  saveState();
  showPhase('xi');
}

/* ============================================================
   习 Phase — SRS Review
   ============================================================ */

function startReviewPhase() {
  reviewQueue = getDueItems();

  if (reviewQueue.length === 0) {
    // No reviews due — auto-skip to completion
    const state = loadState();
    state.progress.daily_pillar_completed.xi = true;
    saveState();
    showPhase('complete');
    return;
  }

  dom.reviewEmpty.hidden = true;
  reviewIdx = 0;
  renderReviewCard(reviewIdx);
}

function renderReviewCard(idx) {
  if (idx >= reviewQueue.length) {
    // All reviews done
    dom.reviewCards.innerHTML = '<div class="review-empty" style="padding:2rem;"><p>复习完成！</p></div>';
    return;
  }

  const item = reviewQueue[idx];
  // Find the full word data for example sentence
  const wordData = HSK_DATA ? HSK_DATA.words.find(w => w.id === item.id) : null;

  dom.reviewCards.innerHTML = `
    <div class="review-card" data-word-id="${item.id}">
      <div class="review-char" lang="zh-CN">${escHtml(item.word)}</div>
      <div class="review-reveal" id="review-reveal-${idx}" hidden>
        <div class="review-pinyin">
          ${renderToneColoredPinyin(
            wordData ? wordData.pinyin_parts : null,
            wordData ? wordData.pinyin_tones : null
          ) || escHtml(item.pinyin)}
        </div>
        <div class="review-english">"${escHtml(item.english)}"</div>
        ${wordData && wordData.example ? `
        <div class="review-example">
          <div class="review-example-zh" lang="zh-CN">${escHtml(wordData.example.zh)}</div>
          <div class="review-example-pinyin">${renderToneColoredPinyin(wordData.example.pinyin_parts, wordData.example.pinyin_tones)}</div>
          <div class="review-example-en">"${escHtml(wordData.example.en)}"</div>
        </div>
        ` : ''}
        <div class="review-audio">
          <button class="btn-play review-play-btn" data-word-id="${item.id}" data-audio-type="word">▶ 听词</button>
          ${wordData && wordData.example ? `<button class="btn-play review-play-btn" data-word-id="${item.id}" data-audio-type="sentence">▶ 听例句</button>` : ''}
        </div>
      </div>
      <div class="review-actions" id="review-actions-${idx}">
        <button class="btn-reveal" data-review-idx="${idx}">显示 Show</button>
      </div>
      <div class="review-judgment" id="review-judgment-${idx}" hidden>
        <button class="btn-know" data-word-id="${item.id}" data-quality="4">会了 ✓</button>
        <button class="btn-need" data-word-id="${item.id}" data-quality="1">需要再背 ↺</button>
      </div>
    </div>
  `;

  // Wire reveal button
  dom.reviewCards.querySelector(`.btn-reveal[data-review-idx="${idx}"]`)
    .addEventListener('click', function() {
      document.getElementById(`review-reveal-${idx}`).hidden = false;
      document.getElementById(`review-actions-${idx}`).hidden = true;
      document.getElementById(`review-judgment-${idx}`).hidden = false;
    });

  // Wire audio buttons
  dom.reviewCards.querySelectorAll('.review-play-btn').forEach(btn => {
    btn.addEventListener('click', () => playWordAudio(btn.dataset.wordId, btn.dataset.audioType));
  });

  // Wire judgment buttons
  dom.reviewCards.querySelectorAll('.btn-know, .btn-need').forEach(btn => {
    btn.addEventListener('click', function() {
      const wordId = this.dataset.wordId;
      const quality = parseInt(this.dataset.quality);
      recordResult(wordId, quality);
      incrementDaily('reviews_done');
      // Move to next review
      reviewIdx++;
      renderReviewCard(reviewIdx);
    });
  });
}

/* ---- 习 completion ---- */
function onXiDone() {
  const state = loadState();
  state.progress.daily_pillar_completed.xi = true;
  saveState();
  showPhase('complete');
}

function onXiSkip() {
  const state = loadState();
  state.progress.daily_pillar_completed.xi = true;
  saveState();
  showPhase('complete');
}

/* ============================================================
   Completion
   ============================================================ */

function showCompletion() {
  const state = loadState();
  const streak = updateStreak();
  const dayOffset = getDayOffset(state);

  dom.stampStreak.textContent = `连续 ${streak.current_streak} 天`;
  dom.stampStem.textContent = `甲子 cycle: ${(dayOffset + 1) % 60 || 60}/60`;

  // Check 甲子 completion
  const jiaziCompleted = checkJiaziCompletion(state, dayOffset);
  if (jiaziCompleted) {
    const cycleNum = state.progress.completed_jiazi_cycles || 0;
    const wordsSeen = state.progress.words_seen.length;
    showJiaziCelebration(cycleNum, dayOffset, wordsSeen);
  }

  // Update daily pillar completions
  incrementDaily('pillar_completions');
}

/* ============================================================
   Audio
   ============================================================ */

function updateAudioButton(wordId) {
  const entry = AUDIO_INDEX && AUDIO_INDEX.files ? AUDIO_INDEX.files[wordId] : null;
  const hasAudio = entry && entry.word;
  dom.btnPlayWord.classList.toggle('error', !hasAudio);
  dom.btnPlayWord.textContent = '▶ 听';
  dom.audioUnavail.hidden = hasAudio;
}

function updateSentenceAudioButton(wordId) {
  const entry = AUDIO_INDEX && AUDIO_INDEX.files ? AUDIO_INDEX.files[wordId] : null;
  const hasAudio = entry && entry.sentence;
  dom.btnPlaySentence.classList.toggle('error', !hasAudio);
  dom.btnPlaySentence.textContent = '▶ 听句';
  dom.sentenceAudioUnavail.hidden = hasAudio;
}

function getAudioButton(type) {
  return type === 'sentence' ? dom.btnPlaySentence : dom.btnPlayWord;
}

function getAudioUnavailable(type) {
  return type === 'sentence' ? dom.sentenceAudioUnavail : dom.audioUnavail;
}

function playWordAudio(wordId, type) {
  const entry = AUDIO_INDEX && AUDIO_INDEX.files ? AUDIO_INDEX.files[wordId] : null;
  const audioPath = entry ? entry[type || 'word'] : null;
  const btn = getAudioButton(type);
  const unavail = getAudioUnavailable(type);

  if (!audioPath) {
    btn.classList.add('error');
    return;
  }

  stopCurrentAudio();

  const state = loadState();
  const speed = state.settings.audio_speed || 0.95;

  // Audio paths in index.json are relative to the audio/ directory
  const fullPath = 'audio/' + audioPath;
  const audio = new Audio(fullPath);
  audio.playbackRate = speed;

  audio.addEventListener('ended', () => {
    btn.classList.remove('playing');
    btn.textContent = type === 'sentence' ? '▶ 听句' : '▶ 听';
    currentAudio = null;
  });

  audio.addEventListener('error', () => {
    btn.classList.remove('playing');
    btn.classList.add('error');
    unavail.hidden = false;
    currentAudio = null;
  });

  currentAudio = audio;
  btn.classList.add('playing');
  btn.textContent = '⏸';
  audio.play().catch(() => {
    btn.classList.remove('playing');
    btn.classList.add('error');
  });
}

function stopCurrentAudio() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio = null;
  }
}

/* ============================================================
   First-Visit Onboarding
   ============================================================ */

function checkFirstVisit(state) {
  // First visit: no words seen, recent creation, not already onboarded
  const isFirstVisit = state.progress.words_seen.length === 0 &&
    !state.onboarding_completed &&
    (!state.created_at || Date.now() - new Date(state.created_at).getTime() < 60000);

  if (!isFirstVisit) return;

  // Show onboarding after a brief delay
  setTimeout(() => {
    showOnboarding();
  }, 800);
}

function showOnboarding() {
  const c = getC();
  c.svg.innerHTML = `
    <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g stroke="#d4a93b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <circle cx="100" cy="80" r="40" stroke="#d4a93b" stroke-width="1.5"/>
        <text x="100" y="95" text-anchor="middle" fill="#d4a93b" font-family="Ma Shan Zheng, serif" font-size="36">字</text>
        <path d="M60 100 C40 120 30 140 25 160" stroke-width="1" opacity="0.5"/>
        <path d="M68 105 C55 125 48 145 45 165" stroke-width="1" opacity="0.5"/>
        <path d="M100 120 C100 140 100 155 100 170" stroke-width="1" opacity="0.5"/>
        <path d="M132 105 C145 125 152 145 155 165" stroke-width="1" opacity="0.5"/>
        <path d="M140 100 C160 120 170 140 175 160" stroke-width="1" opacity="0.5"/>
        <path d="M58 115 C50 110 45 112 48 118" stroke-width="1" opacity="0.7"/>
        <path d="M105 135 C112 130 118 132 115 138" stroke-width="1" opacity="0.7"/>
        <path d="M138 118 C148 114 155 116 152 122" stroke-width="1" opacity="0.7"/>
      </g>
    </svg>`;
  c.title.textContent = '欢迎来到 每日字';
  
  // Build level picker options from LEVEL_BOUNDARIES
  const levelOptions = [
    { id: null, label: 'HSK 1 — 木 (Beginner)', offset: 0 },
    { id: 'hsk2', label: 'HSK 2 — 木→火', offset: 497 },
    { id: 'hsk3', label: 'HSK 3 — 火 (Fire)', offset: 1258 },
    { id: 'hsk4', label: 'HSK 4 — 火→土', offset: 2224 },
    { id: 'hsk5', label: 'HSK 5 — 土→金', offset: 3217 },
    { id: 'hsk6', label: 'HSK 6 — 金 (Metal)', offset: 4284 },
    { id: 'hsk79', label: 'HSK 7-9 — 水 (Water)', offset: 5417 },
  ];
  
  c.body.innerHTML = `
    <p style="margin-bottom:16px;">A word a day, like a daily vitamin for your Chinese.</p>
    <p style="color:var(--fg-soft);font-size:14px;margin-bottom:12px;">Choose your starting level:</p>
    <div class="level-picker" id="onboarding-level-picker">
      ${levelOptions.map(lo => `
        <button class="level-opt" data-offset="${lo.offset}" ${lo.offset === 0 ? 'class="level-opt active"' : ''}>
          <span class="level-opt-label">${lo.label}</span>
        </button>
      `).join('')}
    </div>
    <p style="color:var(--fg-soft);font-size:12px;margin-top:12px;">Your progress stays on this device.</p>
  `;
  c.overlay.hidden = false;
  c.btn.textContent = '开始 Start →';
  
  // Wire level picker
  document.getElementById('onboarding-level-picker').addEventListener('click', function(e) {
    const btn = e.target.closest('.level-opt');
    if (!btn) return;
    this.querySelectorAll('.level-opt').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
  
  // Override the continue button to apply level selection
  c.btn.onclick = function() {
    const active = document.querySelector('.level-opt.active');
    if (active) {
      const offset = parseInt(active.dataset.offset);
      const state = loadState();
      state.learner.start_offset = offset;
      state.onboarding_completed = true;  // mark so we don't loop
      state.created_at = new Date().toISOString();  // reset timer
      saveState();
    }
    c.overlay.hidden = true;
    c.btn.onclick = null;
    location.reload();
  };
}

/* ============================================================
   Favorites
   ============================================================ */

function toggleFavorite() {
  if (!currentWord) return;
  const state = loadState();
  const idx = state.favorites.indexOf(currentWord.id);

  if (idx >= 0) {
    state.favorites.splice(idx, 1);
  } else {
    state.favorites.push(currentWord.id);
  }

  saveState();
  updateFavButton();
}

function updateFavButton() {
  if (!currentWord) return;
  const state = loadState();
  const saved = state.favorites.includes(currentWord.id);
  dom.favBtn.textContent = saved ? '★' : '☆';
  dom.favBtn.classList.toggle('saved', saved);
  dom.favBtn.setAttribute('aria-label', saved ? 'Unsave word' : 'Save word');
}

/* ============================================================
   Altar Update
   ============================================================ */

function updateAltar() {
  if (!HSK_DATA) return;
  const state = loadState();
  const altar = getAltarState(state.progress.words_seen);

  const fillMap = {
    wood: dom.altarWood,
    fire: dom.altarFire,
    earth: dom.altarEarth,
    metal: dom.altarMetal,
    water: dom.altarWater
  };

  for (const [tier, el] of Object.entries(fillMap)) {
    if (el) {
      const data = altar[tier];
      const pct = data && data.total > 0 ? Math.round((data.seen / data.total) * 100) : 0;
      el.style.width = Math.min(pct, 100) + '%';
    }
  }
}

/* ============================================================
   Missed-Day Handling
   ============================================================ */

function showMissedNotice(days) {
  dom.missedCount.textContent = days;
  dom.missedNotice.hidden = false;
}

function onCatchUp() {
  dom.missedNotice.hidden = true;
  catchupMode = true;

  const state = loadState();
  const today = getLocalDate();
  const daysMissed = dateDiffInDays(state.progress.last_opened_date, today) - 1;
  state.progress.catchup_days_remaining = daysMissed;
  saveState();

  // Show the first missed day's word (识 card only)
  const catchupOffset = getDayOffset(state) - daysMissed;
  loadDay(catchupOffset);
}

function onSkipAhead() {
  dom.missedNotice.hidden = true;
  catchupMode = false;

  const state = loadState();
  cleanupCatchupState(state);
  saveState();

  const todayOffset = getDayOffset(state);
  loadDay(todayOffset);
}

/* ============================================================
   Day Navigation
   ============================================================ */

function goToPrevDay() {
  if (currentDayOffset > 0) {
    loadDay(currentDayOffset - 1);
  }
}

function goToNextDay() {
  if (catchupMode) {
    const state = loadState();
    if (state.progress.catchup_days_remaining > 0) {
      state.progress.catchup_days_remaining -= 1;
      saveState();
      loadDay(currentDayOffset + 1);
      if (state.progress.catchup_days_remaining <= 0) {
        catchupMode = false;
        cleanupCatchupState(state);
        saveState();
      }
      return;
    }
  }
  const maxIdx = HSK_DATA ? HSK_DATA.words.length - 1 : 0;
  if (currentDayOffset < maxIdx) {
    loadDay(currentDayOffset + 1);
  }
}

function goToToday() {
  const state = loadState();
  const todayOffset = getDayOffset(state);
  loadDay(todayOffset);
  dom.missedNotice.hidden = true;
}

/* ============================================================
   Search
   ============================================================ */

function openSearch() {
  dom.searchModal.hidden = false;
  dom.searchResults.innerHTML = '';
  dom.searchInput.value = '';
  dom.searchInput.focus();
  buildSearchFilters();
}

function closeSearch() {
  dom.searchModal.hidden = true;
}

function buildSearchFilters() {
  if (!HSK_DATA || !HSK_DATA.meta || !HSK_DATA.meta.levels) return;
  dom.searchFilters.innerHTML =
    '<button class="filter-btn active" data-level="all">All</button>' +
    HSK_DATA.meta.levels.filter(l => l.word_count > 0).map(l =>
      `<button class="filter-btn" data-level="${l.id}">${l.name}</button>`
    ).join('');

  dom.searchFilters.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      dom.searchFilters.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterSearch();
    });
  });
}

let searchTimer = null;
function filterSearch() {
  const q = dom.searchInput.value.trim().toLowerCase();
  const activeFilter = dom.searchFilters.querySelector('.filter-btn.active');
  const levelFilter = activeFilter ? activeFilter.dataset.level : 'all';

  if (!HSK_DATA) return;
  let results = HSK_DATA.words;

  if (levelFilter !== 'all') {
    results = results.filter(w => {
      const levelKey = `hsk${w.hsk_level}`;
      return levelKey === levelFilter || (w.hsk_level === 7 && levelFilter === 'hsk79');
    });
  }

  if (q) {
    results = results.filter(w =>
      w.word.includes(q) ||
      (w.pinyin_text || '').toLowerCase().includes(q) ||
      (w.english || '').toLowerCase().includes(q)
    );
  }

  renderSearchResults(q ? results : []);
}

function renderSearchResults(results) {
  if (results.length === 0) {
    dom.searchResults.innerHTML = '<div class="search-empty">未找到匹配字词 · No matching words</div>';
    return;
  }

  const state = loadState();
  dom.searchResults.innerHTML = results.slice(0, 50).map(w => {
    const isFav = state.favorites.includes(w.id);
    const dayIdx = HSK_DATA.words.indexOf(w);
    const levelColors = ['', 'var(--hsk1)', 'var(--hsk2)', 'var(--hsk3)', 'var(--hsk4)', 'var(--hsk5)', 'var(--hsk6)', 'var(--hsk79)'];
    const color = levelColors[w.hsk_level] || 'var(--hsk1)';
    return `<button class="search-result" data-day-idx="${dayIdx}">
      <span class="result-char">${escHtml(w.word)}</span>
      <span class="result-pinyin">${escHtml(w.pinyin_text || '')}</span>
      <span class="result-english">${escHtml(w.english || '')}</span>
      <span class="result-level-badge" style="border-color:${color};color:${color}">HSK ${w.hsk_level}</span>
      <span class="result-fav">${isFav ? '★' : ''}</span>
    </button>`;
  }).join('');

  dom.searchResults.querySelectorAll('.search-result').forEach(el => {
    el.addEventListener('click', () => {
      const idx = parseInt(el.dataset.dayIdx);
      if (!isNaN(idx)) {
        closeSearch();
        loadDay(idx);
      }
    });
  });
}

/* ============================================================
   Favorites View
   ============================================================ */

function openFavorites() {
  dom.favoritesModal.hidden = false;
  renderFavorites();
}

function closeFavorites() {
  dom.favoritesModal.hidden = true;
}

function renderFavorites() {
  if (!HSK_DATA) return;
  const state = loadState();
  const favIds = state.favorites || [];

  if (favIds.length === 0) {
    dom.favoritesList.innerHTML = '<div class="search-empty">还没有收藏 · No saved words yet</div>';
    return;
  }

  dom.favoritesList.innerHTML = favIds.map(id => {
    const word = HSK_DATA.words.find(w => w.id === id);
    if (!word) return '';
    return `<div class="fav-item">
      <span class="fav-char" lang="zh-CN">${escHtml(word.word)}</span>
      <span class="fav-pinyin">${escHtml(word.pinyin_text || '')}</span>
      <span class="fav-english">${escHtml(word.english || '')}</span>
      <button class="fav-remove" data-word-id="${word.id}" aria-label="Remove from favorites">✕</button>
    </div>`;
  }).join('');

  dom.favoritesList.querySelectorAll('.fav-remove').forEach(btn => {
    btn.addEventListener('click', () => {
      const state = loadState();
      const id = btn.dataset.wordId;
      state.favorites = state.favorites.filter(f => f !== id);
      saveState();
      renderFavorites();
      updateFavButton();
    });
  });
}

/* ============================================================
   Quiz Mode
   ============================================================ */

let quizWords = [];
let quizIdx = 0;
let quizScore = 0;
let quizTotal = 0;
let quizAnswered = false;
let quizResults = [];
let quizMode = 'char-to-en'; // 'char-to-en' or 'en-to-char'

function openQuiz() {
  const state = loadState();
  const seenIds = state.progress.words_seen || [];

  if (seenIds.length < 4) {
    alert('需要至少学习 4 个字才能开始测验\nLearn at least 4 words first!');
    return;
  }

  // Pick 10 random words from seen words, or all if fewer
  const pool = seenIds.slice().sort(() => Math.random() - 0.5);
  quizWords = pool.slice(0, Math.min(10, pool.length));
  quizIdx = 0;
  quizScore = 0;
  quizTotal = quizWords.length;
  quizResults = [];
  quizAnswered = false;

  // Randomly choose quiz direction
  quizMode = Math.random() < 0.5 ? 'char-to-en' : 'en-to-char';

  dom.quizSummary.hidden = true;
  dom.quizNext.hidden = true;
  dom.quizDone.hidden = true;
  dom.quizModal.hidden = false;

  showQuizQuestion();
}

function closeQuiz() {
  dom.quizModal.hidden = true;
}

function showQuizQuestion() {
  if (quizIdx >= quizWords.length) {
    showQuizSummary();
    return;
  }

  const wordId = quizWords[quizIdx];
  const word = HSK_DATA ? HSK_DATA.words.find(w => w.id === wordId) : null;
  if (!word) { quizIdx++; showQuizQuestion(); return; }

  dom.quizAnswered = false;
  dom.quizResult.hidden = true;
  dom.quizNext.hidden = true;
  dom.quizStats.textContent = `${quizIdx + 1}/${quizTotal}`;

  // Generate distractors (3 wrong answers)
  const distractors = generateDistractors(word, 3);
  const options = quizMode === 'char-to-en'
    ? [word.english, ...distractors]
    : [word.word, ...distractors];

  // Shuffle options
  const shuffled = options.sort(() => Math.random() - 0.5);
  const correctAnswer = quizMode === 'char-to-en' ? word.english : word.word;

  // Render question
  if (quizMode === 'char-to-en') {
    dom.quizQuestion.innerHTML = `
      <div class="q-label">选择正确的意思 · Choose the meaning</div>
      <div class="q-char" lang="zh-CN">${escHtml(word.word)}</div>
      <div class="q-pinyin">${escHtml(word.pinyin_text || '')}</div>
    `;
  } else {
    dom.quizQuestion.innerHTML = `
      <div class="q-label">选择正确的汉字 · Choose the character</div>
      <div class="q-english">${escHtml(word.english || '')}</div>
    `;
  }

  // Render options
  dom.quizOptions.innerHTML = shuffled.map((opt, i) => {
    const isChar = quizMode === 'en-to-char';
    return `<button class="quiz-option ${isChar ? 'opt-char' : ''}" data-idx="${i}" data-correct="${opt === correctAnswer}">${escHtml(opt)}</button>`;
  }).join('');

  dom.quizOptions.querySelectorAll('.quiz-option').forEach(btn => {
    btn.addEventListener('click', () => handleQuizAnswer(btn, correctAnswer));
  });
}

function generateDistractors(word, count) {
  if (!HSK_DATA) return [];
  // Get random words from the same HSK level as distractors
  const sameLevel = HSK_DATA.words.filter(w =>
    w.hsk_level === word.hsk_level && w.id !== word.id
  );
  const pool = quizMode === 'char-to-en'
    ? sameLevel.map(w => w.english).filter(Boolean)
    : sameLevel.map(w => w.word).filter(Boolean);

  // Shuffle and pick
  const shuffled = pool.sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(count, shuffled.length));
}

function handleQuizAnswer(btn, correctAnswer) {
  if (dom.quizAnswered) return;
  dom.quizAnswered = true;

  const selected = btn.dataset.correct === 'true';
  const wordId = quizWords[quizIdx];
  const word = HSK_DATA ? HSK_DATA.words.find(w => w.id === wordId) : null;

  // Disable all buttons and mark correct/wrong
  dom.quizOptions.querySelectorAll('.quiz-option').forEach(b => {
    b.disabled = true;
    if (b.dataset.correct === 'true') b.classList.add('correct');
  });
  if (!selected) btn.classList.add('wrong');

  // Show result
  dom.quizResult.hidden = false;
  if (selected) {
    dom.quizResult.className = 'quiz-result correct';
    dom.quizResult.textContent = '✓ Correct!';
    quizScore++;
  } else {
    dom.quizResult.className = 'quiz-result wrong';
    const correctWord = quizMode === 'char-to-en' ? correctAnswer : `"${word?.word || ''}"`;
    dom.quizResult.textContent = `✗ 正确答案: ${correctWord}`;
  }

  quizResults.push({
    wordId: wordId,
    word: word?.word || '',
    pinyin: word?.pinyin_text || '',
    english: word?.english || '',
    correct: selected
  });

  // Feed back into SRS
  if (word) {
    recordResult(wordId, selected ? 4 : 1);
  }

  // Show next button or done
  if (quizIdx >= quizWords.length - 1) {
    dom.quizDone.hidden = false;
  } else {
    dom.quizNext.hidden = false;
  }
}

function nextQuizQuestion() {
  quizIdx++;
  dom.quizNext.hidden = true;
  dom.quizDone.hidden = true;
  showQuizQuestion();
}

function showQuizSummary() {
  dom.quizQuestion.innerHTML = '';
  dom.quizOptions.innerHTML = '';
  dom.quizResult.hidden = true;
  dom.quizNext.hidden = true;
  dom.quizDone.hidden = true;
  dom.quizSummary.hidden = false;

  const pct = Math.round((quizScore / quizTotal) * 100);
  dom.quizScore.textContent = `${quizScore}/${quizTotal} (${pct}%)`;

  dom.quizResultsList.innerHTML = quizResults.map(r => `
    <div class="quiz-result-item">
      <span class="r-word">${escHtml(r.word)}</span>
      <span style="color:var(--fg-dim);font-size:12px;">${escHtml(r.pinyin)}</span>
      <span style="color:var(--fg-dim);font-size:12px;">${escHtml(r.english)}</span>
      <span class="r-status ${r.correct ? 'good' : 'bad'}">${r.correct ? '✓' : '✗'}</span>
    </div>
  `).join('');
}

/* ============================================================
   Settings
   ============================================================ */

function openSettings() {
  dom.settingsModal.hidden = false;
  const state = loadState();
  const s = state.settings;
  dom.settingToneColors.checked = s.tone_colors !== false;
  dom.settingSeasonal.checked = s.seasonal_atmosphere !== false;
  dom.settingWriteAll.checked = s.write_all_chars !== false;
  dom.settingAudioSpeed.value = s.audio_speed || 0.95;
  dom.settingLanguage.value = s.language || 'en';
  dom.settingStartLevel.value = String(state.learner.start_offset || 0);
}

function closeSettings() {
  dom.settingsModal.hidden = true;
  applySettings();
}

function applySettings() {
  const state = loadState();
  state.settings.tone_colors = dom.settingToneColors.checked;
  state.settings.seasonal_atmosphere = dom.settingSeasonal.checked;
  state.settings.write_all_chars = dom.settingWriteAll.checked;
  state.settings.audio_speed = parseFloat(dom.settingAudioSpeed.value);
  state.settings.language = dom.settingLanguage.value;
  
  // Handle starting level change
  const newOffset = parseInt(dom.settingStartLevel.value);
  if (newOffset !== (state.learner.start_offset || 0)) {
    state.learner.start_offset = newOffset;
    // Reset progress to start fresh at the new level
    state.progress.words_seen = [];
    state.progress.daily_pillar_completed = { shi: false, xie: false, xi: false };
    saveState();
    location.reload();
    return;
  }
  
  saveState();
  applySeasonalAtmosphere(state);
}

/* ---- Seasonal Atmosphere ---- */
function applySeasonalAtmosphere(state) {
  // Preserve the existing level class
  const currentLevel = document.body.className.match(/level-\d+/);
  const levelClass = currentLevel ? currentLevel[0] : '';
  
  if (state.settings.seasonal_atmosphere === false) {
    document.body.className = levelClass;
    return;
  }
  const term = getCurrentSolarTerm();
  if (term) {
    const tempIdx = Math.round(term.temp * 8);
    document.body.className = `temp-${tempIdx} ${levelClass}`.trim();
  }
}

/* ---- Backup / Restore / Sync ---- */
function onBackup() {
  exportBackup();
}

function onRestore() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.addEventListener('change', async () => {
    if (input.files.length === 0) return;
    try {
      await importBackup(input.files[0]);
      alert('恢复成功！页面将重新加载。\nRestore successful! Reloading.');
      location.reload();
    } catch (err) {
      alert('恢复失败: ' + err.message);
    }
  });
  input.click();
}

function onSyncUrl() {
  const url = createSyncURL();
  if (url) {
    // Copy to clipboard
    navigator.clipboard.writeText(url).then(() => {
      alert('同步链接已复制到剪贴板！\nSync URL copied to clipboard!');
    }).catch(() => {
      // Fallback
      prompt('复制此链接以同步您的进度:\nCopy this URL to sync your progress:', url);
    });
  } else {
    alert('创建同步链接失败');
  }
}

/* ============================================================
   Keyboard Shortcuts
   ============================================================ */

function onKeyDown(e) {
  // Don't handle when in input fields
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;

  switch (e.key) {
    case 'ArrowLeft':
      if (!e.metaKey && !e.ctrlKey) { e.preventDefault(); goToPrevDay(); }
      break;
    case 'ArrowRight':
      if (!e.metaKey && !e.ctrlKey) { e.preventDefault(); goToNextDay(); }
      break;
    case 'Home':
      e.preventDefault(); goToToday();
      break;
    case ' ':
      if (currentPhase === 'shi') { e.preventDefault(); playWordAudio(currentWord?.id, 'word'); }
      break;
    case 's':
      if (currentPhase === 'shi') { e.preventDefault(); toggleFavorite(); }
      break;
    case 'Enter':
      if (currentPhase === 'shi') { e.preventDefault(); onShiContinue(); }
      break;
    case '/':
      if (!dom.searchModal.hidden) break;
      e.preventDefault(); openSearch();
      break;
    case 'Escape':
      if (!dom.searchModal.hidden) closeSearch();
      else if (!dom.favoritesModal.hidden) closeFavorites();
      else if (!dom.settingsModal.hidden) closeSettings();
      else if (!dom.celebrationOverlay.hidden) dom.celebrationOverlay.hidden = true;
      break;
    case 'a':
      if (currentPhase === 'xie') { e.preventDefault(); onAnimate(); }
      break;
    case 'q':
      if (currentPhase === 'xie') { e.preventDefault(); onQuiz(); }
      break;
    case 'v':
      if (currentPhase === 'xie') { e.preventDefault(); onShowChar(); }
      break;
    case '1':
      if (currentPhase === 'xi') { clickJudgmentButton(1); }
      break;
    case '2':
      if (currentPhase === 'xi') { clickJudgmentButton(2); }
      break;
  }
}

function clickJudgmentButton(quality) {
  const buttons = dom.reviewCards.querySelectorAll(
    quality === 1 ? '.btn-need' : '.btn-know'
  );
  if (buttons.length > 0) buttons[0].click();
}

/* ============================================================
   Error State
   ============================================================ */

function showError(title, err) {
  const main = document.querySelector('main');
  main.innerHTML = `
    <div style="text-align:center;padding:4rem 2rem;">
      <div style="font-size:48px;margin-bottom:1rem;color:var(--fg-dim);">字</div>
      <h2 style="font-family:var(--font-body-zh);font-size:20px;margin-bottom:0.5rem;">${escHtml(title)}</h2>
      <p style="color:var(--fg-dim);font-size:13px;font-family:var(--font-ui);">${escHtml(String(err))}</p>
      <button class="btn btn-primary" style="margin-top:1.5rem;" onclick="location.reload()">↻ 重试 Retry</button>
    </div>`;
}

function showCompletionMessage() {
  const main = document.querySelector('main');
  main.innerHTML = `
    <div style="text-align:center;padding:4rem 2rem;">
      <div style="font-size:48px;margin-bottom:1rem;color:var(--correct);">✓</div>
      <h2 style="font-family:var(--font-display-zh);font-size:28px;margin-bottom:0.5rem;">恭喜！</h2>
      <p style="font-family:var(--font-body-zh);font-size:16px;color:var(--fg-dim);">你已完成所有每日字</p>
      <p style="font-family:var(--font-body-en);font-size:14px;color:var(--fg-soft);">You've completed all words!</p>
    </div>`;
}

/* ============================================================
   Event Wiring
   ============================================================ */

function wireEvents() {
  // Card phase buttons
  dom.btnShiContinue.addEventListener('click', onShiContinue);
  dom.btnShiSkip.addEventListener('click', onShiSkip);

  // Writing phase buttons
  dom.btnAnimate.addEventListener('click', onAnimate);
  dom.btnTrace.addEventListener('click', onQuiz);
  dom.btnQuizHeader.addEventListener('click', openQuiz);
  dom.btnShow.addEventListener('click', onShowChar);
  dom.btnCharPrev.addEventListener('click', onCharPrev);
  dom.btnCharNext.addEventListener('click', onCharNext);
  dom.btnXieContinue.addEventListener('click', onXieContinue);
  dom.btnXieSkip.addEventListener('click', onXieSkip);

  // Review phase buttons
  dom.btnXiDone.addEventListener('click', onXiDone);
  dom.btnXiSkip.addEventListener('click', onXiSkip);

  // Navigation
  dom.navPrev.addEventListener('click', goToPrevDay);
  dom.navToday.addEventListener('click', goToToday);
  dom.navNext.addEventListener('click', goToNextDay);

  // Audio
  dom.btnPlayWord.addEventListener('click', () => {
    if (currentWord) playWordAudio(currentWord.id, 'word');
  });
  dom.btnPlaySentence.addEventListener('click', () => {
    if (currentWord) playWordAudio(currentWord.id, 'sentence');
  });

  // Favorites
  dom.favBtn.addEventListener('click', toggleFavorite);

  // Missed-day
  dom.btnCatchUp.addEventListener('click', onCatchUp);
  dom.btnSkipAhead.addEventListener('click', onSkipAhead);

  // Search
  dom.btnSearch.addEventListener('click', openSearch);
  dom.searchModal.querySelector('.btn-close-modal').addEventListener('click', closeSearch);
  dom.searchInput.addEventListener('input', () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(filterSearch, 200);
  });
  // Close search on overlay click
  dom.searchModal.addEventListener('click', (e) => {
    if (e.target === dom.searchModal) closeSearch();
  });

  // Favorites modal
  dom.btnFavorites.addEventListener('click', openFavorites);
  dom.favoritesModal.querySelector('.btn-close-modal').addEventListener('click', closeFavorites);
  dom.favoritesModal.addEventListener('click', (e) => {
    if (e.target === dom.favoritesModal) closeFavorites();
  });

  // Settings
  dom.btnSettings.addEventListener('click', openSettings);
  dom.settingsModal.querySelector('.btn-close-modal').addEventListener('click', closeSettings);
  dom.settingsModal.addEventListener('click', (e) => {
    if (e.target === dom.settingsModal) closeSettings();
  });
  dom.settingToneColors.addEventListener('change', applySettings);
  dom.settingSeasonal.addEventListener('change', applySettings);
  dom.settingWriteAll.addEventListener('change', applySettings);
  dom.settingAudioSpeed.addEventListener('change', applySettings);
  dom.settingLanguage.addEventListener('change', applySettings);

  // Settings actions
  dom.btnBackup.addEventListener('click', onBackup);
  dom.btnRestore.addEventListener('click', onRestore);
  dom.btnSyncUrl.addEventListener('click', onSyncUrl);

  // Celebration
  dom.celebrationContinue.addEventListener('click', () => {
    dom.celebrationOverlay.hidden = true;
  });

  // Quiz modal
  dom.quizModal.querySelector('.btn-close-modal').addEventListener('click', closeQuiz);
  dom.quizModal.addEventListener('click', (e) => { if (e.target === dom.quizModal) closeQuiz(); });
  dom.quizNext.addEventListener('click', nextQuizQuestion);
  dom.quizDone.addEventListener('click', () => { quizIdx = quizWords.length; showQuizQuestion(); });
  dom.quizClose.addEventListener('click', closeQuiz);

  // Keyboard
  document.addEventListener('keydown', onKeyDown);

  // Pillar tabs navigation
  dom.pillarTabs.querySelectorAll('.pillar-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const phase = tab.dataset.pillar;
      // Only allow navigation to already-visited phases
      if (phase === 'shi') showPhase('shi');
      else if (phase === 'xie') {
        const state = loadState();
        if (state.progress.daily_pillar_completed.shi) showPhase('xie');
      }
      else if (phase === 'xi') {
        const state = loadState();
        if (state.progress.daily_pillar_completed.xie) showPhase('xi');
      }
    });
  });

  // Resize observer for writing canvas (debounced)
  let resizeTimer;
  const ro = new ResizeObserver(() => {
    if (resizeTimer) clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (currentPhase === 'xie' && currentWord) {
        const state = loadState();
        const writeAll = state.settings.write_all_chars !== false;
        const chars = writeAll ? [...currentWord.word] : [currentWord.word[0]];
        if (currentCharIdx < chars.length) {
          clearWriter();
          initHanziWriter(chars[currentCharIdx], currentWord.hsk_level || 1);
        }
      }
    }, 200);
  });
  ro.observe(dom.writingCanvas);
}

/* ============================================================
   Kick Off
   ============================================================ */
document.addEventListener('DOMContentLoaded', init);
