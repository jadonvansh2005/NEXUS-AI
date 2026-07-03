import * as vscode from 'vscode';
import { UpssChatViewProvider } from './webviewProvider';

export function activate(context: vscode.ExtensionContext) {
    console.log('UPSS Developer Assistant Extension is now active!');

    // Register Webview Chat Provider for the Sidebar Panel
    const provider = new UpssChatViewProvider(context.extensionUri);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            'upss-chat-view',
            provider
        )
    );

    // Register command to insert generated code block at cursor
    const insertCodeCmd = vscode.commands.registerCommand('upss.insertCode', (code: string) => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            editor.edit(editBuilder => {
                editBuilder.insert(editor.selection.active, code);
            });
            vscode.window.showInformationMessage('Code snippet inserted successfully!');
        } else {
            vscode.window.showWarningMessage('No active editor found to insert code.');
        }
    });

    // Register command to save and create a file from generated code
    const createFileCmd = vscode.commands.registerCommand('upss.createFile', async (code: string, suggestedName?: string) => {
        const defaultName = suggestedName || 'generated_code.py';
        const fileUri = await vscode.window.showSaveDialog({
            defaultUri: vscode.workspace.workspaceFolders 
                ? vscode.Uri.joinPath(vscode.workspace.workspaceFolders[0].uri, defaultName)
                : vscode.Uri.file(defaultName),
            filters: { 'All Files': ['*'] }
        });

        if (fileUri) {
            try {
                const uint8 = new Uint8Array(Buffer.from(code));
                await vscode.workspace.fs.writeFile(fileUri, uint8);
                const doc = await vscode.workspace.openTextDocument(fileUri);
                await vscode.window.showTextDocument(doc);
                vscode.window.showInformationMessage(`File created successfully: ${fileUri.fsPath}`);
            } catch (err: any) {
                vscode.window.showErrorMessage(`Failed to create file: ${err.message}`);
            }
        }
    });

    context.subscriptions.push(insertCodeCmd, createFileCmd);
}

export function deactivate() {}
