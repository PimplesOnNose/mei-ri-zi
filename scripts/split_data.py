#!/usr/bin/env python3
"""
split_data.py — Split hsk_daily.json into per-level files for lazy loading.

Creates data/levels/hsk1.json through data/levels/hsk79.json.
Also creates data/index.json with level metadata for the frontend.

Usage:
  python scripts/split_data.py
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
SOURCE_FILE = DATA_DIR / "hsk_daily.json"
LEVELS_DIR = DATA_DIR / "levels"

LEVEL_MAP = {
    1: "hsk1", 2: "hsk2", 3: "hsk3", 4: "hsk4",
    5: "hsk5", 6: "hsk6", 7: "hsk79"
}


def main():
    data = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))
    LEVELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Per-level index info
    level_index = {}
    start_offset = 0
    
    for level_num in range(1, 8):
        level_key = LEVEL_MAP[level_num]
        words = [w for w in data["words"] if w["hsk_level"] == level_num]
        
        level_data = {
            "meta": {
                "title": data["meta"]["title"],
                "title_en": data["meta"]["title_en"],
                "version": data["meta"]["version"],
                "level": level_key,
                "hsk_level": level_num,
                "word_count": len(words),
                "start_offset": start_offset,
                "element": next((l["element"] for l in data["meta"]["levels"] if l["id"] == level_key), ""),
                "color": next((l["color"] for l in data["meta"]["levels"] if l["id"] == level_key), ""),
            },
            "words": words
        }
        
        out_file = LEVELS_DIR / f"{level_key}.json"
        out_file.write_text(json.dumps(level_data, ensure_ascii=False, indent=2), encoding="utf-8")
        
        level_index[level_key] = {
            "word_count": len(words),
            "start_offset": start_offset,
            "element": level_data["meta"]["element"],
            "color": level_data["meta"]["color"],
            "file": f"levels/{level_key}.json"
        }
        
        print(f"  {level_key}: {len(words)} words (offset {start_offset}) -> {out_file.name}")
        start_offset += len(words)
    
    # Write index
    index = {
        "version": 1,
        "total_words": len(data["words"]),
        "levels": level_index,
        "stems": data["meta"]["stems"],
        "stem_elements": data["meta"]["stem_elements"],
        "generated_at": data["meta"]["generated_at"]
    }
    
    (DATA_DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nIndex written to data/index.json")
    print(f"Total: {len(data['words'])} words across {len(level_index)} levels")
    
    # Show sizes
    total_size = 0
    for lk in level_index:
        sz = (LEVELS_DIR / f"{lk}.json").stat().st_size
        total_size += sz
        print(f"  {lk}.json: {sz/1024:.0f} KB")
    print(f"  Total: {total_size/1024/1024:.1f} MB (vs {SOURCE_FILE.stat().st_size/1024/1024:.1f} MB monolithic)")


if __name__ == "__main__":
    main()
