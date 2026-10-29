from __future__ import annotations

import os
import sys
from contextlib import AsyncExitStack
from pathlib import Path

from mcp import Client, StdioServerParameters


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent


class CombinedMCPClient:
    """Manage and route calls to the Filesystem and Development MCP servers."""

    def __init__(self) -> None:
        self._stack = AsyncExitStack()
        self._clients = {}

    async def __aenter__(self):
        filesystem_server = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_servers.filesystem.server"],
            cwd=str(BACKEND_ROOT),
            env={
                **os.environ,
                "NEXUS_MCP_ALLOWED_ROOTS": os.pathsep.join([
                    r"C:\\",
                    r"D:\\",
                    r"F:\\",
                ]),
                "PYTHONPATH": str(BACKEND_ROOT),
            },
        )

        development_server = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_servers.development.server"],
            cwd=str(BACKEND_ROOT),
            env={
                **os.environ,
                "NEXUS_DEV_REPO": str(REPO_ROOT),
                "PYTHONPATH": str(BACKEND_ROOT),
            },
        )

        try:
            self._clients["filesystem"] = await self._stack.enter_async_context(
                Client(filesystem_server)
            )
            self._clients["development"] = await self._stack.enter_async_context(
                Client(development_server)
            )
        except BaseException:
            await self._stack.aclose()
            raise

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return await self._stack.__aexit__(exc_type, exc_value, traceback)

    async def list_tools(self) -> list[dict]:
        """Return all tools with server-prefixed names."""
        tools = []

        for server_name, client in self._clients.items():
            response = await client.list_tools()

            for tool in response.tools:
                tools.append({
                    "name": f"{server_name}.{tool.name}",
                    "server": server_name,
                    "description": tool.description,
                    "input_schema": tool.input_schema,
                })

        return tools

    async def call_tool(self, name: str, arguments: dict):
        """Route a namespaced tool call to its owning MCP server."""
        if not isinstance(name, str) or name.count(".") != 1:
            raise ValueError(
                "Tool name must use 'filesystem.tool_name' "
                "or 'development.tool_name'."
            )

        server_name, tool_name = name.split(".", 1)

        if server_name not in self._clients:
            raise ValueError(f"Unknown MCP server: {server_name}")

        available = {
            tool["name"] for tool in await self.list_tools()
        }

        if name not in available:
            raise ValueError(f"Unknown MCP tool: {name}")

        return await self._clients[server_name].call_tool(
            tool_name, arguments
        )
