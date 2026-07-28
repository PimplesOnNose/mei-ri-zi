#!/usr/bin/env python3
"""
ai_sentences.py — Generate HSK-level-graded example sentences using DeepSeek.

Processes words in batches, sending them to the DeepSeek API to generate
natural, level-appropriate example sentences with pinyin and translations.

Usage:
  # Set your API key
  export DEEPSEEK_API_KEY='your-key-here'
  
  # Generate for HSK 1
  python scripts/ai_sentences.py --level hsk1
  
  # Generate for all levels (takes a while)
  python scripts/ai_sentences.py
  
  # Dry run — show what would be sent
  python scripts/ai_sentences.py --level hsk1 --dry-run
"""

import json
import os
import subprocess
import sys
import time
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "hsk_daily.json"

BATCH_SIZE = 25  # words per API call
RATE_LIMIT_SEC = 1.5  # seconds between API calls

# HSK level names for the prompt
HSK_NAMES = {
    1: "HSK 1 (Beginner — 300 words, simple daily vocabulary)",
    2: "HSK 2 (Elementary — 197 words, basic conversations)",
    3: "HSK 3 (Intermediate — 493 words, daily life topics)",
    4: "HSK 4 (Upper Intermediate — 990 words, broader topics)",
    5: "HSK 5 (Advanced — 1579 words, news and complex topics)",
    6: "HSK 6 (Proficient — 1777 words, academic and literary)",
    7: "HSK 7-9 (Mastery — 5562 words, near-native fluency)",
}


def load_existing():
    """Load the current vocabulary data."""
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_data(data):
    """Save updated vocabulary data."""
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def call_deepseek(prompt, dry_run=False):
    """Call the DeepSeek API with a prompt. Returns the response text."""
    if dry_run:
        print(f"[DRY RUN] Would send prompt ({len(prompt)} chars)")
        return None
    
    # Build the request
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are a Chinese language expert. Generate example sentences for HSK vocabulary learning. Return ONLY valid JSON, no other text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }
    
    # Get API key from environment
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("ERROR: DEEPSEEK_API_KEY environment variable not set")
        print("  export DEEPSEEK_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Call via curl (since we have it available)
    import tempfile
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
            print(f"  curl error: {result.stderr}")
            return None
        
        response = json.loads(result.stdout)
        
        # Check for API errors
        if "error" in response:
            print(f"  API error: {response['error']}")
            return None
        
        if "choices" not in response or len(response["choices"]) == 0:
            print(f"  Unexpected response: {response}")
            return None
        
        content = response["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        print(f"  Request failed: {e}")
        return None
    finally:
        os.unlink(req_file)


def build_prompt(words_batch, level):
    """Build a prompt asking DeepSeek to generate example sentences for a batch of words."""
    level_desc = HSK_NAMES.get(level, f"HSK Level {level}")
    
    words_list = []
    for w in words_batch:
        words_list.append({
            "id": w["id"],
            "word": w["word"],
            "pinyin": w.get("pinyin_text", ""),
            "english": w.get("english", ""),
            "pos": w.get("pos", "")
        })
    
    prompt = f"""Generate natural example sentences for these {level_desc} Chinese vocabulary words.

For EACH word, provide ONE example sentence that:
1. Uses grammar and vocabulary appropriate for {level_desc} learners
2. Sounds natural in everyday Chinese
3. Demonstrates the word's meaning clearly
4. Is short enough for a beginner/intermediate learner to understand

Return a valid JSON array ONLY, with this exact structure for each word:
[{{"id": "hsk1_0001", "zh": "example sentence in Chinese", "pinyin": "pinyin with tone marks", "en": "English translation"}}, ...]

Words to process:
{json.dumps(words_list, ensure_ascii=False, indent=2)}
"""
    return prompt


def parse_sentences_response(content):
    """Parse the DeepSeek response to extract sentence data."""
    if not content:
        return None
    
    # Try to parse as JSON
    # The model might wrap in markdown code blocks
    text = content.strip()
    
    # Strip markdown code fences if present
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        sentences = json.loads(text)
        if isinstance(sentences, list):
            return sentences
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON array in the text
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        try:
            sentences = json.loads(match.group())
            if isinstance(sentences, list):
                return sentences
        except json.JSONDecodeError:
            pass
    
    print(f"  WARNING: Could not parse response as JSON")
    print(f"  Response starts with: {text[:200]}")
    return None


def process_level(data, level_key, dry_run=False):
    """Process all words at a given HSK level."""
    level_num = int(level_key.replace("hsk", "").replace("79", "7"))
    if level_num > 6:
        level_num = 7
    
    # Get words that need sentences (skip hand-crafted ones)
    words_to_process = []
    for w in data["words"]:
        if w["hsk_level"] != level_num:
            continue
        # Skip words that already have hand-crafted examples (with proper pinyin_parts)
        if w.get("example") and w["example"].get("pinyin_parts") and len(w["example"]["pinyin_parts"]) > 1:
            continue
        words_to_process.append(w)
    
    if not words_to_process:
        print(f"  No words need processing at {level_key}")
        return 0
    
    print(f"  Processing {len(words_to_process)} words in {level_key}...")
    
    total_updated = 0
    total_words = len(words_to_process)
    
    # Process in batches
    for batch_start in range(0, total_words, BATCH_SIZE):
        batch = words_to_process[batch_start:batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (total_words + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"    Batch {batch_num}/{total_batches} ({len(batch)} words)...")
        
        prompt = build_prompt(batch, level_num)
        response = call_deepseek(prompt, dry_run=dry_run)
        
        if dry_run:
            print(f"      Prompt size: {len(prompt)} chars")
            continue
        
        if not response:
            print(f"      Failed to get response for batch {batch_num}")
            print(f"      Waiting {RATE_LIMIT_SEC}s before retry...")
            time.sleep(RATE_LIMIT_SEC * 3)
            response = call_deepseek(prompt, dry_run=dry_run)
            if not response:
                print(f"      Skipping batch {batch_num}")
                continue
        
        sentences = parse_sentences_response(response)
        
        if not sentences:
            print(f"      Could not parse sentences for batch {batch_num}")
            continue
        
        # Match sentences back to words
        for sent_data in sentences:
            word_id = sent_data.get("id", "")
            zh = sent_data.get("zh", "")
            py = sent_data.get("pinyin", "")
            en = sent_data.get("en", "")
            
            if not word_id or not zh:
                continue
            
            # Find the word in the data
            for w in data["words"]:
                if w["id"] == word_id:
                    w["example"] = {
                        "zh": zh,
                        "pinyin": py,
                        "pinyin_parts": [],
                        "pinyin_tones": [],
                        "en": en
                    }
                    total_updated += 1
                    break
        
        print(f"      Updated {len(sentences)}/{len(batch)} words in this batch")
        
        # Rate limiting
        if batch_start + BATCH_SIZE < total_words:
            time.sleep(RATE_LIMIT_SEC)
    
    return total_updated


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate example sentences using DeepSeek AI")
    parser.add_argument("--level", help="Level to process (e.g., hsk1, hsk2, hsk3)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be sent without calling API")
    parser.add_argument("--save-every", type=int, default=5, help="Save data every N batches (default: 5)")
    args = parser.parse_args()
    
    print("Loading vocabulary data...")
    data = load_existing()
    
    if args.level:
        levels = [args.level]
    else:
        levels = [l["id"] for l in data["meta"]["levels"] if l["word_count"] > 0]
    
    print(f"Using DeepSeek API: endpoint=https://api.deepseek.com/chat/completions")
    print(f"Batch size: {BATCH_SIZE}, Rate limit: {RATE_LIMIT_SEC}s")
    if args.dry_run:
        print("[DRY RUN MODE — no API calls will be made]")
    print()
    
    total = 0
    for lv in levels:
        count = process_level(data, lv, dry_run=args.dry_run)
        total += count
        if not args.dry_run:
            save_data(data)
        print()
    
    if args.dry_run:
        print(f"Dry run complete. Would process {total} words.")
    else:
        print(f"Done! Updated {total} words with AI-generated example sentences.")
        # Show word count
        with_examples = sum(1 for w in data["words"] if w.get("example") and w["example"].get("zh"))
        print(f"Total words with examples: {with_examples}/{len(data['words'])}")


if __name__ == "__main__":
    main()
