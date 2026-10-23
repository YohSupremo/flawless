"""Manifest validation: structure, dependencies, cycles, and generated files. Mutations run on a temp copy."""
import json, os, shutil, subprocess, sys, tempfile, unittest
from helpers import *  # noqa: F401,F403


class ManifestTests(unittest.TestCase):
    def copy(self):
        d = tempfile.mkdtemp()
        dst = os.path.join(d, "skill")
        shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "tests", "__pycache__"))
        self.addCleanup(shutil.rmtree, d, True)
        return dst

    def validate(self, root):
        return subprocess.run([sys.executable, os.path.join(root, "core", "scripts", "validate.py")], capture_output=True, text=True)

    def mutate(self, root, fn):
        p = os.path.join(root, "manifest.json")
        m = jread(p)
        fn(m)
        jwrite(p, m)

    def test_repository_validates(self):
        r = self.validate(ROOT)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_call_cycle_is_detected(self):
        root = self.copy()
        def cyc(m):
            m["commands"]["new"]["calls"].append("edit")
            m["commands"]["edit"]["calls"].append("new")
        self.mutate(root, cyc)
        r = self.validate(root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("call cycle", r.stdout)

    def test_unknown_dependency_is_detected(self):
        root = self.copy()
        self.mutate(root, lambda m: m["commands"]["new"]["calls"].append("ghost"))
        r = self.validate(root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("unknown command 'ghost'", r.stdout)

    def test_missing_read_file_is_detected(self):
        root = self.copy()
        self.mutate(root, lambda m: m["commands"]["new"]["reads"].append("core/nope.md"))
        self.assertIn("missing file core/nope.md", self.validate(root).stdout)

    def test_modifying_command_without_snapshot_hook_is_detected(self):
        root = self.copy()
        self.mutate(root, lambda m: m["commands"]["edit"].update(pre_hooks=[]))
        self.assertIn("missing snapshot or audit hook", self.validate(root).stdout)

    def test_readonly_command_with_snapshot_hook_is_detected(self):
        root = self.copy()
        self.mutate(root, lambda m: m["commands"]["audit"].update(pre_hooks=["snapshot"]))
        self.assertIn("read-only command has a snapshot hook", self.validate(root).stdout)

    def test_only_allowed_commands_write_the_scheme(self):
        root = self.copy()
        self.mutate(root, lambda m: m["commands"]["copy"].update(state_writes=["scheme"]))
        self.assertIn("not an allowed writer", self.validate(root).stdout)

    def test_stale_generated_file_is_detected(self):
        root = self.copy()
        with open(os.path.join(root, "core", "graph.md"), "a") as f:
            f.write("\nstale\n")
        self.assertIn("stale generated content: core/graph.md", self.validate(root).stdout)

    def test_build_is_idempotent(self):
        root = self.copy()
        for _ in range(2):
            subprocess.run([sys.executable, os.path.join(root, "core", "scripts", "build.py")], check=True, capture_output=True)
        self.assertEqual(self.validate(root).returncode, 0)

    def test_every_command_has_help_metadata(self):
        m = jread(os.path.join(ROOT, "manifest.json"))
        for n, c in m["commands"].items():
            for k in ("needs_target", "confirms", "output", "common_failures", "related"):
                self.assertIn(k, c, f"{n} missing {k}")


if __name__ == "__main__":
    unittest.main()
