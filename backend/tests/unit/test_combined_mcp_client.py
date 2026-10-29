import asyncio

from integration.mcp_client import CombinedMCPClient


EXPECTED_TOOLS = {
    "filesystem.list_directory",
    "filesystem.search_files",
    "filesystem.read_file",
    "filesystem.create_file",
    "filesystem.edit_file",
    "filesystem.move_file",
    "development.git_status",
    "development.git_diff",
    "development.git_log",
    "development.run_dev_command",
}


async def main():
    async with CombinedMCPClient() as client:
        print("[PASS] Both MCP servers connected")

        tools = await client.list_tools()
        discovered = {tool["name"] for tool in tools}

        print(f"Discovered {len(discovered)} tools:")
        for name in sorted(discovered):
            print(f"  - {name}")

        assert discovered == EXPECTED_TOOLS, (
            f"Missing: {EXPECTED_TOOLS - discovered}; "
            f"unexpected: {discovered - EXPECTED_TOOLS}"
        )

        filesystem_result = await client.call_tool(
            "filesystem.list_directory",
            {"path": str(client.__class__.__module__ and
                          __import__('pathlib').Path(__file__).resolve().parents[2])},
        )
        assert not filesystem_result.is_error, filesystem_result.content
        print("[PASS] filesystem.list_directory")

        development_result = await client.call_tool(
            "development.git_status", {}
        )
        assert not development_result.is_error, development_result.content
        print("[PASS] development.git_status")

        print("[PASS] Combined MCP client smoke test")


if __name__ == "__main__":
    asyncio.run(main())
