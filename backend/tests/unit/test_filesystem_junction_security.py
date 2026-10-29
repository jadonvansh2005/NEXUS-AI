
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from mcp_servers.filesystem import core


class FilesystemJunctionSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.base = Path(self.temp.name).resolve()
        self.allowed = self.base / "allowed"
        self.outside = self.base / "outside"
        self.allowed.mkdir()
        self.outside.mkdir()

        self.roots = [self.allowed]

        self.secret = self.outside / "secret.txt"
        self.secret.write_text("outside secret", encoding="utf-8")

    def test_junction_to_outside_directory_is_not_searched(self):
        junction = self.allowed / "outside_link"

        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(junction), str(self.outside)],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0 or not junction.exists():
            self.skipTest(
                f"Could not create junction: {result.stdout} {result.stderr}"
            )

        search_result = core.search_files(
            str(self.allowed),
            pattern="*.txt",
            roots=self.roots,
        )

        found_paths = [item["path"] for item in search_result["results"]]

        self.assertNotIn(str(self.secret), found_paths)
        self.assertFalse(any("outside_link" in path for path in found_paths))

    def test_junction_target_cannot_be_read_directly(self):
        junction = self.allowed / "outside_link"

        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(junction), str(self.outside)],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0 or not junction.exists():
            self.skipTest(
                f"Could not create junction: {result.stdout} {result.stderr}"
            )

        with self.assertRaises(core.FilesystemError):
            core.read_file(str(junction / "secret.txt"), self.roots)


if __name__ == "__main__":
    unittest.main(verbosity=2)
