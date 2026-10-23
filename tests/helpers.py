"""Shared helpers for the test suite."""
import importlib.util, json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(ROOT, "core", "scripts")
FIXTURES = os.path.join(ROOT, "tests", "fixtures")


def script(name, *args, env=None, cwd=None):
    e = dict(os.environ)
    e.update(env or {})
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, name), *args],
                          capture_output=True, text=True, env=e, cwd=cwd)


def audit(path, *flags, env=None):
    """Run audit.py --json. Returns (exit_code, parsed json)."""
    r = script("audit.py", path, "--json", *flags, env=env)
    return r.returncode, json.loads(r.stdout)


def load_module(name):
    """Import a script as a module without running its main()."""
    spec = importlib.util.spec_from_file_location("flawless_" + name, os.path.join(SCRIPTS, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def jread(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def jwrite(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def jwrite_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def jread_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()
