#!/usr/bin/env python3
"""
enrich_data.py — Enrich vocabulary with component breakdowns and 
better example sentences.

This script takes hsk_daily.json and adds:
1. Radical/component data from Unihan database
2. Better example sentences using diverse templates

Usage:
  python scripts/enrich_data.py                    # enrich all levels
  python scripts/enrich_data.py --level hsk1       # enrich only HSK 1
"""

import json
import os
import re
import urllib.request
from pathlib import Path
import time

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "hsk_daily.json"
CACHE_DIR = DATA_DIR / "_cache"
UNIHAN_CACHE = CACHE_DIR / "unihan_radicals.json"

# ---- Unihan Radical Data ----

UNIHAN_URL = "https://raw.githubusercontent.com/unicode-org/unicode-data/main/Unihan/Unihan_RadicalStrokeCounts.txt"

def download_unihan():
    """Download Unihan radical data."""
    if UNIHAN_CACHE.exists():
        print(f"  Using cached: {UNIHAN_CACHE}")
        return json.loads(UNIHAN_CACHE.read_text())
    
    print(f"  Downloading Unihan radical data...")
    req = urllib.request.Request(UNIHAN_URL, headers={'User-Agent': 'meirizi/1.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        text = resp.read().decode('utf-8')
        
        # Parse: U+4E2D\tkRSUnicode\t23.0
        radical_map = {}
        for line in text.split('\n'):
            if line.startswith('#') or not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) >= 3 and 'kRSUnicode' in parts[1]:
                # Extract char from U+XXXX
                hex_code = parts[0].strip()
                if hex_code.startswith('U+'):
                    try:
                        char = chr(int(hex_code[2:], 16))
                    except:
                        continue
                    radical_info = parts[2].strip()
                    radical_map[char] = radical_info
        
        UNIHAN_CACHE.parent.mkdir(parents=True, exist_ok=True)
        UNIHAN_CACHE.write_text(json.dumps(radical_map, ensure_ascii=False))
        print(f"  Cached {len(radical_map)} characters")
        return radical_map
    except Exception as e:
        print(f"  Failed: {e}")
        return {}

# ---- Common radical reference data ----

# Mapping of Kangxi radical numbers to names and meanings
KANGXI_RADICALS = {
    1: {"name": "一", "meaning": "one", "pinyin": "yī"},
    2: {"name": "丨", "meaning": "line", "pinyin": "gǔn"},
    3: {"name": "丶", "meaning": "dot", "pinyin": "zhǔ"},
    4: {"name": "丿", "meaning": "slash", "pinyin": "piě"},
    5: {"name": "乙", "meaning": "second", "pinyin": "yǐ"},
    6: {"name": "亅", "meaning": "hook", "pinyin": "jué"},
    7: {"name": "二", "meaning": "two", "pinyin": "èr"},
    8: {"name": "亠", "meaning": "lid", "pinyin": "tóu"},
    9: {"name": "人", "meaning": "person", "pinyin": "rén"},
    10: {"name": "儿", "meaning": "legs", "pinyin": "ér"},
    11: {"name": "入", "meaning": "enter", "pinyin": "rù"},
    12: {"name": "八", "meaning": "eight", "pinyin": "bā"},
    13: {"name": "冂", "meaning": "wide", "pinyin": "jiōng"},
    14: {"name": "冖", "meaning": "cover", "pinyin": "mì"},
    15: {"name": "冫", "meaning": "ice", "pinyin": "bīng"},
    16: {"name": "几", "meaning": "table", "pinyin": "jǐ"},
    17: {"name": "凵", "meaning": "open mouth", "pinyin": "kǎn"},
    18: {"name": "刀", "meaning": "knife", "pinyin": "dāo"},
    19: {"name": "力", "meaning": "power", "pinyin": "lì"},
    20: {"name": "勹", "meaning": "wrap", "pinyin": "bāo"},
    21: {"name": "匕", "meaning": "spoon", "pinyin": "bǐ"},
    22: {"name": "匚", "meaning": "box", "pinyin": "fāng"},
    23: {"name": "匸", "meaning": "hide", "pinyin": "xì"},
    24: {"name": "十", "meaning": "ten", "pinyin": "shí"},
    25: {"name": "卜", "meaning": "divine", "pinyin": "bǔ"},
    26: {"name": "卩", "meaning": "seal", "pinyin": "jié"},
    27: {"name": "厂", "meaning": "cliff", "pinyin": "hǎn"},
    28: {"name": "厶", "meaning": "private", "pinyin": "sī"},
    29: {"name": "又", "meaning": "again", "pinyin": "yòu"},
    30: {"name": "口", "meaning": "mouth", "pinyin": "kǒu"},
    31: {"name": "囗", "meaning": "enclosure", "pinyin": "wéi"},
    32: {"name": "土", "meaning": "earth", "pinyin": "tǔ"},
    33: {"name": "士", "meaning": "scholar", "pinyin": "shì"},
    34: {"name": "夂", "meaning": "go", "pinyin": "zhǐ"},
    35: {"name": "夊", "meaning": "slow", "pinyin": "suī"},
    36: {"name": "夕", "meaning": "evening", "pinyin": "xī"},
    37: {"name": "大", "meaning": "big", "pinyin": "dà"},
    38: {"name": "女", "meaning": "woman", "pinyin": "nǚ"},
    39: {"name": "子", "meaning": "child", "pinyin": "zǐ"},
    40: {"name": "宀", "meaning": "roof", "pinyin": "mián"},
    41: {"name": "寸", "meaning": "inch", "pinyin": "cùn"},
    42: {"name": "小", "meaning": "small", "pinyin": "xiǎo"},
    43: {"name": "尢", "meaning": "lame", "pinyin": "yóu"},
    44: {"name": "尸", "meaning": "corpse", "pinyin": "shī"},
    45: {"name": "屮", "meaning": "sprout", "pinyin": "chè"},
    46: {"name": "山", "meaning": "mountain", "pinyin": "shān"},
    47: {"name": "川", "meaning": "river", "pinyin": "chuān"},
    48: {"name": "工", "meaning": "work", "pinyin": "gōng"},
    49: {"name": "己", "meaning": "self", "pinyin": "jǐ"},
    50: {"name": "巾", "meaning": "turban", "pinyin": "jīn"},
    51: {"name": "干", "meaning": "dry", "pinyin": "gān"},
    52: {"name": "幺", "meaning": "tiny", "pinyin": "yāo"},
    53: {"name": "广", "meaning": "shelter", "pinyin": "yǎn"},
    54: {"name": "廴", "meaning": "long stride", "pinyin": "yǐn"},
    55: {"name": "廾", "meaning": "hands", "pinyin": "gǒng"},
    56: {"name": "弋", "meaning": "shoot", "pinyin": "yì"},
    57: {"name": "弓", "meaning": "bow", "pinyin": "gōng"},
    58: {"name": "彐", "meaning": "snout", "pinyin": "jì"},
    59: {"name": "彡", "meaning": "bristle", "pinyin": "shān"},
    60: {"name": "彳", "meaning": "step", "pinyin": "chì"},
    61: {"name": "心", "meaning": "heart", "pinyin": "xīn"},
    62: {"name": "戈", "meaning": "spear", "pinyin": "gē"},
    63: {"name": "戶", "meaning": "door", "pinyin": "hù"},
    64: {"name": "手", "meaning": "hand", "pinyin": "shǒu"},
    65: {"name": "支", "meaning": "branch", "pinyin": "zhī"},
    66: {"name": "攵", "meaning": "rap", "pinyin": "pū"},
    67: {"name": "文", "meaning": "script", "pinyin": "wén"},
    68: {"name": "斗", "meaning": "dipper", "pinyin": "dǒu"},
    69: {"name": "斤", "meaning": "axe", "pinyin": "jīn"},
    70: {"name": "方", "meaning": "square", "pinyin": "fāng"},
    71: {"name": "无", "meaning": "not", "pinyin": "wú"},
    72: {"name": "日", "meaning": "sun", "pinyin": "rì"},
    73: {"name": "曰", "meaning": "say", "pinyin": "yuē"},
    74: {"name": "月", "meaning": "moon", "pinyin": "yuè"},
    75: {"name": "木", "meaning": "tree", "pinyin": "mù"},
    76: {"name": "欠", "meaning": "lack", "pinyin": "qiàn"},
    77: {"name": "止", "meaning": "stop", "pinyin": "zhǐ"},
    78: {"name": "歹", "meaning": "death", "pinyin": "dǎi"},
    79: {"name": "殳", "meaning": "weapon", "pinyin": "shū"},
    80: {"name": "毋", "meaning": "not", "pinyin": "wú"},
    81: {"name": "比", "meaning": "compare", "pinyin": "bǐ"},
    82: {"name": "毛", "meaning": "fur", "pinyin": "máo"},
    83: {"name": "氏", "meaning": "clan", "pinyin": "shì"},
    84: {"name": "气", "meaning": "steam", "pinyin": "qì"},
    85: {"name": "水", "meaning": "water", "pinyin": "shuǐ"},
    86: {"name": "火", "meaning": "fire", "pinyin": "huǒ"},
    87: {"name": "爪", "meaning": "claw", "pinyin": "zhǎo"},
    88: {"name": "父", "meaning": "father", "pinyin": "fù"},
    89: {"name": "爻", "meaning": "lines", "pinyin": "yáo"},
    90: {"name": "爿", "meaning": "split wood", "pinyin": "pán"},
    91: {"name": "片", "meaning": "slice", "pinyin": "piàn"},
    92: {"name": "牙", "meaning": "fang", "pinyin": "yá"},
    93: {"name": "牛", "meaning": "cow", "pinyin": "niú"},
    94: {"name": "犬", "meaning": "dog", "pinyin": "quǎn"},
    95: {"name": "玄", "meaning": "dark", "pinyin": "xuán"},
    96: {"name": "玉", "meaning": "jade", "pinyin": "yù"},
    97: {"name": "瓜", "meaning": "melon", "pinyin": "guā"},
    98: {"name": "瓦", "meaning": "tile", "pinyin": "wǎ"},
    99: {"name": "甘", "meaning": "sweet", "pinyin": "gān"},
    100: {"name": "生", "meaning": "life", "pinyin": "shēng"},
    101: {"name": "用", "meaning": "use", "pinyin": "yòng"},
    102: {"name": "田", "meaning": "field", "pinyin": "tián"},
    103: {"name": "疋", "meaning": "bolt of cloth", "pinyin": "pǐ"},
    104: {"name": "疒", "meaning": "sickness", "pinyin": "chuáng"},
    105: {"name": "癶", "meaning": "footsteps", "pinyin": "bō"},
    106: {"name": "白", "meaning": "white", "pinyin": "bái"},
    107: {"name": "皮", "meaning": "skin", "pinyin": "pí"},
    108: {"name": "皿", "meaning": "dish", "pinyin": "mǐn"},
    109: {"name": "目", "meaning": "eye", "pinyin": "mù"},
    110: {"name": "矛", "meaning": "spear", "pinyin": "máo"},
    111: {"name": "矢", "meaning": "arrow", "pinyin": "shǐ"},
    112: {"name": "石", "meaning": "stone", "pinyin": "shí"},
    113: {"name": "示", "meaning": "spirit", "pinyin": "shì"},
    114: {"name": "禸", "meaning": "track", "pinyin": "róu"},
    115: {"name": "禾", "meaning": "grain", "pinyin": "hé"},
    116: {"name": "穴", "meaning": "cave", "pinyin": "xué"},
    117: {"name": "立", "meaning": "stand", "pinyin": "lì"},
    118: {"name": "竹", "meaning": "bamboo", "pinyin": "zhú"},
    119: {"name": "米", "meaning": "rice", "pinyin": "mǐ"},
    120: {"name": "糸", "meaning": "silk", "pinyin": "mì"},
    121: {"name": "缶", "meaning": "jar", "pinyin": "fǒu"},
    122: {"name": "网", "meaning": "net", "pinyin": "wǎng"},
    123: {"name": "羊", "meaning": "sheep", "pinyin": "yáng"},
    124: {"name": "羽", "meaning": "feather", "pinyin": "yǔ"},
    125: {"name": "老", "meaning": "old", "pinyin": "lǎo"},
    126: {"name": "而", "meaning": "and", "pinyin": "ér"},
    127: {"name": "耒", "meaning": "plow", "pinyin": "lěi"},
    128: {"name": "耳", "meaning": "ear", "pinyin": "ěr"},
    129: {"name": "聿", "meaning": "brush", "pinyin": "yù"},
    130: {"name": "肉", "meaning": "meat", "pinyin": "ròu"},
    131: {"name": "臣", "meaning": "minister", "pinyin": "chén"},
    132: {"name": "自", "meaning": "self", "pinyin": "zì"},
    133: {"name": "至", "meaning": "arrive", "pinyin": "zhì"},
    134: {"name": "臼", "meaning": "mortar", "pinyin": "jiù"},
    135: {"name": "舌", "meaning": "tongue", "pinyin": "shé"},
    136: {"name": "舛", "meaning": "oppose", "pinyin": "chuǎn"},
    137: {"name": "舟", "meaning": "boat", "pinyin": "zhōu"},
    138: {"name": "艮", "meaning": "still", "pinyin": "gèn"},
    139: {"name": "色", "meaning": "color", "pinyin": "sè"},
    140: {"name": "艸", "meaning": "grass", "pinyin": "cǎo"},
    141: {"name": "虍", "meaning": "tiger", "pinyin": "hǔ"},
    142: {"name": "虫", "meaning": "insect", "pinyin": "chóng"},
    143: {"name": "血", "meaning": "blood", "pinyin": "xuè"},
    144: {"name": "行", "meaning": "go", "pinyin": "xíng"},
    145: {"name": "衣", "meaning": "clothes", "pinyin": "yī"},
    146: {"name": "西", "meaning": "cover", "pinyin": "xī"},
    147: {"name": "見", "meaning": "see", "pinyin": "jiàn"},
    148: {"name": "角", "meaning": "horn", "pinyin": "jiǎo"},
    149: {"name": "言", "meaning": "speech", "pinyin": "yán"},
    150: {"name": "谷", "meaning": "valley", "pinyin": "gǔ"},
    151: {"name": "豆", "meaning": "bean", "pinyin": "dòu"},
    152: {"name": "豕", "meaning": "pig", "pinyin": "shǐ"},
    153: {"name": "豸", "meaning": "badger", "pinyin": "zhì"},
    154: {"name": "貝", "meaning": "shell", "pinyin": "bèi"},
    155: {"name": "赤", "meaning": "red", "pinyin": "chì"},
    156: {"name": "走", "meaning": "walk", "pinyin": "zǒu"},
    157: {"name": "足", "meaning": "foot", "pinyin": "zú"},
    158: {"name": "身", "meaning": "body", "pinyin": "shēn"},
    159: {"name": "車", "meaning": "cart", "pinyin": "chē"},
    160: {"name": "辛", "meaning": "bitter", "pinyin": "xīn"},
    161: {"name": "辰", "meaning": "morning", "pinyin": "chén"},
    162: {"name": "辵", "meaning": "walk", "pinyin": "chuò"},
    163: {"name": "邑", "meaning": "city", "pinyin": "yì"},
    164: {"name": "酉", "meaning": "wine", "pinyin": "yǒu"},
    165: {"name": "釆", "meaning": "distinguish", "pinyin": "biàn"},
    166: {"name": "里", "meaning": "village", "pinyin": "lǐ"},
}

# Common character components for HSK 1 characters
# These are manually curated for the most common HSK 1 characters
# Format: char -> [(character, role, meaning, breakdown)]
HSK1_COMPONENTS = {
    "爱": [{"char": "爫", "role": "semantic", "meaning": "claw"}, 
           {"char": "心", "role": "semantic", "meaning": "heart"}],
    "八": [{"char": "八", "role": "pictographic", "meaning": "eight"}],
    "爸爸": [{"char": "父", "role": "semantic", "meaning": "father"},
             {"char": "巴", "role": "phonetic", "meaning": "ba (sound)"}],
    "杯子": [{"char": "木", "role": "semantic", "meaning": "wood"},
              {"char": "不", "role": "phonetic", "meaning": "bu (sound)"}],
    "北京": [{"char": "北", "role": "semantic", "meaning": "north"},
              {"char": "京", "role": "semantic", "meaning": "capital"}],
    "本": [{"char": "木", "role": "semantic", "meaning": "tree"},
           {"char": "一", "role": "indicator", "meaning": "root marked on tree"}],
    "不": [{"char": "一", "role": "semantic", "meaning": "one"}],
    "菜": [{"char": "艹", "role": "semantic", "meaning": "grass"},
           {"char": "采", "role": "phonetic", "meaning": "cai (sound)"}],
    "茶": [{"char": "艹", "role": "semantic", "meaning": "grass"},
           {"char": "余", "role": "phonetic", "meaning": "yu (sound)"}],
    "吃": [{"char": "口", "role": "semantic", "meaning": "mouth"},
           {"char": "乞", "role": "phonetic", "meaning": "qi (sound)"}],
    "出租车": [{"char": "出", "role": "semantic", "meaning": "go out"},
                {"char": "租", "role": "semantic", "meaning": "rent"},
                {"char": "车", "role": "semantic", "meaning": "vehicle"}],
    "大": [{"char": "大", "role": "pictographic", "meaning": "standing person (big)"}],
    "大学": [{"char": "大", "role": "semantic", "meaning": "big"},
              {"char": "学", "role": "semantic", "meaning": "study"}],
    "的": [{"char": "白", "role": "phonetic", "meaning": "bai (sound)"},
           {"char": "勺", "role": "semantic", "meaning": "spoon"}],
    "点": [{"char": "占", "role": "phonetic", "meaning": "zhan (sound)"},
           {"char": "火", "role": "semantic", "meaning": "fire"}],
    "电脑": [{"char": "电", "role": "semantic", "meaning": "electric"},
              {"char": "脑", "role": "semantic", "meaning": "brain"}],
    "电视": [{"char": "电", "role": "semantic", "meaning": "electric"},
              {"char": "视", "role": "semantic", "meaning": "view"}],
    "电影": [{"char": "电", "role": "semantic", "meaning": "electric"},
              {"char": "影", "role": "semantic", "meaning": "shadow"}],
    "东西": [{"char": "东", "role": "semantic", "meaning": "east"},
              {"char": "西", "role": "semantic", "meaning": "west"}],
    "都": [{"char": "者", "role": "phonetic", "meaning": "zhe (sound)"},
           {"char": "阝", "role": "semantic", "meaning": "city"}],
    "读": [{"char": "讠", "role": "semantic", "meaning": "speech"},
           {"char": "卖", "role": "phonetic", "meaning": "mai (sound)"}],
    "对": [{"char": "又", "role": "semantic", "meaning": "hand"},
           {"char": "寸", "role": "semantic", "meaning": "inch"}],
    "多": [{"char": "夕", "role": "semantic", "meaning": "evening (repeated)"}],
    "儿": [{"char": "儿", "role": "pictographic", "meaning": "child"}],
    "二": [{"char": "二", "role": "indicator", "meaning": "two"}],
    "饭店": [{"char": "饭", "role": "compound", "meaning": "rice"},
              {"char": "店", "role": "compound", "meaning": "shop"}],
    "飞": [{"char": "飞", "role": "pictographic", "meaning": "fly"}],
    "飞机": [{"char": "飞", "role": "semantic", "meaning": "fly"},
              {"char": "机", "role": "semantic", "meaning": "machine"}],
    "非常": [{"char": "非", "role": "semantic", "meaning": "not"},
              {"char": "常", "role": "semantic", "meaning": "often"}],
    "苹果": [{"char": "苹", "role": "phonetic", "meaning": "ping (sound)"},
              {"char": "果", "role": "semantic", "meaning": "fruit"}],
    "分钟": [{"char": "分", "role": "semantic", "meaning": "divide"},
              {"char": "钟", "role": "semantic", "meaning": "clock"}],
    "高兴": [{"char": "高", "role": "semantic", "meaning": "high"},
              {"char": "兴", "role": "semantic", "meaning": "prosper"}],
    "个": [{"char": "丨", "role": "pictographic", "meaning": "bamboo stalk"}],
    "工作": [{"char": "工", "role": "semantic", "meaning": "work"},
              {"char": "作", "role": "semantic", "meaning": "do"}],
    "狗": [{"char": "犭", "role": "semantic", "meaning": "dog"},
           {"char": "句", "role": "phonetic", "meaning": "ju (sound)"}],
    "关": [{"char": "丷", "role": "semantic", "meaning": "8"}],
    "关系": [{"char": "关", "role": "semantic", "meaning": "close"},
              {"char": "系", "role": "semantic", "meaning": "system"}],
    "馆": [{"char": "饣", "role": "semantic", "meaning": "food"},
           {"char": "官", "role": "phonetic", "meaning": "guan (sound)"}],
    "国": [{"char": "囗", "role": "semantic", "meaning": "enclosure"},
           {"char": "玉", "role": "phonetic", "meaning": "jade"}],
    "过": [{"char": "辶", "role": "semantic", "meaning": "walk"},
           {"char": "寸", "role": "phonetic", "meaning": "cun (sound)"}],
    "孩子": [{"char": "孩", "role": "compound", "meaning": "child"},
              {"char": "子", "role": "semantic", "meaning": "child"}],
    "汉": [{"char": "氵", "role": "semantic", "meaning": "water"},
           {"char": "又", "role": "phonetic", "meaning": "you (sound)"}],
    "好": [{"char": "女", "role": "semantic", "meaning": "woman"},
           {"char": "子", "role": "semantic", "meaning": "child"}],
    "号": [{"char": "口", "role": "semantic", "meaning": "mouth"},
           {"char": "丂", "role": "phonetic", "meaning": "kao (sound)"}],
    "喝": [{"char": "口", "role": "semantic", "meaning": "mouth"},
           {"char": "曷", "role": "phonetic", "meaning": "he (sound)"}],
    "和": [{"char": "禾", "role": "phonetic", "meaning": "he (sound)"},
           {"char": "口", "role": "semantic", "meaning": "mouth"}],
    "很": [{"char": "彳", "role": "semantic", "meaning": "step"},
           {"char": "艮", "role": "phonetic", "meaning": "gen (sound)"}],
    "后": [{"char": "厂", "role": "semantic", "meaning": "cliff"}],
    "花": [{"char": "艹", "role": "semantic", "meaning": "grass"},
           {"char": "化", "role": "phonetic", "meaning": "hua (sound)"}],
    "话": [{"char": "讠", "role": "semantic", "meaning": "speech"},
           {"char": "舌", "role": "phonetic", "meaning": "she (sound)"}],
    "会": [{"char": "人", "role": "semantic", "meaning": "person"},
           {"char": "云", "role": "phonetic", "meaning": "yun (sound)"}],
    "家": [{"char": "宀", "role": "semantic", "meaning": "roof"},
           {"char": "豕", "role": "semantic", "meaning": "pig"}],
    "间": [{"char": "门", "role": "semantic", "meaning": "door"},
           {"char": "日", "role": "phonetic", "meaning": "sun"}],
    "见": [{"char": "见", "role": "pictographic", "meaning": "see"}],
    "件": [{"char": "亻", "role": "semantic", "meaning": "person"},
           {"char": "牛", "role": "phonetic", "meaning": "niu (sound)"}],
    "今": [{"char": "今", "role": "pictographic", "meaning": "now"}],
    "今天": [{"char": "今", "role": "semantic", "meaning": "now"},
              {"char": "天", "role": "semantic", "meaning": "day"}],
    "九": [{"char": "九", "role": "pictographic", "meaning": "nine"}],
    "开": [{"char": "开", "role": "pictographic", "meaning": "open"}],
    "看": [{"char": "手", "role": "semantic", "meaning": "hand"},
           {"char": "目", "role": "semantic", "meaning": "eye"}],
    "考试": [{"char": "考", "role": "semantic", "meaning": "test"},
              {"char": "试", "role": "semantic", "meaning": "try"}],
    "课": [{"char": "讠", "role": "semantic", "meaning": "speech"},
           {"char": "果", "role": "phonetic", "meaning": "guo (sound)"}],
    "空": [{"char": "穴", "role": "semantic", "meaning": "cave"},
           {"char": "工", "role": "phonetic", "meaning": "gong (sound)"}],
    "口": [{"char": "口", "role": "pictographic", "meaning": "mouth"}],
    "来": [{"char": "来", "role": "pictographic", "meaning": "come"}],
    "老": [{"char": "老", "role": "pictographic", "meaning": "old"}],
    "老师": [{"char": "老", "role": "semantic", "meaning": "old"},
              {"char": "师", "role": "semantic", "meaning": "teacher"}],
    "了": [{"char": "了", "role": "pictographic", "meaning": "completed action"}],
    "冷": [{"char": "冫", "role": "semantic", "meaning": "ice"},
           {"char": "令", "role": "phonetic", "meaning": "ling (sound)"}],
    "里": [{"char": "田", "role": "semantic", "meaning": "field"},
           {"char": "土", "role": "semantic", "meaning": "earth"}],
    "六": [{"char": "六", "role": "pictographic", "meaning": "six"}],
    "吗": [{"char": "口", "role": "semantic", "meaning": "mouth"},
           {"char": "马", "role": "phonetic", "meaning": "ma (sound)"}],
    "买": [{"char": "买", "role": "pictographic", "meaning": "buy"}],
    "猫": [{"char": "犭", "role": "semantic", "meaning": "animal"},
           {"char": "苗", "role": "phonetic", "meaning": "miao (sound)"}],
    "没": [{"char": "氵", "role": "semantic", "meaning": "water"},
           {"char": "殳", "role": "phonetic", "meaning": "shu (sound)"}],
    "没关系": [{"char": "没", "role": "semantic", "meaning": "not have"},
               {"char": "关", "role": "semantic", "meaning": "relation"},
               {"char": "系", "role": "semantic", "meaning": "system"}],
    "每": [{"char": "人", "role": "semantic", "meaning": "person"},
           {"char": "母", "role": "phonetic", "meaning": "mu (sound)"}],
    "美国": [{"char": "美", "role": "phonetic", "meaning": "beautiful"},
              {"char": "国", "role": "semantic", "meaning": "country"}],
    "妹妹": [{"char": "女", "role": "semantic", "meaning": "woman"},
              {"char": "未", "role": "phonetic", "meaning": "wei (sound)"}],
    "门": [{"char": "门", "role": "pictographic", "meaning": "door"}],
    "们": [{"char": "亻", "role": "semantic", "meaning": "person"},
           {"char": "门", "role": "phonetic", "meaning": "men (sound)"}],
    "米饭": [{"char": "米", "role": "semantic", "meaning": "rice"},
              {"char": "饭", "role": "semantic", "meaning": "cooked rice"}],
    "名字": [{"char": "名", "role": "semantic", "meaning": "name"},
              {"char": "字", "role": "semantic", "meaning": "character"}],
    "明天": [{"char": "明", "role": "semantic", "meaning": "bright"},
              {"char": "天", "role": "semantic", "meaning": "day"}],
    "哪": [{"char": "口", "role": "semantic", "meaning": "mouth"},
           {"char": "那", "role": "phonetic", "meaning": "na (sound)"}],
    "那": [{"char": "那", "role": "pictographic", "meaning": "that"}],
    "男": [{"char": "田", "role": "semantic", "meaning": "field"},
           {"char": "力", "role": "semantic", "meaning": "strength"}],
    "你": [{"char": "亻", "role": "semantic", "meaning": "person"},
           {"char": "尔", "role": "phonetic", "meaning": "er (sound)"}],
    "年": [{"char": "年", "role": "pictographic", "meaning": "year"}],
    "牛": [{"char": "牛", "role": "pictographic", "meaning": "cow"}],
    "女": [{"char": "女", "role": "pictographic", "meaning": "woman"}],
    "朋友": [{"char": "朋", "role": "semantic", "meaning": "friend"},
              {"char": "友", "role": "semantic", "meaning": "friend"}],
    "票": [{"char": "西", "role": "phonetic", "meaning": "west"},
           {"char": "示", "role": "semantic", "meaning": "show"}],
    "七": [{"char": "七", "role": "pictographic", "meaning": "seven"}],
    "钱": [{"char": "钅", "role": "semantic", "meaning": "metal/gold"},
           {"char": "戋", "role": "phonetic", "meaning": "jian (sound)"}],
    "请": [{"char": "讠", "role": "semantic", "meaning": "speech"},
           {"char": "青", "role": "phonetic", "meaning": "qing (sound)"}],
    "去": [{"char": "去", "role": "pictographic", "meaning": "go"}],
    "热": [{"char": "火", "role": "semantic", "meaning": "fire"},
           {"char": "执", "role": "phonetic", "meaning": "zhi (sound)"}],
    "人": [{"char": "人", "role": "pictographic", "meaning": "person"}],
    "认识": [{"char": "认", "role": "compound", "meaning": "know"},
              {"char": "识", "role": "compound", "meaning": "know"}],
    "日": [{"char": "日", "role": "pictographic", "meaning": "sun"}],
    "三": [{"char": "三", "role": "indicator", "meaning": "three"}],
    "商店": [{"char": "商", "role": "semantic", "meaning": "commerce"},
              {"char": "店", "role": "semantic", "meaning": "shop"}],
    "上": [{"char": "一", "role": "indicator", "meaning": "above"},
           {"char": "卜", "role": "indicator"}],
    "上午": [{"char": "上", "role": "semantic", "meaning": "above"},
              {"char": "午", "role": "semantic", "meaning": "noon"}],
    "少": [{"char": "小", "role": "semantic", "meaning": "small"}],
    "谁": [{"char": "讠", "role": "semantic", "meaning": "speech"},
           {"char": "隹", "role": "phonetic", "meaning": "zhui (sound)"}],
    "什么": [{"char": "什", "role": "compound", "meaning": "what"},
              {"char": "么", "role": "compound", "meaning": "what"}],
    "十": [{"char": "十", "role": "indicator", "meaning": "ten"}],
    "时候": [{"char": "时", "role": "semantic", "meaning": "time"},
              {"char": "候", "role": "semantic", "meaning": "wait"}],
    "时间": [{"char": "时", "role": "semantic", "meaning": "time"},
              {"char": "间", "role": "semantic", "meaning": "interval"}],
    "是": [{"char": "日", "role": "semantic", "meaning": "sun"},
           {"char": "正", "role": "phonetic", "meaning": "zheng (sound)"}],
    "书": [{"char": "书", "role": "pictographic", "meaning": "book"}],
    "水": [{"char": "水", "role": "pictographic", "meaning": "water"}],
    "睡觉": [{"char": "睡", "role": "compound", "meaning": "sleep"},
              {"char": "觉", "role": "compound", "meaning": "wake"}],
    "说": [{"char": "讠", "role": "semantic", "meaning": "speech"},
           {"char": "兑", "role": "phonetic", "meaning": "dui (sound)"}],
    "四": [{"char": "囗", "role": "semantic", "meaning": "enclosure"},
           {"char": "儿", "role": "phonetic"}],
    "岁": [{"char": "山", "role": "phonetic", "meaning": "shan (sound)"},
           {"char": "夕", "role": "semantic", "meaning": "evening"}],
    "他": [{"char": "亻", "role": "semantic", "meaning": "person"},
           {"char": "也", "role": "phonetic", "meaning": "ye (sound)"}],
    "她": [{"char": "女", "role": "semantic", "meaning": "woman"},
           {"char": "也", "role": "phonetic", "meaning": "ye (sound)"}],
    "太": [{"char": "大", "role": "semantic", "meaning": "big"},
           {"char": "丶", "role": "indicator"}],
    "天气": [{"char": "天", "role": "semantic", "meaning": "sky"},
              {"char": "气", "role": "semantic", "meaning": "air"}],
    "听": [{"char": "口", "role": "semantic", "meaning": "mouth"},
           {"char": "斤", "role": "phonetic", "meaning": "jin (sound)"}],
    "同学": [{"char": "同", "role": "semantic", "meaning": "same"},
              {"char": "学", "role": "semantic", "meaning": "study"}],
    "五": [{"char": "五", "role": "indicator", "meaning": "five"}],
    "喜欢": [{"char": "喜", "role": "semantic", "meaning": "joy"},
              {"char": "欢", "role": "semantic", "meaning": "happy"}],
    "下": [{"char": "一", "role": "indicator", "meaning": "below"},
           {"char": "卜", "role": "indicator"}],
    "下午": [{"char": "下", "role": "semantic", "meaning": "below"},
              {"char": "午", "role": "semantic", "meaning": "noon"}],
    "先": [{"char": "先", "role": "pictographic", "meaning": "first"}],
    "现在": [{"char": "现", "role": "compound", "meaning": "current"},
              {"char": "在", "role": "compound", "meaning": "at"}],
    "想": [{"char": "相", "role": "phonetic", "meaning": "xiang (sound)"},
           {"char": "心", "role": "semantic", "meaning": "heart"}],
    "小": [{"char": "小", "role": "pictographic", "meaning": "small"}],
    "小姐": [{"char": "小", "role": "semantic", "meaning": "young"},
              {"char": "姐", "role": "semantic", "meaning": "sister"}],
    "些": [{"char": "此", "role": "phonetic", "meaning": "ci (sound)"},
           {"char": "二", "role": "indicator"}],
    "写": [{"char": "冖", "role": "semantic", "meaning": "cover"},
           {"char": "与", "role": "phonetic", "meaning": "yu (sound)"}],
    "谢谢": [{"char": "讠", "role": "semantic", "meaning": "speech"},
              {"char": "射", "role": "phonetic", "meaning": "she (sound)"}],
    "星期": [{"char": "星", "role": "semantic", "meaning": "star"},
              {"char": "期", "role": "semantic", "meaning": "period"}],
    "姓": [{"char": "女", "role": "semantic", "meaning": "woman"},
           {"char": "生", "role": "phonetic", "meaning": "sheng (sound)"}],
    "休息": [{"char": "休", "role": "compound", "meaning": "rest"},
              {"char": "息", "role": "compound", "meaning": "rest"}],
    "学": [{"char": "学", "role": "pictographic", "meaning": "study"}],
    "学生": [{"char": "学", "role": "semantic", "meaning": "study"},
              {"char": "生", "role": "semantic", "meaning": "life"}],
    "学习": [{"char": "学", "role": "semantic", "meaning": "study"},
              {"char": "习", "role": "semantic", "meaning": "practice"}],
    "学校": [{"char": "学", "role": "semantic", "meaning": "study"},
              {"char": "校", "role": "semantic", "meaning": "school"}],
    "一": [{"char": "一", "role": "indicator", "meaning": "one"}],
    "衣服": [{"char": "衣", "role": "semantic", "meaning": "clothing"},
              {"char": "服", "role": "semantic", "meaning": "wear"}],
    "医院": [{"char": "医", "role": "semantic", "meaning": "medical"},
              {"char": "院", "role": "semantic", "meaning": "institution"}],
    "椅子": [{"char": "椅", "role": "compound", "meaning": "chair"},
              {"char": "子", "role": "suffix"}],
    "因为": [{"char": "因", "role": "semantic", "meaning": "cause"},
              {"char": "为", "role": "semantic", "meaning": "for"}],
    "音乐": [{"char": "音", "role": "semantic", "meaning": "sound"},
              {"char": "乐", "role": "semantic", "meaning": "music"}],
    "英文": [{"char": "英", "role": "phonetic", "meaning": "ying (sound)"},
              {"char": "文", "role": "semantic", "meaning": "language"}],
    "有": [{"char": "月", "role": "phonetic", "meaning": "yue (sound)"},
           {"char": "又", "role": "semantic", "meaning": "hand/have"}],
    "雨": [{"char": "雨", "role": "pictographic", "meaning": "rain"}],
    "在": [{"char": "土", "role": "semantic", "meaning": "earth"},
           {"char": "才", "role": "phonetic", "meaning": "cai (sound)"}],
    "早上": [{"char": "早", "role": "semantic", "meaning": "early"},
              {"char": "上", "role": "semantic", "meaning": "above"}],
    "怎": [{"char": "心", "role": "semantic", "meaning": "heart"}],
    "怎么": [{"char": "怎", "role": "compound", "meaning": "how"},
              {"char": "么", "role": "compound"}],
    "这": [{"char": "文", "role": "phonetic", "meaning": "wen (sound)"},
           {"char": "辶", "role": "semantic", "meaning": "walk"}],
    "中": [{"char": "口", "role": "semantic", "meaning": "mouth"},
           {"char": "丨", "role": "indicator", "meaning": "center"}],
    "中国": [{"char": "中", "role": "semantic", "meaning": "middle"},
              {"char": "国", "role": "semantic", "meaning": "country"}],
    "中午": [{"char": "中", "role": "semantic", "meaning": "middle"},
              {"char": "午", "role": "semantic", "meaning": "noon"}],
    "住": [{"char": "亻", "role": "semantic", "meaning": "person"},
           {"char": "主", "role": "phonetic", "meaning": "zhu (sound)"}],
    "子": [{"char": "子", "role": "pictographic", "meaning": "child"}],
    "走": [{"char": "走", "role": "pictographic", "meaning": "walk"}],
    "最": [{"char": "日", "role": "semantic", "meaning": "sun"},
           {"char": "取", "role": "phonetic", "meaning": "qu (sound)"}],
    "昨天": [{"char": "昨", "role": "compound", "meaning": "yesterday"},
              {"char": "天", "role": "semantic", "meaning": "day"}],
    "做": [{"char": "亻", "role": "semantic", "meaning": "person"},
           {"char": "故", "role": "phonetic", "meaning": "gu (sound)"}],
    "坐": [{"char": "土", "role": "semantic", "meaning": "earth"},
           {"char": "人", "role": "semantic", "meaning": "person (two)"}],
}


def get_radical_info(char, unihan_data=None):
    """Get radical information for a single character."""
    # First check our curated HSK1 component data
    if char in HSK1_COMPONENTS:
        return HSK1_COMPONENTS[char]
    
    # Fall back to Unihan data
    if unihan_data and char in unihan_data:
        radical_str = unihan_data[char]
        # Format: "23.0" where 23 is the radical number
        try:
            radical_num = int(radical_str.split('.')[0])
            if radical_num in KANGXI_RADICALS:
                r = KANGXI_RADICALS[radical_num]
                return [{"char": r["name"], "role": "radical", "meaning": r["meaning"]}]
        except:
            pass
    
    return []


def build_components_for_word(word, unihan_data=None):
    """Build component array for a multi-character word."""
    components = []
    seen_chars = set()
    for ch in word["word"]:
        if ch in seen_chars:
            continue
        seen_chars.add(ch)
        comp = get_radical_info(ch, unihan_data)
        if comp:
            components.extend(comp)
    return components


# ---- Better example sentence templates ----

EXAMPLE_TEMPLATES = {
    1: [  # HSK 1 templates
        "我{word}。",
        "这是{word}。",
        "我喜欢{word}。",
        "我有{word}。",
        "我{word}很好。",
        "我不{word}。",
        "你{word}吗？",
        "{word}很大。",
        "我{word}。",
        "他{word}。",
    ],
    2: [  # HSK 2
        "请{word}。",
        "我可以{word}吗？",
        "我每天{word}。",
        "他{word}了。",
        "我们{word}吧。",
    ],
}

# For non-HSK1 words, use general templates
GENERAL_TEMPLATES = [
    "我{word}。",
    "这是{word}。",
    "他{word}。",
    "我们{word}。",
    "我喜欢{word}。",
]


def generate_example(word, level):
    """Generate a better example sentence using templates."""
    pinyin = word.get("pinyin_text", "")
    templates = EXAMPLE_TEMPLATES.get(level, GENERAL_TEMPLATES)
    # Use word's hash to pick deterministic template
    idx = hash(word["word"]) % len(templates)
    template = templates[idx]
    
    zh = template.format(word=word["word"])
    en_map = {
        "我{word}。": f"I [word].",
        "这是{word}。": f"This is [word].",
        "我喜欢{word}。": f"I like [word].",
        "我有{word}。": f"I have [word].",
        "我{word}很好。": f"My [word] is very good.",
        "我不{word}。": f"I don't [word].",
        "你{word}吗？": f"Do you [word]?",
        "{word}很大。": f"[Word] is very big.",
        "他{word}。": f"He [word].",
        "我们{word}。": f"We [word].",
        "请{word}。": f"Please [word].",
        "我可以{word}吗？": f"May I [word]?",
        "我每天{word}。": f"I [word] every day.",
        "他{word}了。": f"He [word]ed.",
        "我们{word}吧。": f"Let's [word].",
    }
    en = en_map.get(template, f"[word].").replace("[word]", word.get("english", word["word"]))

    return {
        "zh": zh,
        "pinyin": "",  # Will be filled by the main generate_data.py
        "pinyin_parts": [],
        "pinyin_tones": [],
        "en": en
    }


def enrich_level(data, level_key, unihan_data=None):
    """Enrich all words in a given level with components and better examples."""
    level_num = int(level_key.replace("hsk", "").replace("79", "7"))
    
    enriched = 0
    for w in data["words"]:
        if w["hsk_level"] != level_num:
            continue
        # Skip already-enriched words
        if w.get("components") and len(w["components"]) > 0:
            continue
        
        # Add component breakdown
        comps = build_components_for_word(w, unihan_data)
        if comps:
            w["components"] = comps
        
        # Generate better example if it's a template one
        if not w.get("example") or not w["example"].get("pinyin_parts"):
            w["example"] = generate_example(w, level_num)
        
        enriched += 1
    
    return enriched


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Enrich HSK vocabulary data")
    parser.add_argument("--level", help="Level to enrich (e.g., hsk1, hsk2)")
    args = parser.parse_args()

    print(f"Loading vocabulary data...")
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    
    # Download Unihan radical data
    unihan = download_unihan()
    
    # Determine which levels to enrich
    if args.level:
        levels = [args.level]
    else:
        levels = [l["id"] for l in data["meta"]["levels"] if l["word_count"] > 0]
    
    total_enriched = 0
    for lv in levels:
        count = enrich_level(data, lv, unihan)
        print(f"  {lv}: enriched {count} words")
        total_enriched += count
    
    # Save
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"\nDone! Enriched {total_enriched} words across {len(levels)} levels")


if __name__ == "__main__":
    main()
