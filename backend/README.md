# Nexus-AI Local Filesystem MCP — Step 1

This package is isolated from existing `tools/file_tools`, `tools/terminal`, registry, agents and FastAPI routes. It does not auto-register itself.

## Install

From `D:\UPSS\backend`, with your current venv active:

```powershell
python -m pip install -r requirements-mcp.txt
```

This separate dependency file does not overwrite your existing requirements file. It targets the official MCP Python SDK v2 (`MCPServer` API).

## Allowed roots

Default root: `D:\UPSS\backend`.

To allow additional folders intentionally, set this before launching (Windows uses semicolon-separated paths):

```powershell
$env:NEXUS_MCP_ALLOWED_ROOTS = "D:\UPSS\backend;D:\Projects\SelectedFolder"
```

Unset means only the default backend root. Configured roots must already exist.

## Run

Run from the backend directory (where `mcp_servers` lives):

```powershell
python -m mcp_servers.filesystem.server
```

It uses stdio; no startup banner should be printed to stdout because stdout carries MCP protocol messages.

## Tools

- `list_directory(path)`
- `search_files(root, pattern="*", max_results=100)`
- `read_file(path)` — UTF-8 text, up to 1 MB, returns SHA-256
- `create_file(path, content, confirm=false)` — explicit confirm argument, never overwrites
- `edit_file(path, content, expected_sha256, confirm=false)` — confirm plus hash from fresh read
- `move_file(source, destination, confirm=false)` — file-only, within roots, no overwrite

`confirm=true` is only a server-side safeguard; it is not a real user approval UI. Until Nexus-AI's approval workflow is integrated, do not expose write tools to autonomous workflows.

## Safety controls

- Resolve requested paths and enforce containment under configured roots.
- Skip/reject paths resolving outside configured roots, including escaping symlinks.
- 1 MB read/write limit; search max 500 results; listing max 500 entries.
- Skip common dependency/cache directories during search.
- No overwrite on create/move; edit requires matching SHA-256.
- Directory moves and shell commands are not supported.

These are defense-in-depth controls, not an OS sandbox against another process running as the same user.

## Test filesystem logic (does not require MCP installed)

```powershell
python -m unittest discover -s tests -p "test_filesystem_core.py" -v
```

Then verify the SDK import after installing the dependency:

```powershell
python -c "from mcp.server import MCPServer; print('MCP SDK import OK')"
```

Do not integrate this server into the existing tool registry until standalone tests and a real MCP-client/Inspector smoke test pass.
