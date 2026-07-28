/* ============================================================
   Celebrations — 甲子 Yellow Dragon & Level-Transition Guardians
   ============================================================ */

/* Self-contained DOM lookups (loaded before app.js, so no dependency on 'dom' object) */
function getC() {
  return {
    overlay: document.getElementById('celebration-overlay'),
    svg: document.getElementById('celebration-svg'),
    title: document.getElementById('celebration-title'),
    body: document.getElementById('celebration-body'),
    btn: document.getElementById('celebration-continue'),
  };
}

/* Ink-wash style SVG guardians — single stroke weight, no fills,
   traditional brushwork aesthetic. */

const GUARDIANS = {
  /* 青龙 Azure Dragon — East, Wood */
  azureDragon: `
    <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g stroke="#4a9e8a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <!-- Dragon head -->
        <path d="M90 40 C85 35 75 30 70 35 C65 40 68 48 75 50"/>
        <path d="M90 40 C95 32 108 28 110 35 C112 42 105 50 95 50"/>
        <path d="M70 35 C60 28 55 20 58 15"/>
        <path d="M110 35 C118 28 125 22 120 15"/>
        <!-- Horns -->
        <path d="M70 35 C65 22 55 15 50 10"/>
        <path d="M110 35 C118 22 130 15 135 10"/>
        <!-- Eyes -->
        <circle cx="80" cy="42" r="2" fill="#4a9e8a" stroke="none"/>
        <circle cx="100" cy="42" r="2" fill="#4a9e8a" stroke="none"/>
        <!-- Snout -->
        <path d="M82 50 C85 55 90 56 95 55 C100 56 105 54 108 50"/>
        <path d="M88 52 L90 50"/>
        <path d="M98 52 L96 50"/>
        <!-- Whiskers -->
        <path d="M78 50 C70 52 60 50 55 48"/>
        <path d="M82 53 C72 56 62 56 55 54"/>
        <path d="M108 50 C115 52 125 50 130 48"/>
        <path d="M106 53 C114 56 124 56 130 54"/>
        <!-- Body (serpentine) -->
        <path d="M85 55 C80 70 60 80 50 95 C40 110 42 125 55 130 C68 135 75 125 80 115 C85 105 95 100 105 105 C115 110 118 120 125 125 C132 130 140 128 145 120 C150 112 148 100 140 95"/>
        <!-- Scales pattern -->
        <path d="M70 75 C72 72 78 72 80 75" stroke-width="1"/>
        <path d="M55 90 C57 87 63 87 65 90" stroke-width="1"/>
        <path d="M60 110 C62 107 68 107 70 110" stroke-width="1"/>
        <path d="M95 95 C97 92 103 92 105 95" stroke-width="1"/>
        <path d="M120 108 C122 105 128 105 130 108" stroke-width="1"/>
        <!-- Tail -->
        <path d="M140 95 C148 88 155 85 160 80 C162 78 165 78 165 82 C163 88 158 92 155 95" stroke-width="1.5"/>
        <!-- Legs/claws -->
        <path d="M60 95 C55 100 50 108 52 112 C54 115 58 112 60 108"/>
        <path d="M75 110 C70 115 65 122 67 126 C69 129 73 126 75 122"/>
        <path d="M125 115 C130 120 135 128 133 132 C131 135 127 132 125 128"/>
        <!-- Flame/cloud motif -->
        <path d="M55 48 C48 45 42 48 40 55" stroke-width="1" opacity="0.6"/>
        <path d="M130 48 C138 45 145 48 148 55" stroke-width="1" opacity="0.6"/>
      </g>
    </svg>`,

  /* 朱雀 Vermilion Bird — South, Fire */
  vermilionBird: `
    <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g stroke="#c4452d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <!-- Head and crest -->
        <path d="M100 35 C95 30 88 28 82 30 C78 32 75 38 78 42 C80 45 85 46 90 45"/>
        <path d="M100 35 C105 28 112 24 118 26 C122 28 125 34 122 38 C120 42 115 44 110 43"/>
        <!-- Crest feathers -->
        <path d="M82 30 C75 22 68 18 65 15" stroke-width="1.5"/>
        <path d="M100 32 C100 22 100 15 98 10" stroke-width="1.5"/>
        <path d="M118 26 C125 18 132 15 135 12" stroke-width="1.5"/>
        <!-- Eye -->
        <circle cx="95" cy="38" r="1.5" fill="#c4452d" stroke="none"/>
        <!-- Beak -->
        <path d="M78 40 C72 42 68 40 66 38"/>
        <path d="M78 40 C73 43 70 44 67 44"/>
        <!-- Neck -->
        <path d="M90 45 C85 55 75 60 70 70 C65 80 65 85 70 90"/>
        <path d="M110 43 C115 52 125 58 130 68 C135 78 135 82 130 88"/>
        <!-- Body -->
        <path d="M70 90 C55 100 40 115 35 130 C32 138 35 145 42 145 C48 145 52 140 55 135"/>
        <path d="M130 88 C145 100 158 115 162 128 C165 136 162 143 155 143 C150 143 146 138 143 133"/>
        <!-- Chest -->
        <path d="M70 90 C80 100 95 105 100 105 C105 105 115 100 130 88"/>
        <!-- Tail feathers -->
        <path d="M55 135 C45 155 35 170 30 180" stroke-width="1.5"/>
        <path d="M60 138 C55 158 50 175 48 185" stroke-width="1.5"/>
        <path d="M100 105 C98 130 95 155 92 180" stroke-width="1.5"/>
        <path d="M143 133 C153 153 162 168 168 178" stroke-width="1.5"/>
        <path d="M140 136 C148 156 155 173 158 183" stroke-width="1.5"/>
        <!-- Wings -->
        <path d="M70 95 C50 100 35 108 25 118" stroke-width="1.5"/>
        <path d="M68 100 C48 108 30 118 20 130" stroke-width="1.5"/>
        <path d="M130 95 C148 100 162 108 172 118" stroke-width="1.5"/>
        <path d="M132 100 C152 108 168 118 178 130" stroke-width="1.5"/>
        <!-- Flame accents -->
        <path d="M30 130 C25 135 22 140 25 145" stroke-width="1" opacity="0.6"/>
        <path d="M35 140 C28 145 25 150 28 155" stroke-width="1" opacity="0.6"/>
        <path d="M168 128 C173 133 176 138 173 143" stroke-width="1" opacity="0.6"/>
        <path d="M163 138 C170 143 173 148 170 153" stroke-width="1" opacity="0.6"/>
      </g>
    </svg>`,

  /* 白虎 White Tiger — West, Metal */
  whiteTiger: `
    <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g stroke="#8faacc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <!-- Head -->
        <path d="M90 45 C85 38 75 35 65 38 C58 40 52 45 50 52 C48 58 50 65 55 68"/>
        <path d="M110 45 C115 38 125 35 135 38 C142 40 148 45 150 52 C152 58 150 65 145 68"/>
        <!-- Ears -->
        <path d="M70 38 C68 28 72 22 78 25 C82 27 82 32 80 36"/>
        <path d="M130 38 C132 28 128 22 122 25 C118 27 118 32 120 36"/>
        <!-- Eyes -->
        <path d="M75 48 C78 45 85 45 88 48 C85 50 78 50 75 48" stroke-width="1.5"/>
        <path d="M125 48 C122 45 115 45 112 48 C115 50 122 50 125 48" stroke-width="1.5"/>
        <!-- Pupils -->
        <ellipse cx="81" cy="47" rx="1.5" ry="2.5" fill="#8faacc" stroke="none"/>
        <ellipse cx="119" cy="47" rx="1.5" ry="2.5" fill="#8faacc" stroke="none"/>
        <!-- Nose -->
        <path d="M98 55 L100 58 L102 55"/>
        <!-- Muzzle -->
        <path d="M92 58 C95 62 105 62 108 58"/>
        <path d="M95 60 L93 64"/>
        <path d="M105 60 L107 64"/>
        <!-- Whiskers -->
        <path d="M70 54 C60 52 50 52 45 54" stroke-width="1"/>
        <path d="M70 57 C58 58 48 58 42 61" stroke-width="1.5"/>
        <path d="M130 54 C140 52 150 52 155 54" stroke-width="1"/>
        <path d="M130 57 C142 58 152 58 158 61" stroke-width="1.5"/>
        <!-- 王 forehead mark -->
        <path d="M85 40 L93 38 L100 40" stroke-width="1.5"/>
        <path d="M90 38 L100 36 L110 38" stroke-width="1.5"/>
        <!-- Body -->
        <path d="M55 68 C45 85 35 100 30 120 C28 130 30 138 38 140"/>
        <path d="M145 68 C155 85 165 100 170 120 C172 130 170 138 162 140"/>
        <path d="M55 68 C70 75 100 80 100 80 C100 80 130 75 145 68"/>
        <!-- Stripes -->
        <path d="M48 85 C52 82 58 82 60 85" stroke-width="1"/>
        <path d="M40 100 C44 97 50 97 52 100" stroke-width="1"/>
        <path d="M152 85 C148 82 142 82 140 85" stroke-width="1"/>
        <path d="M160 100 C156 97 150 97 148 100" stroke-width="1"/>
        <!-- Front legs -->
        <path d="M55 100 C48 110 42 120 40 130 C38 135 42 138 46 136 C50 134 52 128 55 122"/>
        <path d="M145 100 C152 110 158 120 160 130 C162 135 158 138 154 136 C150 134 148 128 145 122"/>
        <!-- Tail -->
        <path d="M38 140 C30 148 22 150 18 145 C14 140 16 135 20 132" stroke-width="1.5"/>
      </g>
    </svg>`,

  /* 玄武 Black Tortoise — North, Water */
  blackTortoise: `
    <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g stroke="#3a6e8e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <!-- Shell (dome) -->
        <path d="M40 85 C35 70 40 50 60 40 C75 32 90 30 100 30 C110 30 125 32 140 40 C160 50 165 70 160 85"/>
        <!-- Shell bottom -->
        <path d="M40 85 C45 100 60 110 80 115 C90 117 110 117 120 115 C140 110 155 100 160 85"/>
        <!-- Shell pattern — hexagonal plates -->
        <path d="M70 50 C75 45 85 45 90 50 C92 55 88 60 80 60 C72 60 68 55 70 50" stroke-width="1"/>
        <path d="M100 42 C105 38 115 38 118 42 C120 47 116 52 110 52 C104 52 100 47 100 42" stroke-width="1"/>
        <path d="M125 50 C130 45 140 48 140 55 C140 60 132 62 128 58 C126 55 123 52 125 50" stroke-width="1"/>
        <path d="M60 70 C65 65 75 65 80 70 C82 75 78 80 70 80 C62 80 58 75 60 70" stroke-width="1"/>
        <path d="M100 65 C105 60 115 60 120 65 C122 70 118 75 110 75 C102 75 98 70 100 65" stroke-width="1"/>
        <path d="M135 70 C140 65 148 68 148 75 C148 80 140 82 136 78 C134 75 133 72 135 70" stroke-width="1"/>
        <path d="M80 90 C85 85 95 85 100 90 C102 95 98 100 90 100 C82 100 78 95 80 90" stroke-width="1"/>
        <path d="M115 92 C120 87 130 88 132 93 C134 98 128 102 122 100 C118 98 113 95 115 92" stroke-width="1"/>
        <!-- Head -->
        <path d="M60 85 C55 80 48 78 42 80 C36 82 32 88 34 94 C36 100 42 102 48 100"/>
        <!-- Eye -->
        <circle cx="45" cy="88" r="1.5" fill="#3a6e8e" stroke="none"/>
        <!-- Snake coiled around (the companion spirit) -->
        <path d="M140 40 C145 35 155 35 158 42 C162 50 158 58 152 60" stroke-width="1.5"/>
        <path d="M152 60 C148 62 142 58 140 52 C138 46 140 40 145 38" stroke-width="1.5"/>
        <path d="M148 45 C150 48 148 52 145 52 C142 52 140 48 142 45" stroke-width="1"/>
        <!-- Snake head rises above shell -->
        <path d="M145 38 C150 30 158 25 165 22"/>
        <path d="M165 22 C170 20 175 22 173 28 C172 32 168 33 165 30"/>
        <circle cx="170" cy="26" r="1" fill="#3a6e8e" stroke="none"/>
        <!-- Legs -->
        <path d="M55 105 C48 115 42 125 40 132 C38 136 42 138 45 136"/>
        <path d="M80 112 C75 122 70 132 68 138 C66 142 70 144 73 142"/>
        <path d="M120 112 C125 122 130 132 132 138 C134 142 130 144 127 142"/>
        <path d="M145 105 C152 115 158 125 160 132 C162 136 158 138 155 136"/>
        <!-- Tail -->
        <path d="M160 85 C168 82 175 85 178 90 C180 95 176 100 170 100"/>
      </g>
    </svg>`,

  /* 黄龙 Yellow Dragon — Center, Earth — for 甲子 celebration */
  yellowDragon: `
    <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g stroke="#d4a93b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <!-- Dragon head — more regal than Azure -->
        <path d="M85 42 C78 35 65 30 60 38 C55 45 60 55 70 58"/>
        <path d="M115 42 C122 35 135 30 140 38 C145 45 140 55 130 58"/>
        <!-- Crown/horns — five-clawed imperial dragon -->
        <path d="M65 38 C55 25 42 18 35 12" stroke-width="2"/>
        <path d="M60 35 C50 28 38 25 30 22" stroke-width="1.5"/>
        <path d="M135 38 C145 25 158 18 165 12" stroke-width="2"/>
        <path d="M140 35 C150 28 162 25 170 22" stroke-width="1.5"/>
        <!-- Mane -->
        <path d="M70 40 C65 30 58 25 52 20" stroke-width="1" opacity="0.7"/>
        <path d="M130 40 C135 30 142 25 148 20" stroke-width="1" opacity="0.7"/>
        <!-- Eyes — wide and wise -->
        <ellipse cx="80" cy="46" rx="4" ry="3"/>
        <ellipse cx="120" cy="46" rx="4" ry="3"/>
        <circle cx="80" cy="46" r="1.5" fill="#d4a93b" stroke="none"/>
        <circle cx="120" cy="46" r="1.5" fill="#d4a93b" stroke="none"/>
        <!-- Eyebrows -->
        <path d="M70 40 C75 37 85 37 90 40" stroke-width="1.5"/>
        <path d="M110 40 C115 37 125 37 130 40" stroke-width="1.5"/>
        <!-- Snout -->
        <path d="M88 55 C90 62 95 65 100 65 C105 65 110 62 112 55"/>
        <path d="M95 60 L98 58"/>
        <path d="M105 60 L102 58"/>
        <!-- Whiskers -->
        <path d="M78 55 C65 58 50 55 40 50" stroke-width="1.5"/>
        <path d="M82 60 C68 65 52 65 42 62" stroke-width="1.5"/>
        <path d="M122 55 C135 58 150 55 160 50" stroke-width="1.5"/>
        <path d="M118 60 C132 65 148 65 158 62" stroke-width="1.5"/>
        <!-- Body — powerful S-curve -->
        <path d="M70 62 C55 80 40 95 45 115 C50 135 65 140 80 135 C95 130 105 115 110 100 C115 85 125 78 140 82 C155 86 158 98 155 110 C152 122 145 128 138 132"/>
        <!-- Scales -->
        <path d="M62 80 C65 77 72 77 75 80" stroke-width="1"/>
        <path d="M50 100 C53 97 60 97 63 100" stroke-width="1"/>
        <path d="M55 120 C58 117 65 117 68 120" stroke-width="1"/>
        <path d="M90 108 C93 105 100 105 103 108" stroke-width="1"/>
        <path d="M118 90 C121 87 128 87 131 90" stroke-width="1"/>
        <path d="M142 100 C145 97 152 97 155 100" stroke-width="1"/>
        <!-- Four claws (imperial) -->
        <path d="M55 105 C48 112 42 120 44 126 C46 130 50 128 52 124" stroke-width="1.5"/>
        <path d="M60 128 C54 134 48 142 50 148 C52 152 56 150 58 146" stroke-width="1.5"/>
        <path d="M140 96 C148 100 155 106 153 112 C151 116 147 114 145 110" stroke-width="1.5"/>
        <path d="M148 110 C154 114 160 120 158 126 C156 130 152 128 150 124" stroke-width="1.5"/>
        <!-- Tail -->
        <path d="M138 132 C145 138 155 140 160 135 C165 130 162 124 158 120"/>
        <!-- Pearl / flame pearl -->
        <circle cx="100" cy="42" r="8" stroke="#d4a93b" stroke-width="1" fill="none" opacity="0.4"/>
        <circle cx="100" cy="42" r="3" fill="#d4a93b" opacity="0.6" stroke="none"/>
        <!-- Auspicious cloud wisps -->
        <path d="M30 18 C25 22 20 28 24 32 C28 36 35 34 38 30 C41 26 38 20 34 18" stroke-width="1" opacity="0.4"/>
        <path d="M160 20 C165 24 172 28 175 24 C178 20 175 15 170 14" stroke-width="1" opacity="0.4"/>
        <path d="M22 55 C18 60 14 65 18 70 C22 75 28 72 30 68" stroke-width="1" opacity="0.3"/>
        <path d="M175 55 C180 60 185 65 182 70 C178 75 172 72 170 68" stroke-width="1" opacity="0.3"/>
      </g>
    </svg>`
};

/* Level-transition data */
const LEVEL_TRANSITIONS = [
  { from_lvl: null, to_lvl: 1, tier: 'wood', name: 'HSK 1', element: '木 Wood',
    guardian: 'azureDragon', message: 'Learning begins — the Wood element awakens.' },
  { from_lvl: 2, to_lvl: 3, tier: 'fire', name: 'HSK 3', element: '火 Fire',
    guardian: 'vermilionBird', message: 'The Fire element ignites — your words have warmth.' },
  { from_lvl: 4, to_lvl: 5, tier: 'earth', name: 'HSK 5', element: '土 Earth',
    guardian: null, message: 'The Earth element — steady and grounded.',
    note: 'Earth uses the Yellow Dragon (shared with jiazi) or no guardian.' },
  { from_lvl: 5, to_lvl: 6, tier: 'metal', name: 'HSK 6', element: '金 Metal',
    guardian: 'whiteTiger', message: 'The Metal element — refined and precise.' },
  { from_lvl: 6, to_lvl: 7, tier: 'water', name: 'HSK 7-9', element: '水 Water',
    guardian: 'blackTortoise', message: 'The Water element — deep and boundless.' },
];

function getGuardianSVG(name) {
  return GUARDIANS[name] || '';
}

function getLevelTransition(dayOffset) {
  for (const t of LEVEL_TRANSITIONS) {
    if (t.from_lvl === null && t.to_lvl === 1) {
      // First word of HSK 1 = dayOffset 0
      if (dayOffset === 0) return t;
    } else {
      // Check if this dayOffset is the first word of the new level
      const boundary = LEVEL_BOUNDARIES.find(b => b.level === `hsk${t.to_lvl}` ||
        (t.to_lvl === 7 && b.level === 'hsk79'));
      if (boundary && dayOffset === boundary.start) return t;
    }
  }
  return null;
}

function showJiaziCelebration(cycleNum, dayOffset, wordsSeen) {
  const c = getC();
  c.overlay.hidden = false;
  c.svg.innerHTML = getGuardianSVG('yellowDragon');
  c.title.textContent = `甲子完成 #${cycleNum}`;
  c.body.innerHTML = `
    <p>Congratulations — you completed your ${ordinal(cycleNum)} jiazi cycle!</p>
    <p style="color:var(--fg);margin-top:12px;">${dayOffset + 1} 天 · ${wordsSeen} 字</p>
    <p style="color:var(--fg-soft);font-size:13px;margin-top:8px;">The Yellow Dragon honors your dedication.</p>`;
}

function showLevelTransition(transition, levelName) {
  const c = getC();
  const svg = transition.guardian ? getGuardianSVG(transition.guardian) : getGuardianSVG('yellowDragon');
  c.overlay.hidden = false;
  c.svg.innerHTML = svg;
  c.title.textContent = `${levelName} · ${transition.element}`;
  c.body.innerHTML = `
    <p>${transition.message}</p>
    <p style="color:var(--fg-soft);font-size:13px;margin-top:8px;">You've entered a new element on your journey.</p>`;
}

function ordinal(n) {
  const s = ['th', 'st', 'nd', 'rd'];
  const v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
}
