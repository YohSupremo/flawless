import json, os, tempfile, unittest, threading
from helpers import *  # noqa: F401,F403

state = load_module("state")


class StateTests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.d.name, "s.json")
        self.env = {"FLAWLESS_STATE": self.path}

    def tearDown(self):
        self.d.cleanup()

    def test_init_writes_versioned_state(self):
        self.assertEqual(script("state.py", "init", env=self.env).returncode, 0)
        st = jread(self.path)
        self.assertEqual(st["version"], state.STATE_VERSION)
        self.assertEqual(st["scheme"], {})

    def test_set_and_show_round_trip(self):
        script("state.py", "set", "accent", "#b23a14", env=self.env)
        r = script("state.py", "show", env=self.env)
        self.assertEqual(json.loads(r.stdout)["scheme"]["accent"], "#b23a14")

    def test_unknown_scheme_key_is_rejected(self):
        self.assertNotEqual(script("state.py", "set", "nonsense", "x", env=self.env).returncode, 0)

    def test_corrupt_file_is_moved_aside_and_state_recovers(self):
        jwrite_text(self.path, "{this is not json")
        r = script("state.py", "show", env=self.env)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["pages"], {})
        self.assertTrue(os.path.exists(self.path + ".corrupt"))
        self.assertIn("unreadable", r.stderr)

    def test_unversioned_file_is_migrated(self):
        jwrite(self.path, {"active": True, "scheme": {"base": "#fff"}, "pages": {}})
        st = state.load(self.path)
        self.assertEqual(st["version"], 1)
        self.assertTrue(st["active"])

    def test_newer_version_is_not_silently_loaded(self):
        jwrite(self.path, {"version": 99})
        st = state.load(self.path)  # treated as unreadable, moved aside
        self.assertEqual(st["version"], 1)
        self.assertTrue(os.path.exists(self.path + ".corrupt"))

    def test_save_is_atomic_no_temp_files_left(self):
        script("state.py", "init", env=self.env)
        left = [f for f in os.listdir(self.d.name) if f.endswith(".tmp") or f.endswith(".lock")]
        self.assertEqual(left, [])

    def test_stale_lock_does_not_block(self):
        script("state.py", "init", env=self.env)
        lock = self.path + ".lock"
        jwrite_text(lock, "")
        os.utime(lock, (1, 1))
        self.assertEqual(script("state.py", "set", "base", "#000", env=self.env).returncode, 0)

    def test_concurrent_writers_do_not_lose_updates(self):
        keys = ["base", "surface", "text", "accent", "radius"]
        threads = [threading.Thread(target=script, args=("state.py", "set", k, "v" + k), kwargs={"env": self.env}) for k in keys]
        [t.start() for t in threads]; [t.join() for t in threads]
        sc = jread(self.path)["scheme"]
        for k in keys:
            self.assertEqual(sc.get(k), "v" + k)

    def test_legacy_env_var_still_works(self):
        legacy = os.path.join(self.d.name, "legacy.json")
        script("state.py", "init", env={"CLEAN_UI_STATE": legacy})
        self.assertTrue(os.path.exists(legacy))

    def test_project_root_scopes_state_and_relative_pages(self):
        env = {"FLAWLESS_PROJECT_ROOT": self.d.name}
        r = script("state.py", "path", env=env)
        self.assertEqual(r.stdout.strip(), os.path.join(os.path.abspath(self.d.name), ".flawless-state.json"))
        page = os.path.join(self.d.name, "site", "index.html")
        script("state.py", "page", page, "audit=clean", env=env)
        st = jread(os.path.join(self.d.name, ".flawless-state.json"))
        self.assertIn(os.path.join("site", "index.html"), st["pages"])

    def test_explicit_state_overrides_project_root(self):
        env = {"FLAWLESS_PROJECT_ROOT": self.d.name, "FLAWLESS_STATE": self.path}
        self.assertEqual(script("state.py", "path", env=env).stdout.strip(), os.path.abspath(self.path))


if __name__ == "__main__":
    unittest.main()
