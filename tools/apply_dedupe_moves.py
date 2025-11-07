#!/usr/bin/env python3
"""Safe dedupe operations: move extras duplicates to archive and replace kit duplicates with README pointers.

Run this only after review. It is conservative: moves files to archive and creates README pointers in kit folders (except baremetal kit).
"""
import os
import shutil
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ARCHIVE = os.path.join(ROOT, 'archive', 'duplicates', datetime.now().strftime('%Y%m%d'))
os.makedirs(ARCHIVE, exist_ok=True)

extras = [
    'extras/neo-openai-skeleton.py',
    'extras/neo-orchestrator-real.py',
    'extras/requirements-2.txt',
    'extras/requirements.txt',
    'extras/run-evals.py',
    'extras/test-actions.py',
    'extras/app-4.py',
    'extras/mint-jwt.py',
    'extras/requirements-1.txt',
    'extras/requirements-6.txt',
    'extras/app-1.py',
    'extras/app-2.py',
    'extras/app-3.py',
    'extras/app.py',
    'extras/deploy.sh',
    'extras/provision.sh',
    'extras/requirements-3.txt',
    'extras/requirements-4.txt',
    'extras/requirements-5.txt',
    'extras/worker.py',
]

kit_file_patterns = [
    'api/neo_openai_skeleton.py',
    'orchestrator/neo_orchestrator_real.py',
    'worker/worker.py',
    'actions/app.py',
    'api/requirements.txt',
    'orchestrator/requirements.txt',
]

def move_to_archive(rel_path):
    src = os.path.join(ROOT, rel_path.replace('/', os.sep))
    if not os.path.exists(src):
        return False
    dest = os.path.join(ARCHIVE, os.path.relpath(src, ROOT))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(src, dest)
    print('moved', rel_path, '->', os.path.relpath(dest, ROOT))
    return True

def replace_with_readme(path, canonical):
    # Create README.md pointing to canonical path
    content = f"This file was canonicalized. See the canonical source in the repository:\n\n{canonical}\n"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('wrote pointer', os.path.relpath(path, ROOT))

def process_extras():
    for e in extras:
        move_to_archive(e)

def process_kits():
    kits_dir = os.path.join(ROOT, 'kits')
    for kit_name in os.listdir(kits_dir):
        kit_path = os.path.join(kits_dir, kit_name, 'neo-godmode')
        if not os.path.isdir(kit_path):
            continue
        # skip baremetal (keep canonical)
        if 'baremetal' in kit_name:
            continue
        for pattern in kit_file_patterns:
            rel = os.path.join('kits', kit_name, 'neo-godmode', pattern)
            abs_path = os.path.join(ROOT, *rel.split('/'))
            if os.path.exists(abs_path):
                # move original to archive
                move_to_archive(rel)
                # create README pointer in place
                replace_with_readme(abs_path, f'kits/neo-godmode-baremetal-kit/neo-godmode/{pattern}')

def main():
    print('Archive root:', os.path.relpath(ARCHIVE, ROOT))
    process_extras()
    process_kits()
    print('Done.')

if __name__ == '__main__':
    main()
