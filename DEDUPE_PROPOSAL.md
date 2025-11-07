DEDUPE PROPOSAL
================

This document lists candidate files to remove or archive as part of an aggressive deduplication step. Do NOT apply deletions until maintainers review and approve. The goal: keep `kits/neo-godmode-baremetal-kit/neo-godmode/` as the canonical source and remove or archive identical copies in `extras/` and other kit folders.

Summary of recommendation

- Keep canonical copies in: `kits/neo-godmode-baremetal-kit/neo-godmode/`
- Move exact duplicate files found under `extras/` to `archive/duplicates/` (or delete) — these appear to be snapshots.
- For kit copies (kits/*/neo-godmode/...), remove duplicate files and replace with a small README pointing to the canonical source. Alternatively, keep the copies but mark `baremetal-kit` as canonical in CONTRIBUTING.md (current state).

Exact candidates (from automated scan) — review each before delete:

1) Files in `extras/` that duplicate kit files (move to archive or delete):

- extras/neo-openai-skeleton.py
- extras/neo-orchestrator-real.py
DEDUPE PROPOSAL
===============

This document lists candidate files to remove or archive as part of an aggressive deduplication step. Do NOT apply deletions until maintainers review and approve. The goal: keep `kits/neo-godmode-baremetal-kit/neo-godmode/` as the canonical source and remove or archive identical copies in `extras/` and other kit folders.

Summary of recommendation

1. Keep canonical copies in: `kits/neo-godmode-baremetal-kit/neo-godmode/`
1. Move exact duplicate files found under `extras/` to `archive/duplicates/` (or delete) — these appear to be snapshots.
1. For kit copies (kits/*/neo-godmode/...), remove duplicate files and replace with a small README pointing to the canonical source. Alternatively, keep the copies but mark `baremetal-kit` as canonical in CONTRIBUTING.md (current state).

Exact candidates (from automated scan) — review each before delete:

1) Files in `extras/` that duplicate kit files (move to archive or delete):

- extras/neo-openai-skeleton.py
- extras/neo-orchestrator-real.py
- extras/requirements-2.txt
- extras/requirements.txt
- extras/run-evals.py
- extras/test-actions.py
- extras/app-4.py
- extras/mint-jwt.py
- extras/requirements-1.txt
- extras/requirements-6.txt
- extras/app-1.py
- extras/app-2.py
- extras/app-3.py
DEDUPE PROPOSAL
===============

This document lists candidate files to remove or archive as part of an aggressive deduplication step. Do NOT apply deletions until maintainers review and approve. The goal: keep `kits/neo-godmode-baremetal-kit/neo-godmode/` as the canonical source and remove or archive identical copies in `extras/` and other kit folders.

Summary of recommendation

- Keep canonical copies in `kits/neo-godmode-baremetal-kit/neo-godmode/`.
- Move exact duplicate files found under `extras/` to `archive/duplicates/` (or delete) — these appear to be snapshots.
- For kit copies (kits/*/neo-godmode/...), either delete duplicate files and replace with a small README pointing to the canonical source, or keep the copies but mark `baremetal-kit` as canonical in `CONTRIBUTING.md`.

Exact candidates (from automated scan) — review each before delete

1) Files in `extras/` that duplicate kit files (move to archive or delete):

- extras/neo-openai-skeleton.py
- extras/neo-orchestrator-real.py
- extras/requirements-2.txt
- extras/requirements.txt
- extras/run-evals.py
- extras/test-actions.py
- extras/app-4.py
- extras/mint-jwt.py
- extras/requirements-1.txt
- extras/requirements-6.txt
- extras/app-1.py
- extras/app-2.py
- extras/app-3.py
- extras/app.py
- extras/deploy.sh
- extras/provision.sh
- extras/requirements-3.txt
- extras/requirements-4.txt
- extras/requirements-5.txt
- extras/worker.py

Rationale: these are exact copies of kit files and appear to be maintenance snapshots. Moving them to `archive/duplicates/` preserves history while reducing noise.

Kit copies that can be canonicalized to `baremetal-kit`
----------------------------------------------------

The proposed action is to delete duplicates in kit folders and keep only the `baremetal-kit` canonical copy, or replace duplicates with a small README that points at the canonical file.

- kits/*/neo-godmode/api/neo_openai_skeleton.py
- kits/*/neo-godmode/orchestrator/neo_orchestrator_real.py
- kits/*/neo-godmode/worker/worker.py
- kits/*/neo-godmode/actions/app.py  (note: backups `.bak` were created for some kits during mirroring)
- kits/*/neo-godmode/api/requirements.txt
- kits/*/neo-godmode/orchestrator/requirements.txt

Rationale: These files are identical copies across kit variants. Keeping a single canonical copy reduces maintenance burden. Deletions should be accompanied by update notes to CI/infrastructure references that may point to kit-local paths.

Templates and infra duplicates to consolidate to `templates/`
---------------------------------------------------------

- kits/neo-godmode-baremetal-kit/neo-godmode/infra/loki/local-config.yaml  -> duplicate of templates/local-config.yaml
- kits/neo-godmode-baremetal-kit/neo-godmode/infra/promtail/config.yml -> duplicate of templates/config.yml

Proposed process (safe, review-first)

1. Create a new branch `dedupe/proposal` and commit the current tools/docs (done).
1. Create an archive folder `archive/duplicates/YYYYMMDD/` and move all `extras/*` files there. Commit.
1. For kit duplicates, either:
   a) Replace the duplicate file with a tiny `README.md` containing a pointer to the canonical `baremetal-kit` path, or
   b) Delete the duplicate entirely (only after CI run and integration test).
1. Run integration smoke tests (docker compose up, run basic API call, ensure CI passes).
1. Remove `archive/duplicates` after maintainers confirm.

Safety notes

1. Don't delete files yet. This proposal is purely to get approval and to let reviewers point out exceptions.
1. Where possible, create backups (e.g., `.bak`) or move files to `archive/duplicates/` rather than permanent deletion.

Next steps

1. Please review this list and indicate which files I should move to `archive/duplicates/` and which kit duplicates (if any) are safe to remove now. After your approval I will implement the moves/deletions on a dedicated branch and open a PR.
