#!/usr/bin/env python3
"""
enrich_glyphs.py — Add component/radical breakdowns to all vocabulary words.

Uses DeepSeek API to generate radical information for all unique characters
in the HSK vocabulary, then applies them to each word.

Usage:
  export DEEPSEEK_API_KEY='your-key-here'
  python scripts/enrich_glyphs.py
"""

import json
import os
import subprocess
import sys
import re
import time
import tempfile
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "hsk_daily.json"
CACHE_DIR = DATA_DIR / "_cache"
RADICAL_CACHE = CACHE_DIR / "char_radicals.json"

BATCH_SIZE = 40  # characters per API call
RATE_LIMIT = 1.0  # seconds between API calls


def load_data():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def get_unique_chars(data):
    """Get all unique characters from the vocabulary."""
    chars = set()
    for w in data["words"]:
        for ch in w["word"]:
            chars.add(ch)
    return sorted(chars)


def get_cached_radicals():
    """Load cached radical data."""
    if RADICAL_CACHE.exists():
        return json.loads(RADICAL_CACHE.read_text(encoding="utf-8"))
    return {}


def save_cached_radicals(data):
    RADICAL_CACHE.parent.mkdir(parents=True, exist_ok=True)
    RADICAL_CACHE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def call_deepseek(prompt):
    """Call the DeepSeek API with a prompt."""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("ERROR: DEEPSEEK_API_KEY not set")
        sys.exit(1)
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a Chinese character expert. Return ONLY valid JSON, no other text."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(json.dumps(payload))
        req_file = f.name
    
    try:
        result = subprocess.run([
            "curl", "-s",
            "https://api.deepseek.com/chat/completions",
            "-H", "Content-Type: application/json",
            "-H", f"Authorization: Bearer {api_key}",
            "-d", f"@{req_file}"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            return None
        
        response = json.loads(result.stdout)
        if "choices" not in response or len(response["choices"]) == 0:
            return None
        
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  Error: {e}")
        return None
    finally:
        os.unlink(req_file)


def build_radical_prompt(chars_batch):
    """Build a prompt for getting radical info about a batch of characters."""
    chars_list = list(chars_batch)
    prompt = f"""For each of these Chinese characters, provide the Kangxi radical information.
Return a JSON array where each entry has:
- "char": the character
- "radical": the Kangxi radical character
- "radical_name": Chinese name of the radical
- "radical_meaning": English meaning of the radical
- "meaning": brief meaning of the character itself

Only return valid JSON, no other text.
Format: [{{"char": "好", "radical": "女", "radical_name": "女字旁", "radical_meaning": "woman", "meaning": "good"}}, ...]

Characters: {json.dumps(chars_list, ensure_ascii=False)}
"""
    return prompt


def parse_radical_response(content):
    """Parse the DeepSeek response to get radical data."""
    if not content:
        return None
    
    text = content.strip()
    # Strip markdown code fences
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON array
    match = re.search(r'\[.*?\]', text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            if isinstance(data, list):
                return data
        except:
            pass
    return None


def enrich_word_components(word, radical_map):
    """Add component breakdown to a word using radical data."""
    components = []
    seen_chars = set()
    
    for ch in word["word"]:
        if ch in seen_chars:
            continue
        seen_chars.add(ch)
        
        if ch in radical_map:
            r = radical_map[ch]
            components.append({
                "char": ch,
                "role": "semantic",
                "meaning": r.get("meaning", r.get("radical_meaning", ""))
            })
    
    return components


def main():
    print("Loading vocabulary...")
    data = load_data()
    
    # Get all unique characters
    all_chars = get_unique_chars(data)
    print(f"Unique characters in vocabulary: {len(all_chars)}")
    
    # Load cached radicals
    radical_map = get_cached_radicals()
    print(f"Cached radicals: {len(radical_map)}")
    
    # Find characters that need processing
    chars_to_fetch = [c for c in all_chars if c not in radical_map]
    print(f"Characters to fetch: {len(chars_to_fetch)}")
    
    if not chars_to_fetch:
        print("All characters already cached!")
    else:
        # Process in batches
        for i in range(0, len(chars_to_fetch), BATCH_SIZE):
            batch = chars_to_fetch[i:i + BATCH_SIZE]
            batch_num = i // BATCH_SIZE + 1
            total_batches = (len(chars_to_fetch) + BATCH_SIZE - 1) // BATCH_SIZE
            
            print(f"  Batch {batch_num}/{total_batches} ({len(batch)} chars)...")
            
            prompt = build_radical_prompt(batch)
            response = call_deepseek(prompt)
            
            if response:
                results = parse_radical_response(response)
                if results:
                    for r in results:
                        ch = r.get("char", "")
                        if ch:
                            radical_map[ch] = {
                                "radical": r.get("radical", ""),
                                "radical_name": r.get("radical_name", ""),
                                "radical_meaning": r.get("radical_meaning", ""),
                                "meaning": r.get("meaning", "")
                            }
                    print(f"    Got {len(results)} radicals")
                else:
                    print(f"    Failed to parse response")
            else:
                print(f"    API call failed")
            
            # Save cache periodically
            if (i // BATCH_SIZE + 1) % 5 == 0:
                save_cached_radicals(radical_map)
                print(f"    Cache saved ({len(radical_map)} radicals)")
            
            if i + BATCH_SIZE < len(chars_to_fetch):
                time.sleep(RATE_LIMIT)
        
        save_cached_radicals(radical_map)
        print(f"Done fetching. Total radicals cached: {len(radical_map)}")
    
    # Now apply radicals to all words
    print("\nApplying radical data to words...")
    
    enriched = 0
    for w in data["words"]:
        # Skip words that already have rich component data
        if w.get("components") and len(w["components"]) > 0:
            # Check if they're rich (hand-crafted)
            if any(c.get("breakdown") for c in w["components"]):
                continue
        
        comps = enrich_word_components(w, radical_map)
        if comps:
            w["components"] = comps
            enriched += 1
    
    save_data(data)
    
    # Stats
    with_comps = sum(1 for w in data["words"] if w.get("components") and len(w["components"]) > 0)
    print(f"Enriched {enriched} words with radical data")
    print(f"Total words with components: {with_comps}/{len(data['words'])}")
    
    # Show per-level stats
    for lname, lnum in [('HSK 1',1),('HSK 2',2),('HSK 3',3),('HSK 4',4),('HSK 5',5),('HSK 6',6),('HSK 7-9',7)]:
        words = [w for w in data["words"] if w["hsk_level"] == lnum]
        with_c = [w for w in words if w.get("components") and len(w["components"]) > 0]
        if words:
            print(f"  {lname}: {len(with_c)}/{len(words)} words have components")


if __name__ == "__main__":
    main()
