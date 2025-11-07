{
  "name": "neo-godmode-vscode",
  "displayName": "Neo Godmode",
  "publisher": "Kydras8",
  "description": "Command palette helpers and skeletons for Neo Godmode Army workflows.",
  "version": "0.1.1",
  "engines": {
    "vscode": "^1.84.0"
  },
  "categories": ["Other"],
  "main": "./out/extension.js",
  "activationEvents": [
    "onCommand:neo-godmode.insertPrompt",
    "onCommand:neo-godmode.newPromptFile",
    "onCommand:neo-godmode.insertArmySkeleton"
  ],
  "contributes": {
    "commands": [
      {
        "command": "neo-godmode.insertPrompt",
        "title": "Neo Godmode: Insert Master Prompt"
      },
      {
        "command": "neo-godmode.newPromptFile",
        "title": "Neo Godmode: New Prompt File"
      },
      {
        "command": "neo-godmode.insertArmySkeleton",
        "title": "Neo Godmode: Insert [ARMY] Command Skeleton"
      }
    ],
    "keybindings": [
      {
        "command": "neo-godmode.insertPrompt",
        "key": "ctrl+alt+8",
        "when": "editorTextFocus"
      },
      {
        "command": "neo-godmode.insertArmySkeleton",
        "key": "ctrl+alt+a",
        "when": "editorTextFocus"
      }
    ]
  },
  "scripts": {
    "vscode:prepublish": "tsc -p ./",
    "compile": "tsc -w",
    "build": "tsc -p ./",
    "package": "vsce package"
  },
  "devDependencies": {
    "@types/vscode": "^1.84.0",
    "tslib": "^2.6.2",
    "typescript": "^5.4.0",
    "vsce": "^2.15.0"
  }
}
