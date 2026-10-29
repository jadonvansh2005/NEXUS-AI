
import asyncio
import os
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters

BACKEND_ROOT = Path(__file__).resolve().parents[2]
SERVER_MODULE = "mcp_servers.development.server"

EXPECTED_TOOLS = {
    "git_status",
    "git_diff",
    "git_log",
    "run_dev_command",
}


async def main():
    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", SERVER_MODULE],
        cwd=str(BACKEND_ROOT),
        env={
            **os.environ,
            "NEXUS_DEV_REPO": str(BACKEND_ROOT.parent),
            "PYTHONPATH": str(BACKEND_ROOT),
        },
    )

    async with Client(server) as client:
        print("[PASS] MCP connection and initialization")

        # 1. Discover and verify all expected tools
        response = await client.list_tools()
        discovered = {tool.name for tool in response.tools}

        print("Discovered tools:", sorted(discovered))

        missing = EXPECTED_TOOLS - discovered
        if missing:
            raise AssertionError(
                f"Missing MCP tools: {sorted(missing)}"
            )

        print("[PASS] All four expected tools discovered")

        # 2. Test the Git tools
        calls = [
            ("git_status", {}),
            ("git_diff", {"staged": False}),
            ("git_log", {"limit": 3}),
        ]

        for name, arguments in calls:
            result = await client.call_tool(name, arguments)

            if result.is_error:
                raise AssertionError(
                    f"{name} returned an MCP tool error: "
                    f"{result.content!r}"
                )

            text_content = "\n".join(
                item.text
                for item in result.content
                if hasattr(item, "text")
            )

            if not text_content.strip():
                raise AssertionError(
                    f"{name} returned no text content"
                )

            print(f"\n[PASS] {name}")
            print(text_content[:1500])

        # 3. Test the allowlisted development command
        result = await client.call_tool(
            "run_dev_command",
            {"command_id": "python_unit_tests"},
        )

        if result.is_error:
            raise AssertionError(
                "run_dev_command returned an MCP tool error: "
                f"{result.content!r}"
            )

        output = "\n".join(
            item.text
            for item in result.content
            if hasattr(item, "text")
        )

        print("\nDevelopment command output:")
        print(output[:5000])

        # Verify the returned structured result
        if '"returncode": 0' not in output:
            raise AssertionError(
                "Development test command did not return "
                "a successful exit code."
            )

        if '"timed_out": false' not in output:
            raise AssertionError(
                "Development test command timed out or its "
                "timeout status was not successful."
            )

        if "Ran 20 tests" not in output or "OK" not in output:
            raise AssertionError(
                "Development unit tests did not pass as expected."
            )

        print("\n[PASS] run_dev_command")

        print("\nAll Development MCP smoke tests passed.")


if __name__ == "__main__":
    asyncio.run(main())
