"""Local Filesystem MCP server for Nexus-AI; official MCP Python SDK v2."""
import logging
from mcp.server import MCPServer
from mcp_servers.filesystem.core import (
    configured_roots, list_directory as _list_directory, search_files as _search_files,
    read_file as _read_file, create_file as _create_file, edit_file as _edit_file,
    move_file as _move_file,
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nexus.filesystem_mcp")
mcp = MCPServer("nexus-filesystem")

def roots():
    return configured_roots()

@mcp.tool()
def list_directory(path: str) -> dict:
    """List entries inside a configured allowed root."""
    return _list_directory(path, roots())

@mcp.tool()
def search_files(root: str, pattern: str = "*", max_results: int = 100) -> dict:
    """Search filenames under an allowed directory; common cache/dependency folders are skipped."""
    return _search_files(root, pattern, max_results, roots())

@mcp.tool()
def read_file(path: str) -> dict:
    """Read UTF-8 text up to 1 MB and return its SHA-256 digest."""
    return _read_file(path, roots())

@mcp.tool()
def create_file(path: str, content: str, confirm: bool = False) -> dict:
    """Create a new text file after explicit confirmation; never overwrites."""
    return _create_file(path, content, confirm, roots())

@mcp.tool()
def edit_file(path: str, content: str, expected_sha256: str, confirm: bool = False) -> dict:
    """Edit only after confirmation and only when the current SHA-256 matches a fresh read."""
    return _edit_file(path, content, expected_sha256, confirm, roots())

@mcp.tool()
def move_file(source: str, destination: str, confirm: bool = False) -> dict:
    """Move a file within allowed roots after confirmation; never overwrites."""
    return _move_file(source, destination, confirm, roots())

if __name__ == "__main__":
    # stdio is the default. Never print startup banners to stdout.
    mcp.run()
