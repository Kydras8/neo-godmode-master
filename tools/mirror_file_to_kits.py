#!/usr/bin/env python3
"""Mirror a file from a canonical location into each kit copy.

This is a safe, non-destructive helper for deduplication:
- It copies SOURCE into each kit at the given RELATIVE_PATH (creating dirs as needed).
- If a destination file exists and differs, it creates a `.bak` backup first.

Usage:
  python tools/mirror_file_to_kits.py \
      --source kits/neo-godmode-baremetal-kit/neo-godmode/api/neo_openai_skeleton.py \
      --relpath api/neo_openai_skeleton.py

Only performs copy; it does not delete files. This keeps changes explicit and reviewable.
"""
import argparse
import filecmp
import os
import shutil
from glob import glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def find_kit_paths(root):
    pattern = os.path.join(root, 'kits', '*', 'neo-godmode')
    for path in glob(pattern):
        yield os.path.abspath(path)

def mirror(source, relpath, dry_run=False):
    src = os.path.abspath(source)
    if not os.path.exists(src):
        raise SystemExit(f"Source not found: {src}")

    changed = []
    for kit in find_kit_paths(ROOT):
        dest = os.path.join(kit, relpath)
        dest_dir = os.path.dirname(dest)
        os.makedirs(dest_dir, exist_ok=True)
        if os.path.exists(dest):
            if filecmp.cmp(src, dest, shallow=False):
                # identical
                continue
            else:
                bak = dest + '.bak'
                print(f"Backing up {os.path.relpath(dest, ROOT)} -> {os.path.relpath(bak, ROOT)}")
                if not dry_run:
                    shutil.copy2(dest, bak)
        print(f"Copying {os.path.relpath(src, ROOT)} -> {os.path.relpath(dest, ROOT)}")
        if not dry_run:
            shutil.copy2(src, dest)
        changed.append(dest)
    return changed

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True, help='Path to canonical source file')
    p.add_argument('--relpath', required=True, help='Relative path inside each kit to copy to')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    changed = mirror(args.source, args.relpath, dry_run=args.dry_run)
    print(f"Done. Files changed: {len(changed)}")

if __name__ == '__main__':
    main()
