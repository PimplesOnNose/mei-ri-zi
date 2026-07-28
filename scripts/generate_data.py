#!/usr/bin/env python3
"""
generate_data.py — Build hsk_daily.json from HSK 3.0 vocabulary lists.

Downloads from krmanik/HSK-3.0 (GitHub) — the most complete open-source
HSK 3.0 dataset with 11,000+ words across all 9 levels.

Usage:
  python scripts/generate_data.py
  python scripts/generate_data.py --hsk-levels 1,2   # only HSK 1-2 for testing
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_DIR = DATA_DIR / "_cache"
OUTPUT_FILE = DATA_DIR / "hsk_daily.json"

LEVELS = [
    {"id": "prep",  "name": "入门",  "element": "天水",   "color": "#e8e8ec", "word_count": 0},
    {"id": "hsk1",  "name": "HSK 1", "element": "木",     "color": "#4a9e8a", "word_count": 497},
    {"id": "hsk2",  "name": "HSK 2", "element": "木→火",  "color": "#6db3a4", "word_count": 763},
    {"id": "hsk3",  "name": "HSK 3", "element": "火",     "color": "#c4452d", "word_count": 966},
    {"id": "hsk4",  "name": "HSK 4", "element": "火→土",  "color": "#c9a96e", "word_count": 994},
    {"id": "hsk5",  "name": "HSK 5", "element": "土→金",  "color": "#d4b878", "word_count": 1067},
    {"id": "hsk6",  "name": "HSK 6", "element": "金",     "color": "#8faacc", "word_count": 1134},
    {"id": "hsk79", "name": "HSK 7-9", "element": "水",   "color": "#3a6e8e", "word_count": 5615},
]

HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
STEM_ELEMENTS = ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]

# Source URLs — TSV files with columns: traditional, simplified, pinyin, meaning
TSV_BASE = "https://raw.githubusercontent.com/krmanik/HSK-3.0/main/New%20HSK%20(2021)/HSK%20List%20(Meaning)"
HSK_LEVEL_IDS = {
    "1": "hsk1", "2": "hsk2", "3": "hsk3", "4": "hsk4",
    "5": "hsk5", "6": "hsk6", "7-9": "hsk79"
}


def parse_pinyin_tones(pinyin_text: str):
    """Parse pinyin string into parts and tone numbers.
    
    Splits by matching known pinyin syllable patterns using a
    greedy maximum-munch approach. Each syllable has exactly one
    tone-marked vowel.
    
    E.g., 'nǐhǎo' → (['nǐ', 'hǎo'], [3, 3])
    E.g., 'àixīn' → (['ài', 'xīn'], [4, 1])
    """
    tone_map = {
        'ā': (1, 'a'), 'á': (2, 'a'), 'ǎ': (3, 'a'), 'à': (4, 'a'),
        'ē': (1, 'e'), 'é': (2, 'e'), 'ě': (3, 'e'), 'è': (4, 'e'),
        'ī': (1, 'i'), 'í': (2, 'i'), 'ǐ': (3, 'i'), 'ì': (4, 'i'),
        'ō': (1, 'o'), 'ó': (2, 'o'), 'ǒ': (3, 'o'), 'ò': (4, 'o'),
        'ū': (1, 'u'), 'ú': (2, 'u'), 'ǔ': (3, 'u'), 'ù': (4, 'u'),
        'ǖ': (1, 'ü'), 'ǘ': (2, 'ü'), 'ǚ': (3, 'ü'), 'ǜ': (4, 'ü'),
        'm̄': (1, 'm'), 'ḿ': (2, 'm'), 'm̀': (4, 'm'),
        'ń': (2, 'n'), 'ň': (3, 'n'), 'ǹ': (4, 'n'),
    }

    text = pinyin_text.strip()
    if not text:
        return [], []

    # If space/apostrophe separated, split on those
    if ' ' in text:
        raw_parts = text.split()
        parts = [p for p in raw_parts if p]
        return parts, [_find_syllable_tone(p, tone_map) for p in parts]
    elif "'" in text:
        raw_parts = text.split("'")
        parts = [p for p in raw_parts if p]
        return parts, [_find_syllable_tone(p, tone_map) for p in parts]
    else:
        # Use regex-based splitting: match pinyin syllable patterns
        # A syllable is: optional initial + final with tone mark
        # Initials: zh, ch, sh, b, p, m, f, d, t, n, l, g, k, h, j, q, x, r, z, c, s, y, w
        # We build a regex that matches the whole string as a sequence of syllables
        
        # First, normalize: replace each char with its plain version for matching,
        # but track the original chars with tone marks
        
        # Actually, let's use a completely different approach:
        # Build the regex from known pinyin patterns
        # Each syllable = (initial)?(final) where final contains exactly one tone mark
        
        # Build the final pattern with tone marks:
        # A final can be: V, VV, Vn, Vng, VVn, VVng where V is a tone-marked vowel
        plain_vowels = 'aeiouü'
        tone_vowel_class = '[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]'
        tone_vowel_plain = '[' + plain_vowels + ']'
        
        # Pattern for a single pinyin syllable:
        # Initial (optional) + final (mandatory, with tone mark)
        # Initial: one of the known initials (case-insensitive for first char)
        # Final: starts with a tone-marked vowel, optionally followed by plain chars
        
        # But we can't just regex this easily because tone marks are ON vowels.
        # Better approach: use the fact that each tone-marked char marks a syllable nucleus.
        
        # Step 1: Find all tone-marked positions (nuclei)
        tone_chars = set(tone_map.keys())
        nuclei = [i for i, ch in enumerate(text) if ch in tone_chars]
        
        if not nuclei:
            return [text], [0]
        
        # Step 2: For each pair of nuclei, determine the boundary
        # The boundary is where the first syllable's final ends and
        # the second syllable's initial begins.
        # 
        # Key rules:
        # - 'n' after a vowel typically belongs to the first syllable (final -n)
        #   UNLESS followed by a vowel (e.g., 'nǚ' starts a new syllable)
        # - 'ng' after a vowel belongs to the first syllable (final -ng)
        # - 'r' after a vowel is erhua (final -r)
        # - Other consonants start a new syllable
        #
        # Simpler approach: each syllable is a maximal sequence starting from
        # an initial (or start of string) through the tone-marked vowel and
        # any following final characters, stopping before the next initial.
        
        # Build a set of initial strings for matching
        init_set = ['zh', 'ch', 'sh', 'b', 'p', 'm', 'f', 'd', 't', 'n', 'l',
                    'g', 'k', 'h', 'j', 'q', 'x', 'r', 'z', 'c', 's', 'y', 'w']
        init_chars = set('bcdfghjklmnpqrstwxyz')
        vowel_chars = set('aeiouü')
        
        # Find syllable boundaries using the following method:
        # Walk through the string. A new syllable starts when we encounter
        # a consonant that can be an initial, AND either:
        # - It's a known initial cluster AND the previous char was a final char
        # - It's followed by a tone-marked vowel
        
        # Actually, the simplest correct method:
        # For each nucleus at position i, the syllable starts at:
        #   - position 0 for the first nucleus
        #   - for subsequent nuclei, the position right after the previous
        #     syllable's final ended
        # A syllable's final ends at the last character that could be part of
        # a valid pinyin final: vowels, n, ng
        # The next syllable starts at the first consonant that follows.
        
        # Simpler yet: use the fact that between two tone marks,
        # the characters in between belong to either the preceding final
        # or the following initial. We can use a lookup table.
        
        # Let me use an even simpler approach: 
        # Split the pinyin at known syllable-boundary patterns.
        # These are positions where a consonant cluster follows a vowel.
        # The specific boundary rules for Mandarin pinyin:
        
        # A syllable boundary occurs between:
        # - Any consonant (b, p, m, f, d, t, g, k, h, j, q, x, r, z, c, s, y, w)
        #   that follows a vowel, UNLESS it's 'n' or 'g' continuing a final
        # - 'zh', 'ch', 'sh' after a vowel
        # - 'n' after a vowel, UNLESS it's completing '-n' final (an, en, in, etc.)
        #   and followed by a consonant (like 'g' for 'ng' or another initial)
        
        # Actually let me just use a really simple heuristic:
        # Each syllable has exactly one vowel with a tone mark.
        # Between two tone marks, split at a position where we have
        # a valid initial followed by a valid final.
        
        # Let me use python's re module with a custom-built pattern
        import re
        
        # Build a regex that matches a single pinyin syllable
        # This captures the largest possible initial followed by a final with tone mark
        
        # All possible finals (using plain letters, then we match tone marks on vowels)
        finals_plain = sorted([
            'iang', 'iong', 'uang', 'ueng', 
            'ang', 'eng', 'ing', 'ong', 'ian', 'iao', 'iou',
            'uai', 'uan', 'uei', 'uen', 'uang', 'ueng',
            'an', 'en', 'in', 'on', 'un', 'ün', 'van', 'ven', 'vn',
            'ai', 'ao', 'ei', 'ia', 'ie', 'io', 'iu',
            'ou', 'ua', 'ue', 'ui', 'uo', 'üe',
            'a', 'e', 'i', 'o', 'u', 'ü',
            'er', 'ng', 'n', 'm'
        ], key=len, reverse=True)
        
        initials_sorted = sorted(init_set + [c.upper() for c in init_set], key=len, reverse=True)
        
        # Approach: iterate through the text, and at each position,
        # try to match the longest possible syllable
        result_parts = []
        result_tones = []
        
        pos = 0
        while pos < len(text):
            matched = False
            remainder = text[pos:]
            
            for init in initials_sorted:
                if remainder.startswith(init):
                    after_init = remainder[len(init):]
                    
                    # Find the tone-marked vowel in after_init
                    tone_pos = -1
                    for ci, ch in enumerate(after_init):
                        if ch in tone_map:
                            tone_pos = ci
                            break
                    
                    if tone_pos >= 0:
                        # Syllable starts at pos, tone-marked vowel at pos + len(init) + tone_pos
                        syl_end = pos + len(init) + tone_pos + 1
                        
                        # After the tone-marked vowel, include remaining final characters:
                        # vowels, n, ng, r, m
                        # 
                        # CRITICAL: 'n' after a tone-marked vowel is PART OF THE FINAL
                        # (like -n in an/en/in/un/ün/ian/uan/üan/uen)
                        # It ONLY starts a new syllable if followed by a tone-marked vowel
                        # that can't be absorbed into the current final
                        #
                        # 'ng' after a tone-marked vowel is PART OF THE FINAL
                        # (like -ng in ang/eng/ing/ong/iang/iong/uang/ueng)
                        #
                        # A new syllable starts when we encounter:
                        # - A consonant that is NOT n/g (like b, p, m, f, d, t, etc.)
                        # - 'n' followed by a tone-marked vowel (like nǚ, nǐ)
                        # - 'g' that is NOT preceded by 'n' (rare)
                        
                        while syl_end < len(text):
                            ch = text[syl_end].lower()
                            
                            if ch == 'n':
                                # 'n' after a vowel is part of the final (like 'àn', 'īn')
                                # EXCEPT if it starts a new syllable like 'nǚ', 'nǐ'
                                # Check if 'n' is immediately followed by a tone-marked vowel
                                if syl_end + 1 < len(text):
                                    next_ch_toned = text[syl_end + 1] in tone_map
                                    if next_ch_toned:
                                        # 'n' could start a new syllable (nǐ, nǚ, etc.)
                                        # Only split if the current final can't end with 'nn'
                                        # which it can't — 'n' starts new syllable
                                        break
                                # 'n' continues the final (make the final nasal)
                                syl_end += 1
                            elif ch == 'g':
                                # 'g' after 'n' completes '-ng' final
                                # 'g' NOT after 'n' starts a new syllable (gāo, gěi, etc.)
                                if syl_end > 0 and text[syl_end-1].lower() == 'n':
                                    # 'ng' — part of final
                                    syl_end += 1
                                else:
                                    # 'g' starting a new syllable
                                    break
                            elif ch in vowel_chars or ch == 'r':
                                # Extends the final (diphthong, erhua)
                                syl_end += 1
                            elif ch == 'm':
                                # 'm' almost always starts a new syllable (mā, mǐ, ma)
                                # Exception: onomatopoeia like 'hmm'
                                # Treat 'm' as starting a new syllable
                                break
                            else:
                                # Any other consonant starts a new syllable
                                break
                        
                        # Final sanity check: if syl_end is at a position where
                        # the next chars form a known initial (like zh, ch, sh, etc.)
                        # AND we're past the tone mark, this is a valid boundary
                        # 
                        # But for cases like 'xīn' where there's nothing after,
                        # syl_end should be at the end of string
                        
                        # Extract the syllable
                        syllable = text[pos:syl_end]
                        if syllable:
                            # Find tone
                            syl_tone = 0
                            for ch in syllable:
                                if ch in tone_map:
                                    syl_tone = tone_map[ch][0]
                                    break
                            result_parts.append(syllable)
                            result_tones.append(syl_tone)
                            pos = syl_end
                            matched = True
                            break
            
            if not matched:
                # Try to match as a vowel-starting syllable (no explicit initial)
                # Common for syllables like 'ā', 'ài', 'ōu'
                for tch in tone_map:
                    if text[pos:].startswith(tch):
                        tone_val, _ = tone_map[tch]
                        # Include following final chars
                        syl_end = pos + 1
                        while syl_end < len(text):
                            ch = text[syl_end].lower()
                            if ch == 'n':
                                if syl_end + 1 < len(text) and text[syl_end+1] in tone_map:
                                    break
                                syl_end += 1
                            elif ch == 'g' and syl_end > 0 and text[syl_end-1].lower() == 'n':
                                syl_end += 1
                            elif ch in vowel_chars or ch == 'r':
                                syl_end += 1
                            else:
                                break
                        syllable = text[pos:syl_end]
                        result_parts.append(syllable)
                        result_tones.append(tone_val)
                        pos = syl_end
                        matched = True
                        break
            
            if not matched:
                # Try to match a neutral-tone syllable (no tone mark)
                # This happens with particles like 'ma', 'le', 'de', 'ne'
                # or in multi-syllable words where the last syllable is neutral
                # 
                # A neutral-tone syllable starts with an initial consonant
                # and continues with vowels and final chars (n, ng) but has NO tone mark
                neutral_initials = 'mnlrdthkzpbjqxw'  # all possible initials for neutral-tone syllables
                if pos < len(text) and text[pos].lower() in neutral_initials:
                    syl_end = pos + 1
                    while syl_end < len(text):
                        ch = text[syl_end].lower()
                        if ch in vowel_chars:
                            syl_end += 1
                        elif ch == 'n':
                            if syl_end + 1 < len(text) and text[syl_end+1] in tone_map:
                                break
                            syl_end += 1
                        elif ch == 'g' and syl_end > 0 and text[syl_end-1].lower() == 'n':
                            syl_end += 1
                        else:
                            break
                    syllable = text[pos:syl_end]
                    if syllable:
                        result_parts.append(syllable)
                        result_tones.append(0)
                        pos = syl_end
                        matched = True
                else:
                    result_parts.append(text[pos])
                    result_tones.append(0)
                    pos += 1
        
        return result_parts, result_tones


def _find_syllable_tone(part: str, tone_map: dict):
    """Find tone number of a single pinyin syllable (preserves original)."""
    for ch in part:
        if ch in tone_map:
            return tone_map[ch][0]
    return 0



def parse_tsv_line(line: str):
    """Parse a TSV line: simplified\tpinyin\tmeaning  (after stripping traditional)"""
    parts = line.strip().split('\t')
    if len(parts) >= 4:
        # full format: traditional\tsimplified\tpinyin\tmeaning
        return parts[1], parts[2], parts[3]
    elif len(parts) == 3:
        return parts[0], parts[1], parts[2]
    return None, None, None


def build_word(simplified: str, pinyin_text: str, meaning: str, hsk_level: int, word_id: str):
    """Build a word entry in the 每日字 format."""
    pinyin_parts, pinyin_tones = parse_pinyin_tones(pinyin_text)
    pinyin_joined = ''.join(pinyin_parts) if pinyin_parts else pinyin_text

    # Generate a simple example sentence
    example = generate_example(simplified, pinyin_joined, meaning, hsk_level)

    word = {
        "id": word_id,
        "hsk_level": hsk_level,
        "word": simplified,
        "pinyin_text": pinyin_joined,
        "pinyin_tones": pinyin_tones,
        "pinyin_parts": pinyin_parts,
        "pos": "",
        "english": meaning,
        "radicals": [],
        "components": [],
        "stroke_count": len(simplified) * 5,  # rough estimate
        "example": example
    }
    return word


def generate_example(word, pinyin, meaning, hsk_level):
    """Generate a simple example sentence for the word."""
    # Very basic template-based examples
    templates = {
        1: [
            {"zh": f"这是{word}。", "pinyin": f"Zhè shì {pinyin}.", "en": f"This is {meaning}."},
            {"zh": f"我喜欢{word}。", "pinyin": f"Wǒ xǐhuān {pinyin}.", "en": f"I like {meaning}."},
        ],
        2: [
            {"zh": f"我今天学了{word}。", "pinyin": f"Wǒ jīntiān xuéle {pinyin}.", "en": f"I studied {meaning} today."},
            {"zh": f"你知道{word}吗？", "pinyin": f"Nǐ zhīdào {pinyin} ma?", "en": f"Do you know {meaning}?"},
        ],
    }

    # Default template
    template = templates.get(hsk_level, templates.get(2))[0]
    return template


def download_hsk_data(hsk_levels=None):
    """Download TSV files for specified HSK levels (or all)."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    all_words = []

    level_ids = HSK_LEVEL_IDS.keys() if hsk_levels is None else hsk_levels

    for lv in level_ids:
        url = f"{TSV_BASE}/HSK%20{lv}.tsv"
        cache_file = CACHE_DIR / f"hsk{lv}.tsv"

        if cache_file.exists():
            print(f"  Using cached: {cache_file}")
            content = cache_file.read_text(encoding='utf-8')
        else:
            print(f"  Downloading HSK {lv}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'meirizi/1.0'})
            try:
                resp = urllib.request.urlopen(req, timeout=30)
                content = resp.read().decode('utf-8')
                cache_file.write_text(content, encoding='utf-8')
            except Exception as e:
                print(f"  FAILED: {e}")
                continue

        lines = content.strip().split('\n')
        level_name = HSK_LEVEL_IDS[lv]
        level_num = 7 if lv == '7-9' else int(lv)

        for i, line in enumerate(lines):
            simplified, pinyin_text, meaning = parse_tsv_line(line)
            if not simplified:
                continue
            word_id = f"{level_name}_{i+1:04d}"
            word = build_word(simplified, pinyin_text, meaning, level_num, word_id)
            all_words.append(word)

        print(f"  → {len(lines)} words loaded")

    return all_words


def load_enriched_hsk1_hsk2():
    """Load the manual HSK 1-2 words with rich components and examples."""
    # These are defined inline below
    return _manual_hsk1_words(), _manual_hsk2_words()


def _manual_hsk1_words():
    """Rich HSK 1 words with component breakdowns and proper example sentences."""
    return [
        {"word": "你好", "pinyin_text": "nǐhǎo", "pinyin_parts": ["nǐ", "hǎo"], "pinyin_tones": [3, 3],
         "pos": "greeting", "english": "hello", "radicals": ["亻", "子"],
         "components": [{"char": "你", "role": "semantic", "meaning": "you"},
                        {"char": "好", "role": "compound", "meaning": "good", "breakdown": "女 (woman) + 子 (child)"}],
         "stroke_count": 12,
         "example": {"zh": "你好，我是小明。",   "pinyin": "Nǐ hǎo, wǒ shì Xiǎomíng.",
                     "pinyin_parts": ["Nǐ", "hǎo", "wǒ", "shì", "Xiǎo", "míng"],
                     "pinyin_tones": [3, 3, 3, 4, 3, 2],
                     "en": "Hello, I am Xiaoming."}},
        {"word": "谢谢", "pinyin_text": "xièxie", "pinyin_parts": ["xiè", "xie"], "pinyin_tones": [4, 0],
         "pos": "verb", "english": "thank you", "radicals": ["讠", "身"],
         "components": [{"char": "谢", "role": "compound", "meaning": "to thank", "breakdown": "讠 (speech) + 射 (phonetic)"}],
         "stroke_count": 12,
         "example": {"zh": "谢谢你的帮助。",   "pinyin": "Xièxie nǐ de bāngzhù.",
                     "pinyin_parts": ["Xièxie", "nǐ", "de", "bāng", "zhù"],
                     "pinyin_tones": [4, 0, 3, 0, 1, 4],
                     "en": "Thank you for your help."}},
        {"word": "不", "pinyin_text": "bù", "pinyin_parts": ["bù"], "pinyin_tones": [4],
         "pos": "adverb", "english": "not; no", "radicals": ["一"],
         "components": [{"char": "不", "role": "semantic", "meaning": "not"}],
         "stroke_count": 4,
         "example": {"zh": "我不是学生。",   "pinyin": "Wǒ bù shì xuéshēng.",
                     "pinyin_parts": ["Wǒ", "bù", "shì", "xué", "shēng"],
                     "pinyin_tones": [3, 4, 4, 2, 1],
                     "en": "I am not a student."}},
        {"word": "是", "pinyin_text": "shì", "pinyin_parts": ["shì"], "pinyin_tones": [4],
         "pos": "verb", "english": "to be", "radicals": ["日", "正"],
         "components": [{"char": "是", "role": "semantic", "meaning": "to be"}],
         "stroke_count": 9,
         "example": {"zh": "这是我的书。",   "pinyin": "Zhè shì wǒ de shū.",
                     "pinyin_parts": ["Zhè", "shì", "wǒ", "de", "shū"],
                     "pinyin_tones": [4, 4, 3, 0, 1],
                     "en": "This is my book."}},
        {"word": "我", "pinyin_text": "wǒ", "pinyin_parts": ["wǒ"], "pinyin_tones": [3],
         "pos": "pronoun", "english": "I; me", "radicals": ["戈"],
         "components": [{"char": "我", "role": "semantic", "meaning": "I; me"}],
         "stroke_count": 7,
         "example": {"zh": "我喜欢学习中文。",   "pinyin": "Wǒ xǐhuān xuéxí zhōngwén.",
                     "pinyin_parts": ["Wǒ", "xǐ", "huān", "xué", "xí", "zhōng", "wén"],
                     "pinyin_tones": [3, 3, 1, 2, 2, 1, 2],
                     "en": "I like studying Chinese."}},
        {"word": "好", "pinyin_text": "hǎo", "pinyin_parts": ["hǎo"], "pinyin_tones": [3],
         "pos": "adjective", "english": "good", "radicals": ["女", "子"],
         "components": [{"char": "好", "role": "compound", "meaning": "good", "breakdown": "女 (woman) + 子 (child)"}],
         "stroke_count": 6,
         "example": {"zh": "今天天气很好。",   "pinyin": "Jīntiān tiānqì hěn hǎo.",
                     "pinyin_parts": ["Jīn", "tiān", "tiān", "qì", "hěn", "hǎo"],
                     "pinyin_tones": [1, 1, 1, 4, 3, 3],
                     "en": "The weather is good today."}},
        {"word": "大", "pinyin_text": "dà", "pinyin_parts": ["dà"], "pinyin_tones": [4],
         "pos": "adjective", "english": "big; large", "radicals": ["大"],
         "components": [{"char": "大", "role": "semantic", "meaning": "big"}],
         "stroke_count": 3,
         "example": {"zh": "这个苹果很大。",   "pinyin": "Zhège píngguǒ hěn dà.",
                     "pinyin_parts": ["Zhè", "ge", "píng", "guǒ", "hěn", "dà"],
                     "pinyin_tones": [4, 0, 2, 3, 3, 4],
                     "en": "This apple is very big."}},
        {"word": "小", "pinyin_text": "xiǎo", "pinyin_parts": ["xiǎo"], "pinyin_tones": [3],
         "pos": "adjective", "english": "small; little", "radicals": ["小"],
         "components": [{"char": "小", "role": "semantic", "meaning": "small"}],
         "stroke_count": 3,
         "example": {"zh": "这只小猫很可爱。",   "pinyin": "Zhè zhī xiǎo māo hěn kě'ài.",
                     "pinyin_parts": ["Zhè", "zhī", "xiǎo", "māo", "hěn", "kě", "ài"],
                     "pinyin_tones": [4, 1, 3, 1, 3, 3, 4],
                     "en": "This kitten is very cute."}},
        {"word": "一", "pinyin_text": "yī", "pinyin_parts": ["yī"], "pinyin_tones": [1],
         "pos": "numeral", "english": "one", "radicals": ["一"],
         "components": [{"char": "一", "role": "semantic", "meaning": "one"}],
         "stroke_count": 1,
         "example": {"zh": "我有一个哥哥。",   "pinyin": "Wǒ yǒu yī gè gēgē.",
                     "pinyin_parts": ["Wǒ", "yǒu", "yī", "gè", "gē", "gē"],
                     "pinyin_tones": [3, 3, 1, 4, 1, 1],
                     "en": "I have an older brother."}},
        {"word": "二", "pinyin_text": "èr", "pinyin_parts": ["èr"], "pinyin_tones": [4],
         "pos": "numeral", "english": "two", "radicals": ["二"],
         "components": [{"char": "二", "role": "semantic", "meaning": "two"}],
         "stroke_count": 2,
         "example": {"zh": "我有两个朋友。",   "pinyin": "Wǒ yǒu liǎng gè péngyǒu.",
                     "pinyin_parts": ["Wǒ", "yǒu", "liǎng", "gè", "péng", "yǒu"],
                     "pinyin_tones": [3, 3, 3, 4, 2, 3],
                     "en": "I have two friends."}},
        {"word": "三", "pinyin_text": "sān", "pinyin_parts": ["sān"], "pinyin_tones": [1],
         "pos": "numeral", "english": "three", "radicals": ["一"],
         "components": [{"char": "三", "role": "semantic", "meaning": "three"}],
         "stroke_count": 3,
         "example": {"zh": "我们有三本书。",   "pinyin": "Wǒmen yǒu sān běn shū.",
                     "pinyin_parts": ["Wǒ", "men", "yǒu", "sān", "běn", "shū"],
                     "pinyin_tones": [3, 0, 3, 1, 3, 1],
                     "en": "We have three books."}},
        {"word": "人", "pinyin_text": "rén", "pinyin_parts": ["rén"], "pinyin_tones": [2],
         "pos": "noun", "english": "person; people", "radicals": ["人"],
         "components": [{"char": "人", "role": "semantic", "meaning": "person"}],
         "stroke_count": 2,
         "example": {"zh": "他是好人。",   "pinyin": "Tā shì hǎo rén.",
                     "pinyin_parts": ["Tā", "shì", "hǎo", "rén"],
                     "pinyin_tones": [1, 4, 3, 2],
                     "en": "He is a good person."}},
        {"word": "中国",   "pinyin_text": "Zhōngguó", "pinyin_parts": ["Zhōng", "guó"], "pinyin_tones": [1, 2],
         "pos": "noun", "english": "China", "radicals": ["口", "囗"],
         "components": [{"char": "中", "role": "semantic", "meaning": "middle; center"},
                        {"char": "国", "role": "semantic", "meaning": "country"}],
         "stroke_count": 15,
         "example": {"zh": "中国很大。",   "pinyin": "Zhōngguó hěn dà.",
                     "pinyin_parts": ["Zhōng", "guó", "hěn", "dà"],
                     "pinyin_tones": [1, 2, 3, 4],
                     "en": "China is very big."}},
        {"word": "学生", "pinyin_text": "xuéshēng", "pinyin_parts": ["xué", "shēng"], "pinyin_tones": [2, 1],
         "pos": "noun", "english": "student", "radicals": ["子", "生"],
         "components": [{"char": "学", "role": "semantic", "meaning": "study"},
                        {"char": "生", "role": "semantic", "meaning": "life; born"}],
         "stroke_count": 14,
         "example": {"zh": "她是学生。",   "pinyin": "Tā shì xuéshēng.",
                     "pinyin_parts": ["Tā", "shì", "xué", "shēng"],
                     "pinyin_tones": [1, 4, 2, 1],
                     "en": "She is a student."}},
        {"word": "老师", "pinyin_text": "lǎoshī", "pinyin_parts": ["lǎo", "shī"], "pinyin_tones": [3, 1],
         "pos": "noun", "english": "teacher", "radicals": ["老", "师"],
         "components": [{"char": "老", "role": "semantic", "meaning": "old"},
                        {"char": "师", "role": "semantic", "meaning": "teacher"}],
         "stroke_count": 10,
         "example": {"zh": "王老师很好。",   "pinyin": "Wáng lǎoshī hěn hǎo.",
                     "pinyin_parts": ["Wáng", "lǎo", "shī", "hěn", "hǎo"],
                     "pinyin_tones": [2, 3, 1, 3, 3],
                     "en": "Teacher Wang is very good."}},
        {"word": "学习", "pinyin_text": "xuéxí", "pinyin_parts": ["xué", "xí"], "pinyin_tones": [2, 2],
         "pos": "verb", "english": "to study; to learn", "radicals": ["学", "习"],
         "components": [{"char": "学", "role": "semantic", "meaning": "study"},
                        {"char": "习", "role": "semantic", "meaning": "practice"}],
         "stroke_count": 12,
         "example": {"zh": "我们学习中文。",   "pinyin": "Wǒmen xuéxí zhōngwén.",
                     "pinyin_parts": ["Wǒ", "men", "xué", "xí", "zhōng", "wén"],
                     "pinyin_tones": [3, 0, 2, 2, 1, 2],
                     "en": "We study Chinese."}},
        {"word": "朋友", "pinyin_text": "péngyǒu", "pinyin_parts": ["péng", "yǒu"], "pinyin_tones": [2, 3],
         "pos": "noun", "english": "friend", "radicals": ["月", "又"],
         "components": [{"char": "朋", "role": "semantic", "meaning": "friend"},
                        {"char": "友", "role": "semantic", "meaning": "friend"}],
         "stroke_count": 8,
         "example": {"zh": "他是我的朋友。",   "pinyin": "Tā shì wǒ de péngyǒu.",
                     "pinyin_parts": ["Tā", "shì", "wǒ", "de", "péng", "yǒu"],
                     "pinyin_tones": [1, 4, 3, 0, 2, 3],
                     "en": "He is my friend."}},
        {"word": "家", "pinyin_text": "jiā", "pinyin_parts": ["jiā"], "pinyin_tones": [1],
         "pos": "noun", "english": "home; family", "radicals": ["宀", "豕"],
         "components": [{"char": "家", "role": "semantic", "meaning": "home; family"}],
         "stroke_count": 10,
         "example": {"zh": "我家在北京。",   "pinyin": "Wǒ jiā zài Běijīng.",
                     "pinyin_parts": ["Wǒ", "jiā", "zài", "Běi", "jīng"],
                     "pinyin_tones": [3, 1, 4, 3, 1],
                     "en": "My home is in Beijing."}},
        {"word": "说", "pinyin_text": "shuō", "pinyin_parts": ["shuō"], "pinyin_tones": [1],
         "pos": "verb", "english": "to speak; to say", "radicals": ["讠", "兑"],
         "components": [{"char": "说", "role": "semantic", "meaning": "to speak", "breakdown": "讠 (speech) + 兑 (phonetic)"}],
         "stroke_count": 9,
         "example": {"zh": "他说中文。",   "pinyin": "Tā shuō zhōngwén.",
                     "pinyin_parts": ["Tā", "shuō", "zhōng", "wén"],
                     "pinyin_tones": [1, 1, 1, 2],
                     "en": "He speaks Chinese."}},
        {"word": "看", "pinyin_text": "kàn", "pinyin_parts": ["kàn"], "pinyin_tones": [4],
         "pos": "verb", "english": "to look; to see", "radicals": ["手", "目"],
         "components": [{"char": "看", "role": "semantic", "meaning": "to look", "breakdown": "手 (hand) + 目 (eye)"}],
         "stroke_count": 9,
         "example": {"zh": "我看书。",   "pinyin": "Wǒ kàn shū.",
                     "pinyin_parts": ["Wǒ", "kàn", "shū"],
                     "pinyin_tones": [3, 4, 1],
                     "en": "I read a book."}},
        {"word": "水", "pinyin_text": "shuǐ", "pinyin_parts": ["shuǐ"], "pinyin_tones": [3],
         "pos": "noun", "english": "water", "radicals": ["水"],
         "components": [{"char": "水", "role": "semantic", "meaning": "water"}],
         "stroke_count": 4,
         "example": {"zh": "我想喝水。",   "pinyin": "Wǒ xiǎng hē shuǐ.",
                     "pinyin_parts": ["Wǒ", "xiǎng", "hē", "shuǐ"],
                     "pinyin_tones": [3, 3, 1, 3],
                     "en": "I want to drink water."}},
    ]


def _manual_hsk2_words():
    """Rich HSK 2 words."""
    return [
        {"word": "一起", "pinyin_text": "yīqǐ", "pinyin_parts": ["yī", "qǐ"], "pinyin_tones": [1, 3],
         "pos": "adverb", "english": "together", "radicals": ["一", "走"],
         "components": [{"char": "一", "role": "semantic", "meaning": "one"},
                        {"char": "起", "role": "compound", "meaning": "to rise", "breakdown": "走 (walk) + 己 (phonetic)"}],
         "stroke_count": 14,
         "example": {"zh": "我们一起去学校。",   "pinyin": "Wǒmen yīqǐ qù xuéxiào.",
                     "pinyin_parts": ["Wǒ", "men", "yī", "qǐ", "qù", "xué", "xiào"],
                     "pinyin_tones": [3, 0, 1, 3, 4, 2, 4],
                     "en": "Let's go to school together."}},
        {"word": "因为", "pinyin_text": "yīnwèi", "pinyin_parts": ["yīn", "wèi"], "pinyin_tones": [1, 4],
         "pos": "conjunction", "english": "because", "radicals": ["口", "大"],
         "components": [{"char": "因", "role": "semantic", "meaning": "cause; reason"},
                        {"char": "为", "role": "semantic", "meaning": "for; because"}],
         "stroke_count": 10,
         "example": {"zh": "因为下雨，我不去。",   "pinyin": "Yīnwèi xiàyǔ, wǒ bù qù.",
                     "pinyin_parts": ["Yīn", "wèi", "xià", "yǔ", "wǒ", "bù", "qù"],
                     "pinyin_tones": [1, 4, 4, 3, 3, 4, 4],
                     "en": "Because it's raining, I'm not going."}},
        {"word": "但是", "pinyin_text": "dànshì", "pinyin_parts": ["dàn", "shì"], "pinyin_tones": [4, 4],
         "pos": "conjunction", "english": "but; however", "radicals": ["日", "正"],
         "components": [{"char": "但", "role": "semantic", "meaning": "but; only"},
                        {"char": "是", "role": "semantic", "meaning": "to be"}],
         "stroke_count": 13,
         "example": {"zh": "我很累，但是很开心。",   "pinyin": "Wǒ hěn lèi, dànshì hěn kāixīn.",
                     "pinyin_parts": ["Wǒ", "hěn", "lèi", "dàn", "shì", "hěn", "kāi", "xīn"],
                     "pinyin_tones": [3, 3, 4, 4, 4, 3, 1, 1],
                     "en": "I'm tired, but very happy."}},
        {"word": "可以", "pinyin_text": "kěyǐ", "pinyin_parts": ["kě", "yǐ"], "pinyin_tones": [3, 3],
         "pos": "verb", "english": "can; may", "radicals": ["口", "以"],
         "components": [{"char": "可", "role": "semantic", "meaning": "able; possible"},
                        {"char": "以", "role": "semantic", "meaning": "by means of"}],
         "stroke_count": 9,
         "example": {"zh": "我可以进来吗？",   "pinyin": "Wǒ kěyǐ jìnlái ma?",
                     "pinyin_parts": ["Wǒ", "kě", "yǐ", "jìn", "lái", "ma"],
                     "pinyin_tones": [3, 3, 3, 4, 2, 0],
                     "en": "May I come in?"}},
        {"word": "快乐", "pinyin_text": "kuàilè", "pinyin_parts": ["kuài", "lè"], "pinyin_tones": [4, 4],
         "pos": "adjective", "english": "happy", "radicals": ["忄", "乐"],
         "components": [{"char": "快", "role": "compound", "meaning": "fast; quick"},
                        {"char": "乐", "role": "semantic", "meaning": "joy"}],
         "stroke_count": 12,
         "example": {"zh": "祝你生日快乐！",   "pinyin": "Zhù nǐ shēngrì kuàilè!",
                     "pinyin_parts": ["Zhù", "nǐ", "shēng", "rì", "kuài", "lè"],
                     "pinyin_tones": [4, 3, 1, 4, 4, 4],
                     "en": "Happy birthday to you!"}},
    ]


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate HSK vocabulary data')
    parser.add_argument('--hsk-levels', help='Comma-separated HSK levels (1,2,3,4,5,6,7-9)')
    parser.add_argument('--enriched-only', action='store_true', help='Only use enriched manual words (HSK 1-2)')
    args = parser.parse_args()

    print("Generating 每日字 vocabulary data...")

    if args.hsk_levels:
        hsk_levels = args.hsk_levels.split(',')
    else:
        hsk_levels = ['1', '2', '3', '4', '5', '6', '7-9']

    # Start with enriched manual words for HSK 1-2
    hsk1_manual, hsk2_manual = load_enriched_hsk1_hsk2()
    words = []

    # Add enriched HSK 1 words
    enriched_ids = set()
    for i, w in enumerate(hsk1_manual):
        w["id"] = f"hsk1_{i+1:04d}"
        w["hsk_level"] = 1
        words.append(w)
        enriched_ids.add(w["word"])

    print(f"  Added {len(hsk1_manual)} enriched HSK 1 words")

    # Add enriched HSK 2 words
    for i, w in enumerate(hsk2_manual):
        w["id"] = f"hsk2_{i+1:04d}"
        w["hsk_level"] = 2
        words.append(w)
        enriched_ids.add(w["word"])

    print(f"  Added {len(hsk2_manual)} enriched HSK 2 words")

    if not args.enriched_only:
        # Download full HSK lists from krmanik dataset
        print("\nDownloading HSK word lists from krmanik/HSK-3.0...")
        downloaded = download_hsk_data(hsk_levels)

        # Merge: use downloaded words but skip ones that already have enriched entries
        # Compute ID offsets: number of enriched words per level
        enriched_per_level = {1: len(hsk1_manual), 2: len(hsk2_manual)}
        
        hsk_counts = {}
        
        for w in downloaded:
            word_key = w["word"]
            hsk_level = w["hsk_level"]

            # Skip duplicates of enriched words
            already_have = word_key in enriched_ids
            level_key = hsk_level if hsk_level < 7 else 79
            
            if already_have:
                continue
            
            # Fix the ID to avoid overlapping with enriched words
            offset = enriched_per_level.get(level_key, 0)
            old_id = w["id"]
            # Extract the numeric part and offset it
            import re
            m = re.search(r'(\d+)$', old_id)
            if m:
                new_num = int(m.group(1)) + offset
                new_id = old_id[:m.start()] + f'{new_num:04d}'
                w['id'] = new_id
            
            words.append(w)
            hsk_counts[level_key] = hsk_counts.get(level_key, 0) + 1
        
        print(f"  Added {hsk_counts.get(1, 0)} more HSK 1 words (downloaded)")
        print(f"  Added {hsk_counts.get(2, 0)} more HSK 2 words (downloaded)")
        total_3plus = sum(v for k, v in hsk_counts.items() if k >= 3)
        print(f"  Added {total_3plus} HSK 3+ words (downloaded)")
    else:
        print("  (enriched-only mode, skipping download)")

    # Update word counts in level definitions
    level_counts = {}
    for w in words:
        lv = f"hsk{w['hsk_level']}" if w['hsk_level'] < 7 else 'hsk79'
        level_counts[lv] = level_counts.get(lv, 0) + 1

    for l in LEVELS:
        if l["id"] in level_counts:
            l["word_count"] = level_counts[l["id"]]

    total_words = len(words)
    print(f"\nTotal: {total_words} words")

    # Build the master file
    data = {
        "meta": {
            "title": "每日字",
            "title_en": "Mei Ri Zi",
            "version": "1.0",
            "hsk_revision": "3.0 (2021)",
            "total_words": total_words,
            "levels": LEVELS,
            "stems": HEAVENLY_STEMS,
            "stem_elements": STEM_ELEMENTS,
            "generated_at": "2026-07-27T00:00:00Z"
        },
        "words": words
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Wrote {total_words} words to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
