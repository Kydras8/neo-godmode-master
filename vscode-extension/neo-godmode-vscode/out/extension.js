const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

async function activate(context) {
  const insertCmd = vscode.commands.registerCommand('neo-godmode.insertPrompt', async () => {
    try {
      const extPath = context.extensionPath;
      const repoRoot = path.resolve(extPath, '..', '..');
      const promptPath = path.join(repoRoot, 'prompts', 'neo-godmode-master-prompt.md');
      const content = fs.readFileSync(promptPath, 'utf8');
      const editor = vscode.window.activeTextEditor;
      if (!editor) { vscode.window.showErrorMessage('Open a file to insert the prompt.'); return; }
      editor.edit(editBuilder => { editBuilder.insert(editor.selection.active, content); });
      vscode.window.showInformationMessage('Neo Godmode prompt inserted.');
    } catch (e) {
      vscode.window.showErrorMessage('Failed to insert prompt: ' + e.message);
    }
  });

  const newPromptCmd = vscode.commands.registerCommand('neo-godmode.newPromptFile', async () => {
    try {
      const ws = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath;
      if (!ws) { vscode.window.showErrorMessage('Open a workspace first.'); return; }
      const filename = path.join(ws, 'neo-godmode-prompt.md');
      const template = '# Neo Godmode Prompt\n\n(Place your customized operating instructions here.)\n';
      fs.writeFileSync(filename, template, { flag: 'wx' });
      const doc = await vscode.workspace.openTextDocument(filename);
      await vscode.window.showTextDocument(doc);
      vscode.window.showInformationMessage('New prompt file created.');
    } catch (e) {
      vscode.window.showErrorMessage('Failed to create prompt file: ' + e.message);
    }
  });

  context.subscriptions.push(insertCmd, newPromptCmd);
}

function deactivate() {}

module.exports = { activate, deactivate };
