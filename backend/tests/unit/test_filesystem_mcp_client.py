
import asyncio
import os
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters


BACKEND_ROOT = Path(__file__).resolve().parents[2]
SERVER_MODULE = "mcp_servers.filesystem.server"
ALLOWED_ROOT = str(BACKEND_ROOT)


async def main() -> None:
    print(f"Backend: {BACKEND_ROOT}")
    print(f"Python:  {sys.executable}")
    print("\nLaunching Filesystem MCP Server through the MCP client...")

    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", SERVER_MODULE],
        cwd=str(BACKEND_ROOT),
        env={
            "NEXUS_MCP_ALLOWED_ROOTS": ALLOWED_ROOT,
            "PYTHONPATH": str(BACKEND_ROOT),
        },
    )

    async with Client(server) as client:
        print("\n[PASS] MCP connection and initialization successful")
        print(f"Protocol version: {client.protocol_version}")

        # 1. Discover the tools exposed by the server.
        response = await client.list_tools()
        tools = response.tools

        print(f"\nDiscovered {len(tools)} tool(s):")

        for tool in tools:
            print(f"\n- {tool.name}")
            print(f"  Description: {tool.description}")
            print(f"  Input schema: {tool.input_schema}")

        # 2. Find the expected read-only tool.
        list_tool = next(
            (tool for tool in tools if tool.name == "list_directory"),
            None,
        )

        if list_tool is None:
            raise RuntimeError(
                "Tool 'list_directory' was not discovered. "
                "Check the server's registered tool names."
            )

        # 3. Build arguments from the tool's advertised schema.
        properties = list_tool.input_schema.get("properties", {})
        path_parameter = next(
            (
                name
                for name in ("path", "directory_path", "directory")
                if name in properties
            ),
            None,
        )

        if path_parameter is None:
            raise RuntimeError(
                "Could not identify the directory argument from the "
                f"tool schema: {list_tool.input_schema}"
            )

        arguments = {path_parameter: ALLOWED_ROOT}

        print(f"\nCalling list_directory with: {arguments}")

        # 4. Invoke the tool through MCP.
        result = await client.call_tool("list_directory", arguments)

        if result.is_error:
            print("\n[FAIL] The MCP tool returned an error.")
        else:
            print("\n[PASS] MCP tool invocation completed.")

        print("\nTool response:")
        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)
            else:
                print(item)

        if result.is_error:
            raise RuntimeError("list_directory returned an MCP tool error.")

    print("\n[PASS] MCP client disconnected cleanly.")


if __name__ == "__main__":
    asyncio.run(main())
