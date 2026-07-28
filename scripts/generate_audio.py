#!/usr/bin/env python3
"""
generate_audio.py — Generate Edge TTS audio for HSK words.

Uses Microsoft Edge TTS (free, no API key) with zh-CN-XiaoxiaoNeural voice,
slowed by 5% for learner clarity.

Usage:
  python scripts/generate_audio.py                    # generate all audio
  python scripts/generate_audio.py --hsk-level 1       # generate only HSK 1
  python scripts/generate_audio.py --force             # regenerate existing files
"""

import asyncio
import json
import argparse
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-5%"

AUDIO_DIR = Path(__file__).parent.parent / "audio"
DATA_FILE = Path(__file__).parent.parent / "data" / "hsk_daily.json"
INDEX_FILE = AUDIO_DIR / "index.json"


async def tts(text: str, out_path: Path) -> bool:
    """Generate TTS audio file. Returns True on success."""
    try:
        communicate = edge_tts.Communicate(text, voice=VOICE, rate=RATE)
        await communicate.save(str(out_path))
        return True
    except Exception as e:
        print(f"    ERROR: {e}")
        return False


# Rate limiting: delay between requests to be respectful to Edge TTS
_REQUEST_DELAY = 0.4  # seconds between each TTS request


async def generate_for_word(word: dict, force: bool = False) -> dict:
    """Generate audio files for a single word. Returns the index entry."""
    wid = word["id"]
    out_dir = AUDIO_DIR / "word_audio" / wid
    out_dir.mkdir(parents=True, exist_ok=True)

    word_mp3 = out_dir / "word.mp3"
    sent_mp3 = out_dir / "sentence.mp3"

    entry = {}

    # Generate word audio
    if force or not word_mp3.exists():
        print(f"  [{wid}] word: {word['word']}")
        success = await tts(word["word"], word_mp3)
        if success:
            entry["word"] = f"word_audio/{wid}/word.mp3"
        await asyncio.sleep(_REQUEST_DELAY)
    else:
        entry["word"] = f"word_audio/{wid}/word.mp3"

    # Generate sentence audio
    example = word.get("example", {})
    sentence = example.get("zh", "")
    if sentence:
        if force or not sent_mp3.exists():
            print(f"  [{wid}] sentence")
            success = await tts(sentence, sent_mp3)
            if success:
                entry["sentence"] = f"word_audio/{wid}/sentence.mp3"
            await asyncio.sleep(_REQUEST_DELAY)
        else:
            entry["sentence"] = f"word_audio/{wid}/sentence.mp3"

    return entry


async def main():
    parser = argparse.ArgumentParser(description="Generate Edge TTS audio for HSK words")
    parser.add_argument("--hsk-level", type=int, help="Generate only for specific HSK level (1-9)")
    parser.add_argument("--force", action="store_true", help="Regenerate existing audio files")
    parser.add_argument("--delay", type=float, default=0.4, help="Delay in seconds between requests (default: 0.4)")
    args = parser.parse_args()

    global _REQUEST_DELAY
    _REQUEST_DELAY = args.delay

    if not DATA_FILE.exists():
        print(f"Data file not found: {DATA_FILE}")
        print("Run scripts/generate_data.py first")
        sys.exit(1)

    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    
    # Load existing index to preserve already-generated entries
    index = {"version": 1, "generated_at": "", "files": {}}
    if INDEX_FILE.exists():
        try:
            existing = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
            index["files"] = existing.get("files", {})
        except:
            pass

    # Filter by HSK level
    level_map = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 7, 9: 7}
    if args.hsk_level:
        lnum = level_map.get(args.hsk_level, args.hsk_level)
        words = [w for w in data["words"] if w.get("hsk_level") == lnum]
        print(f"HSK level {args.hsk_level}: {len(words)} words")
    else:
        words = data["words"]
        print(f"Total words: {len(words)}")

    # Check which words already have audio
    todo = []
    for w in words:
        wid = w["id"]
        existing = index["files"].get(wid, {})
        has_word = existing.get("word") and (AUDIO_DIR / existing["word"]).exists()
        has_sent = existing.get("sentence") and (AUDIO_DIR / existing["sentence"]).exists()
        if not (has_word and has_sent):
            todo.append(w)

    print(f"Need to generate: {len(todo)} words (already have {len(words) - len(todo)})")
    print(f"Rate limit: {_REQUEST_DELAY}s between requests (~{len(todo)*2*_REQUEST_DELAY:.0f}s total)")
    print()

    # Generate audio
    total = len(todo)
    completed = 0

    for i, word in enumerate(todo):
        entry = await generate_for_word(word, force=args.force)
        if entry:
            if word["id"] not in index["files"]:
                index["files"][word["id"]] = {}
            index["files"][word["id"]].update(entry)
            completed += 1

        if (i + 1) % 10 == 0 or (i + 1) == total:
            elapsed = (i + 1) * 2 * _REQUEST_DELAY
            remaining = (total - i - 1) * 2 * _REQUEST_DELAY
            print(f"  Progress: {i+1}/{total} (est. remaining: {remaining:.0f}s)")

    # Write index
    index["generated_at"] = "2026-07-27T00:00:00Z"
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"\nDone! Generated audio for {completed}/{total} words")
    print(f"Total in index: {len(index['files'])} words")
    print(f"Index written to {INDEX_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
