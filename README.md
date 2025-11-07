# Neo Godmode — Master Toolkit

A unified, normalized collection of all Neo Godmode kits (baremetal, pro, ultra, originals) plus the latest **Prompt Kit**.
This repo deduplicates overlapping files, standardizes names, and collects prompts, branding, templates, docs, and extras in predictable locations.

## Structure
```
neo-godmode-master/
 ├─ kits/                 # Original kits preserved (normalized names)
 ├─ prompts/              # Aggregated prompts & system instructions (deduped)
 ├─ branding/             # Taglines, hero copy, marketing snippets
 ├─ templates/            # JSON/YAML templates & configs
 ├─ docs/                 # READMEs and guides
 ├─ extras/               # Useful scripts/snippets
 ├─ tools/                # Installer scripts (bash/powershell)
 └─ vscode-extension/     # Ready-to-package VS Code extension
```

## Quick Install
### macOS/Linux
```bash
cd neo-godmode-master/tools
./install.sh
```
### Windows (PowerShell)
```powershell
cd neo-godmode-master\tools
./install.ps1
```

Content installs to `~/.neo-godmode/` by default (override by editing scripts).

## VS Code / Cursor Extension
- Extension ID: `neo-godmode-vscode`
- Commands:
  - **Neo Godmode: Insert Master Prompt** — inserts the master system prompt into the current editor.
  - **Neo Godmode: New Prompt File** — creates a new prompt file from template.
- Packaging: produce a `.vsix` by zipping the `neo-godmode-vscode` folder and renaming to `.vsix`, or use `vsce package`.

## GitHub Push
Use the bootstrap commands (below) to initialize and push this repo.
