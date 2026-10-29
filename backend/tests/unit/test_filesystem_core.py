import hashlib, tempfile, unittest
from pathlib import Path
from mcp_servers.filesystem.core import FilesystemError, list_directory, search_files, read_file, create_file, edit_file, move_file, resolve_allowed

class FilesystemCoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.roots = [self.root]
        (self.root / "sub").mkdir()
        (self.root / "hello.txt").write_text("hello", encoding="utf-8")
        (self.root / "sub" / "nested.py").write_text("print('ok')", encoding="utf-8")
    def tearDown(self): self.tmp.cleanup()
    def test_list(self):
        self.assertEqual({e["name"] for e in list_directory(str(self.root), self.roots)["entries"]}, {"hello.txt", "sub"})
    def test_search(self):
        self.assertEqual(Path(search_files(str(self.root), "*.py", 100, self.roots)["results"][0]["path"]).name, "nested.py")
    def test_read_and_hash(self):
        result = read_file(str(self.root / "hello.txt"), self.roots)
        self.assertEqual(result["content"], "hello")
        self.assertEqual(result["sha256"], hashlib.sha256(b"hello").hexdigest())
    def test_reject_outside_root(self):
        with self.assertRaises(FilesystemError): resolve_allowed(str(self.root.parent / "outside.txt"), self.roots, must_exist=False)
    def test_reject_parent_traversal(self):
        with self.assertRaises(FilesystemError): resolve_allowed(str(self.root / ".." / "outside.txt"), self.roots, must_exist=False)
    def test_create_requires_confirmation(self):
        with self.assertRaises(FilesystemError): create_file(str(self.root / "new.txt"), "x", False, self.roots)
    def test_create_no_overwrite(self):
        create_file(str(self.root / "new.txt"), "new", True, self.roots)
        with self.assertRaises(FilesystemError): create_file(str(self.root / "new.txt"), "overwrite", True, self.roots)
        self.assertEqual((self.root / "new.txt").read_text(), "new")
    def test_edit_requires_confirmation(self):
        digest = hashlib.sha256(b"hello").hexdigest()
        with self.assertRaises(FilesystemError): edit_file(str(self.root / "hello.txt"), "new", digest, False, self.roots)
    def test_edit_rejects_stale_hash(self):
        with self.assertRaises(FilesystemError): edit_file(str(self.root / "hello.txt"), "new", "0" * 64, True, self.roots)
        self.assertEqual((self.root / "hello.txt").read_text(), "hello")
    def test_edit_current_hash(self):
        digest = read_file(str(self.root / "hello.txt"), self.roots)["sha256"]
        edit_file(str(self.root / "hello.txt"), "updated", digest, True, self.roots)
        self.assertEqual((self.root / "hello.txt").read_text(), "updated")
    def test_move_requires_confirmation(self):
        with self.assertRaises(FilesystemError): move_file(str(self.root / "hello.txt"), str(self.root / "sub" / "moved.txt"), False, self.roots)
    def test_move_success(self):
        move_file(str(self.root / "hello.txt"), str(self.root / "sub" / "moved.txt"), True, self.roots)
        self.assertTrue((self.root / "sub" / "moved.txt").exists())
    def test_move_refuses_overwrite(self):
        with self.assertRaises(FilesystemError): move_file(str(self.root / "hello.txt"), str(self.root / "sub" / "nested.py"), True, self.roots)
    def test_no_directory_move(self):
        with self.assertRaises(FilesystemError): move_file(str(self.root / "sub"), str(self.root / "sub2"), True, self.roots)

if __name__ == "__main__": unittest.main()
