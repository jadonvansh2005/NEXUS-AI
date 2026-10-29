"""Local Development MCP server for Nexus-AI."""
import logging

from mcp.server import MCPServer
from mcp_servers.development import core

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nexus.development_mcp")

mcp = MCPServer("nexus-development")


@mcp.tool()
def git_status() -> dict:
    """Inspect the configured repository's working-tree status."""
    return core.git_status()


@mcp.tool()
def git_diff(staged: bool = False) -> dict:
    """Inspect unstaged changes, or staged changes when staged=True."""
    return core.git_diff(staged=staged)


@mcp.tool()
def git_log(limit: int = 10) -> dict:
    """Read recent Git commit summaries; limit must be between 1 and 50."""
    return core.git_log(limit=limit)


@mcp.tool()
def run_dev_command(command_id: str) -> dict:
    """Run an allowlisted development command by ID."""
    return core.run_dev_command(command_id)


if __name__ == "__main__":
    # Use stdio; do not print startup banners to stdout.
    mcp.run()
