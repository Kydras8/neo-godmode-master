#!/usr/bin/env python3
"""Simple duplicate finder: scans the repo and reports files with identical contents.

Usage:
  python tools/find_duplicates.py

This is a low-risk helper to discover duplicated files across kit subfolders.
"""
import hashlib
import os
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def find_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        # skip common virtualenv and .git
        if '.git' in dirpath or '__pycache__' in dirpath or 'node_modules' in dirpath:
            continue
        for fn in filenames:
            yield os.path.join(dirpath, fn)

def main():
    by_hash = defaultdict(list)
    total = 0
    for path in find_files(ROOT):
        try:
            h = sha256_file(path)
        except Exception:
            continue
        by_hash[h].append(path)
        total += 1

    dup_groups = [v for v in by_hash.values() if len(v) > 1]
    print(f"Scanned {total} files. Found {len(dup_groups)} duplicate groups.")
    for i, group in enumerate(sorted(dup_groups, key=len, reverse=True), 1):
        print('\n---')
        print(f"Group {i} ({len(group)} files):")
        for p in sorted(group):
            print(' -', os.path.relpath(p, ROOT))

if __name__ == '__main__':
    main()
