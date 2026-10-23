import os, tempfile, unittest
from helpers import *  # noqa: F401,F403


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.page = os.path.join(self.d.name, "page.html")
        self.write("one")

    def tearDown(self):
        self.d.cleanup()

    def write(self, text):
        jwrite_text(self.page, text)

    def read(self):
        return jread_text(self.page)

    def test_save_creates_numbered_versions(self):
        self.assertIn("saved v1", script("snapshot.py", "save", self.page).stdout)
        self.write("two")
        self.assertIn("saved v2", script("snapshot.py", "save", self.page).stdout)
        self.assertIn("v1, v2", script("snapshot.py", "list", self.page).stdout)

    def test_restore_brings_back_old_content(self):
        script("snapshot.py", "save", self.page)
        self.write("two")
        self.assertIn("restored v1", script("snapshot.py", "restore", self.page, "1").stdout)
        self.assertEqual(self.read(), "one")

    def test_restore_is_itself_undoable(self):
        script("snapshot.py", "save", self.page)   # v1 = one
        self.write("two")
        script("snapshot.py", "restore", self.page, "1")  # saves "two" as v2, page = one
        script("snapshot.py", "restore", self.page, "2")
        self.assertEqual(self.read(), "two")

    def test_restore_defaults_to_latest(self):
        script("snapshot.py", "save", self.page)
        self.write("two")
        script("snapshot.py", "save", self.page)
        self.write("three")
        script("snapshot.py", "restore", self.page)
        self.assertEqual(self.read(), "two")

    def test_restore_unknown_version_fails_and_keeps_page(self):
        script("snapshot.py", "save", self.page)
        self.write("two")
        self.assertNotEqual(script("snapshot.py", "restore", self.page, "9").returncode, 0)
        self.assertEqual(self.read(), "two")

    def test_restore_with_no_history_fails(self):
        self.assertNotEqual(script("snapshot.py", "restore", self.page).returncode, 0)

    def test_missing_page_fails_cleanly(self):
        r = script("snapshot.py", "save", os.path.join(self.d.name, "nope.html"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("page not found", r.stderr)


if __name__ == "__main__":
    unittest.main()
