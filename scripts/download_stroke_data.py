#!/usr/bin/env python3
"""
Download hanzi-writer stroke data for all unique characters in the HSK vocabulary.
Saves to data/char_strokes/ for offline use.

Usage:
    python3 scripts/download_stroke_data.py

This downloads per-character JSON files from hanzi-writer-data CDN.
~5,000 unique characters × ~2KB each ≈ 10MB total.
"""

import json
import os
import sys
import urllib.request
import time

STROKE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'char_strokes')
HSK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'hsk_daily.json')
CDN_URL = 'https://cdn.jsdelivr.net/npm/hanzi-writer-data@3.5/{char}.json'


def get_unique_chars():
    """Extract all unique characters from the HSK word list."""
    if not os.path.exists(HSK_DATA_PATH):
        # Try per-level files
        levels_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'levels')
        chars = set()
        if os.path.isdir(levels_dir):
            for f in sorted(os.listdir(levels_dir)):
                if f.endswith('.json'):
                    with open(os.path.join(levels_dir, f), 'r') as fh:
                        data = json.load(fh)
                        for w in data.get('words', []):
                            for ch in w.get('word', ''):
                                chars.add(ch)
        return sorted(chars)

    with open(HSK_DATA_PATH, 'r') as f:
        data = json.load(f)

    chars = set()
    for w in data.get('words', []):
        for ch in w.get('word', ''):
            chars.add(ch)
    return sorted(chars)


def download_stroke_data(char):
    """Download stroke data for a single character."""
    url = CDN_URL.format(char=char)
    dest = os.path.join(STROKE_DIR, f'{char}.json')

    if os.path.exists(dest):
        return 'cached'

    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'mei-ri-zi/1.0 (stroke data downloader)'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            with open(dest, 'wb') as f:
                f.write(data)
        return 'downloaded'
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return 'not_found'
        return f'http_error_{e.code}'
    except Exception as e:
        return f'error_{e}'


def main():
    os.makedirs(STROKE_DIR, exist_ok=True)

    chars = get_unique_chars()
    total = len(chars)
    print(f'Found {total} unique characters to download')

    cached = 0
    downloaded = 0
    not_found = 0
    errors = 0

    for i, ch in enumerate(chars):
        result = download_stroke_data(ch)
        if result == 'cached':
            cached += 1
        elif result == 'downloaded':
            downloaded += 1
            print(f'  [{i+1}/{total}] Downloaded: {ch}')
        elif result == 'not_found':
            not_found += 1
            print(f'  [{i+1}/{total}] Not found: {ch}')
        else:
            errors += 1
            print(f'  [{i+1}/{total}] Error: {ch} — {result}')

        # Be polite to CDN
        if i % 50 == 49:
            time.sleep(0.5)

    print(f'\nDone! {downloaded} downloaded, {cached} cached, {not_found} not found, {errors} errors')
    print(f'Total: {total} characters in {STROKE_DIR}')


if __name__ == '__main__':
    main()
