import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export class UpssChatViewProvider implements vscode.WebviewViewProvider {
    private _view?: vscode.WebviewView;

    constructor(private readonly _extensionUri: vscode.Uri) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // Handle messages sent from Webview Javascript environment
        webviewView.webview.onDidReceiveMessage(async (data) => {
            switch (data.type) {
                case 'sendMessage': {
                    const userMsg = data.message;
                    const convId = data.conversationId;
                    
                    // Read active workspace folder path from VS Code API
                    const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath || '';
                    const enrichedMsg = userMsg + (workspaceFolder ? ` \n[workspace: ${workspaceFolder}]` : '');

                    try {
                        const response = await this._postMessageToBackend(enrichedMsg, convId);
                        webviewView.webview.postMessage({
                            type: 'receiveResponse',
                            data: response
                        });
                    } catch (error: any) {
                        vscode.window.showErrorMessage(`UPSS Connection Error: ${error.message}`);
                        webviewView.webview.postMessage({
                            type: 'receiveError',
                            message: `Failed to connect to backend server: ${error.message}. Is your local server running?`
                        });
                    }
                    break;
                }
                case 'insertCode': {
                    vscode.commands.executeCommand('upss.insertCode', data.code);
                    break;
                }
                case 'createFile': {
                    vscode.commands.executeCommand('upss.createFile', data.code, data.filename);
                    break;
                }
                case 'showInfo': {
                    vscode.window.showInformationMessage(data.message);
                    break;
                }
            }
        });
    }

    private _getHtmlForWebview(webview: vscode.WebviewView['webview']): string {
        const htmlPath = path.join(this._extensionUri.fsPath, 'src', 'webview', 'chat.html');
        let htmlContent = '';
        
        try {
            htmlContent = fs.readFileSync(htmlPath, 'utf8');
        } catch (e) {
            htmlContent = `
                <!DOCTYPE html>
                <html>
                <body>
                    <h3>UPSS Assistant Sidebar</h3>
                    <p>Failed to load chat.html. Please ensure it is present in src/webview/chat.html</p>
                </body>
                </html>
            `;
        }
        return htmlContent;
    }

    private async _postMessageToBackend(message: string, conversationId?: string): Promise<any> {
        // Hits the local FastAPI chat endpoint
        const url = 'http://localhost:8000/chat';
        
        const params = new URLSearchParams();
        params.append('message', message);
        if (conversationId) {
            params.append('conversation_id', conversationId);
        }

        // VS Code's runtime uses Node 18+ which has native global fetch
        const response = await fetch(url, {
            method: 'POST',
            body: params,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP Error ${response.status}: ${await response.text()}`);
        }

        return await response.json();
    }
}
