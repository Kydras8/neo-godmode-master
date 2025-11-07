# Canonical sources and mirroring

This repository intentionally contains several "kit" copies under `kits/` (baremetal, pro, ultra, ...).
To reduce drift and keep edits reviewable we follow a simple rule:

- The `kits/neo-godmode-baremetal-kit/neo-godmode/` subtree is canonical for code and scripts used by kits.
- To update other kits, either:
  - Edit the canonical file in `baremetal-kit` and run `tools/mirror_file_to_kits.py` to propagate the change (creates .bak backups), or
  - Make a targeted kit-specific change and note the reason in the PR description.

## Tools

- `tools/find_duplicates.py` — scans the repo and reports identical files by content hash.
- `tools/mirror_file_to_kits.py` — mirrors a canonical source into each kit's relative path (non-destructive; creates `.bak`).

## Recommended workflow (safe)

1. Make your change in `kits/neo-godmode-baremetal-kit/neo-godmode/...`.
2. Run `python tools/find_duplicates.py` locally to inspect duplicates.
3. If you intend to propagate the change, run:

```powershell
python tools/mirror_file_to_kits.py --source kits\neo-godmode-baremetal-kit\neo-godmode\path\to\file.py --relpath path\to\file.py
```

1. Review `.bak` files committed to the PR (the mirror tool backs up replaced files).
1. Open a PR and explain whether this is a canonical change or intentionally kit-specific.

## CI check

- The repo contains a lightweight workflow that runs `tools/find_duplicates.py` and uploads the result as an artifact for maintainers to review. It does not fail CI by default.

If you'd like stricter enforcement (fail when duplicates exceed a threshold), open an issue and we can add that check.
