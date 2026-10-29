
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mcp_servers.filesystem import core


class FilesystemSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name).resolve()
        self.outside_temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.outside_temp.cleanup)
        self.outside = Path(self.outside_temp.name).resolve()

        self.roots = [self.root]

    def test_reject_parent_traversal(self):
        outside_file = self.outside / "secret.txt"
        outside_file.write_text("secret", encoding="utf-8")

        with self.assertRaises(core.FilesystemError):
            core.read_file(str(self.root / ".." / self.outside.name / "secret.txt"),
                           self.roots)

    def test_reject_absolute_path_outside_root(self):
        outside_file = self.outside / "secret.txt"
        outside_file.write_text("secret", encoding="utf-8")

        with self.assertRaises(core.FilesystemError):
            core.read_file(str(outside_file), self.roots)

    def test_reject_symlink_to_outside_file(self):
        outside_file = self.outside / "secret.txt"
        outside_file.write_text("secret", encoding="utf-8")
        link = self.root / "linked_secret.txt"

        try:
            link.symlink_to(outside_file)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlink creation unavailable: {exc}")

        with self.assertRaises(core.FilesystemError):
            core.read_file(str(link), self.roots)

    def test_reject_symlink_directory_escape_in_search(self):
        outside_file = self.outside / "secret.txt"
        outside_file.write_text("secret", encoding="utf-8")
        link = self.root / "linked_directory"

        try:
            link.symlink_to(self.outside, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlink creation unavailable: {exc}")

        result = core.search_files(
            str(self.root), pattern="*.txt", roots=self.roots
        )
        self.assertNotIn(
            str(outside_file),
            [item["path"] for item in result["results"]],
        )

    def test_read_rejects_file_over_size_limit(self):
        path = self.root / "large.txt"
        path.write_bytes(b"x" * (core.MAX_READ_BYTES + 1))

        with self.assertRaises(core.FilesystemError):
            core.read_file(str(path), self.roots)

    def test_create_rejects_content_over_size_limit(self):
        path = self.root / "too_large.txt"
        content = "x" * (core.MAX_WRITE_BYTES + 1)

        with self.assertRaises(core.FilesystemError):
            core.create_file(str(path), content, True, self.roots)

        self.assertFalse(path.exists())

    def test_edit_rejects_content_over_size_limit(self):
        path = self.root / "existing.txt"
        path.write_text("original", encoding="utf-8")
        original = path.read_bytes()
        digest = hashlib.sha256(original).hexdigest()

        with self.assertRaises(core.FilesystemError):
            core.edit_file(
                str(path),
                "x" * (core.MAX_WRITE_BYTES + 1),
                digest,
                True,
                self.roots,
            )

        self.assertEqual(path.read_bytes(), original)

    def test_create_rejects_missing_confirmation(self):
        path = self.root / "new.txt"

        with self.assertRaises(core.FilesystemError):
            core.create_file(str(path), "hello", False, self.roots)

        self.assertFalse(path.exists())

    def test_edit_rejects_missing_confirmation(self):
        path = self.root / "existing.txt"
        path.write_text("original", encoding="utf-8")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()

        with self.assertRaises(core.FilesystemError):
            core.edit_file(str(path), "changed", digest, False, self.roots)

        self.assertEqual(path.read_text(encoding="utf-8"), "original")

    def test_move_rejects_missing_confirmation(self):
        source = self.root / "source.txt"
        destination = self.root / "destination.txt"
        source.write_text("data", encoding="utf-8")

        with self.assertRaises(core.FilesystemError):
            core.move_file(
                str(source), str(destination), False, self.roots
            )

        self.assertTrue(source.exists())
        self.assertFalse(destination.exists())

    def test_create_never_overwrites(self):
        path = self.root / "existing.txt"
        path.write_text("original", encoding="utf-8")

        with self.assertRaises(core.FilesystemError):
            core.create_file(str(path), "replacement", True, self.roots)

        self.assertEqual(path.read_text(encoding="utf-8"), "original")

    def test_edit_rejects_stale_hash(self):
        path = self.root / "existing.txt"
        path.write_text("original", encoding="utf-8")
        stale_hash = hashlib.sha256(b"older content").hexdigest()

        with self.assertRaises(core.FilesystemError):
            core.edit_file(
                str(path), "replacement", stale_hash, True, self.roots
            )

        self.assertEqual(path.read_text(encoding="utf-8"), "original")

    def test_move_never_overwrites_destination(self):
        source = self.root / "source.txt"
        destination = self.root / "destination.txt"
        source.write_text("source data", encoding="utf-8")
        destination.write_text("destination data", encoding="utf-8")

        with self.assertRaises(core.FilesystemError):
            core.move_file(
                str(source), str(destination), True, self.roots
            )

        self.assertEqual(source.read_text(encoding="utf-8"), "source data")
        self.assertEqual(
            destination.read_text(encoding="utf-8"), "destination data"
        )

    def test_invalid_paths_are_rejected(self):
        for invalid_path in ("", "   ", None):
            with self.subTest(path=invalid_path):
                with self.assertRaises(core.FilesystemError):
                    core.resolve_allowed(invalid_path, self.roots)

    def test_search_rejects_invalid_result_limits(self):
        for limit in (0, -1, core.MAX_SEARCH_RESULTS + 1):
            with self.subTest(limit=limit):
                with self.assertRaises(core.FilesystemError):
                    core.search_files(
                        str(self.root),
                        max_results=limit,
                        roots=self.roots,
                    )

    def test_search_rejects_empty_pattern(self):
        with self.assertRaises(core.FilesystemError):
            core.search_files(
                str(self.root), pattern="", roots=self.roots
            )

    def test_read_rejects_non_utf8_file(self):
        path = self.root / "binary.txt"
        path.write_bytes(b"\xff\xfe\xfa")

        with self.assertRaises(core.FilesystemError):
            core.read_file(str(path), self.roots)
            
    
    def test_edit_rejects_concurrent_exclusive_access(self):
        import ctypes

        path = self.root / "existing.txt"
        path.write_text("original", encoding="utf-8")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()

        GENERIC_READ = 0x80000000
        GENERIC_WRITE = 0x40000000
        OPEN_EXISTING = 3
        FILE_ATTRIBUTE_NORMAL = 0x80
        INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateFileW.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_void_p,
        ]
        kernel32.CreateFileW.restype = ctypes.c_void_p

        handle = kernel32.CreateFileW(
            str(path),
            GENERIC_READ | GENERIC_WRITE,
            0,
            None,
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            None,
        )

        self.assertNotEqual(handle, INVALID_HANDLE_VALUE)

        try:
            with self.assertRaises(core.FilesystemError):
                core.edit_file(
                    str(path), "assistant edit", digest, True, self.roots
                )
        finally:
            kernel32.CloseHandle(handle)

        self.assertEqual(
            path.read_text(encoding="utf-8"),
            "original",
        )
        
    # def test_edit_preserves_original_when_replace_fails(self):
    #     path = self.root / "existing.txt"
    #     original = b"original content"
    #     path.write_bytes(original)
    #     digest = hashlib.sha256(original).hexdigest()

    #     import ctypes

    #     class FakeKernel32:
    #         def __init__(self):
    #             self.ReplaceFileW = lambda *args: 0

    #         def CreateFileW(self, *args):
    #             return real_create_file(*args)

    #     real_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    #     real_create_file = real_kernel32.CreateFileW
    #     real_create_file.argtypes = [
    #         ctypes.c_wchar_p,
    #         ctypes.c_uint32,
    #         ctypes.c_uint32,
    #         ctypes.c_void_p,
    #         ctypes.c_uint32,
    #         ctypes.c_uint32,
    #         ctypes.c_void_p,
    #     ]
    #     real_create_file.restype = ctypes.c_void_p

    #     fake_kernel32 = FakeKernel32()

    #     with patch.object(core.ctypes, "WinDLL", return_value=fake_kernel32):
    #         with self.assertRaises(core.FilesystemError):
    #             core.edit_file(
    #                 str(path),
    #                 "replacement content",
    #                 digest,
    #                 True,
    #                 self.roots,
    #             )

    #     self.assertEqual(path.read_bytes(), original)
    #     self.assertEqual(
    #         list(self.root.glob(".existing.txt.*.tmp")),
    #         [],
    #         "Temporary replacement file should be cleaned up.",
    #     )
    
    def test_move_rejects_destination_directory_created_during_move(self):
        source = self.root / "source.txt"
        destination = self.root / "destination.txt"
        source.write_text("source data", encoding="utf-8")

        original_rename = core.os.rename

        def create_destination_then_rename(src, dst):
            # Simulate a competing process creating the destination
            # after move_file has checked whether it exists.
            Path(dst).mkdir()
            return original_rename(src, dst)

        with patch.object(
            core.os,
            "rename",
            side_effect=create_destination_then_rename,
        ):
            with self.assertRaises(core.FilesystemError):
                core.move_file(
                    str(source),
                    str(destination),
                    True,
                    self.roots,
                )

        self.assertTrue(source.is_file())
        self.assertEqual(source.read_text(encoding="utf-8"), "source data")
        self.assertTrue(destination.is_dir())
        self.assertFalse((destination / source.name).exists())





if __name__ == "__main__":
    unittest.main(verbosity=2)
