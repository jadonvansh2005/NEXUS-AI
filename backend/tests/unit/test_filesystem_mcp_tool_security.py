
import os
import sys
import tempfile
import unittest
from pathlib import Path

from mcp import Client, StdioServerParameters


BACKEND_ROOT = Path(__file__).resolve().parents[2]
SERVER_MODULE = "mcp_servers.filesystem.server"


class FilesystemMCPToolSecurityTests(unittest.IsolatedAsyncioTestCase):
    async def run_security_case(self, case):
        with tempfile.TemporaryDirectory() as allowed_dir, \
             tempfile.TemporaryDirectory() as outside_dir:

            allowed = Path(allowed_dir).resolve()
            outside = Path(outside_dir).resolve()

            secret_marker = "NEXUS_MCP_SECRET_TEST_MARKER_91A7"
            secret_file = outside / "secret.txt"
            secret_file.write_text(secret_marker, encoding="utf-8")

            target = outside / "should_not_be_created.txt"

            server = StdioServerParameters(
                command=sys.executable,
                args=["-m", SERVER_MODULE],
                cwd=str(BACKEND_ROOT),
                env={
                    **os.environ,
                    "NEXUS_MCP_ALLOWED_ROOTS": str(allowed),
                    "PYTHONPATH": str(BACKEND_ROOT),
                },
            )

            async with Client(server) as client:
                if case == "list_outside":
                    name = "list_directory"
                    arguments = {"path": str(outside)}

                elif case == "read_outside":
                    name = "read_file"
                    arguments = {"path": str(secret_file)}

                elif case == "search_outside":
                    name = "search_files"
                    arguments = {
                        "root": str(outside),
                        "pattern": "*.txt",
                        "max_results": 20,
                    }

                elif case == "create_outside":
                    name = "create_file"
                    arguments = {
                        "path": str(target),
                        "content": "must not be written",
                        "confirm": True,
                    }

                elif case == "empty_path":
                    name = "list_directory"
                    arguments = {"path": ""}

                else:
                    self.fail(f"Unknown test case: {case}")

                try:
                    result = await client.call_tool(name, arguments)
                except Exception as exc:
                    # An exception is acceptable only if it does not
                    # disclose the protected file's content.
                    self.assertNotIn(secret_marker, str(exc))
                else:
                    returned_text = repr(result.content)
                    self.assertNotIn(secret_marker, returned_text)
                    self.assertTrue(
                        result.is_error,
                        f"{name} unexpectedly succeeded for {case}",
                    )

            if case == "create_outside":
                self.assertFalse(
                    target.exists(),
                    "The MCP tool created a file outside the allowed root.",
                )

    async def test_list_directory_rejects_outside_root(self):
        await self.run_security_case("list_outside")

    async def test_read_file_does_not_disclose_outside_secret(self):
        await self.run_security_case("read_outside")

    async def test_search_files_rejects_outside_root(self):
        await self.run_security_case("search_outside")

    async def test_create_file_rejects_outside_root(self):
        await self.run_security_case("create_outside")

    async def test_list_directory_rejects_empty_path(self):
        await self.run_security_case("empty_path")


if __name__ == "__main__":
    unittest.main(verbosity=2)
