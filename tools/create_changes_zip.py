import os
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

FILES = [
    '.github/copilot-instructions.md',
    'CONTRIBUTING.md',
    'tools/find_duplicates.py',
    'tools/mirror_file_to_kits.py',
    '.github/workflows/duplicate-check.yml',
    'kits/neo-godmode-baremetal-kit/.github/copilot-instructions.md',
    'kits/neo-godmode-kit/.github/copilot-instructions.md',
    'kits/neo-godmode-kit-1/.github/copilot-instructions.md',
    'kits/neo-godmode-pro-kit/.github/copilot-instructions.md',
    'kits/neo-godmode-ultra-kit/.github/copilot-instructions.md',
    'kits/neo-godmode-kit/neo-godmode/actions/app.py',
    'kits/neo-godmode-kit/neo-godmode/actions/app.py.bak',
    'kits/neo-godmode-kit-1/neo-godmode/actions/app.py',
    'kits/neo-godmode-kit-1/neo-godmode/actions/app.py.bak',
    'kits/neo-godmode-pro-kit/neo-godmode/actions/app.py',
    'kits/neo-godmode-pro-kit/neo-godmode/actions/app.py.bak',
    'kits/neo-godmode-ultra-kit/neo-godmode/actions/app.py',
    'kits/neo-godmode-ultra-kit/neo-godmode/actions/app.py.bak',
    'kits/neo-godmode-kit/neo-godmode/worker/worker.py',
    'kits/neo-godmode-kit-1/neo-godmode/worker/worker.py',
    'kits/neo-godmode-pro-kit/neo-godmode/worker/worker.py',
    'kits/neo-godmode-ultra-kit/neo-godmode/worker/worker.py',
]

def create_zip():
    zip_path = os.path.join(ROOT, 'neo-godmode-dedupe-changes.zip')
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for rel in FILES:
            src = os.path.join(ROOT, *rel.split('/'))
            if os.path.exists(src):
                z.write(src, arcname=rel)
                print('added', rel)
            else:
                print('missing', rel)
    print('\nCreated', zip_path)

if __name__ == '__main__':
    create_zip()
