import json, os, unittest
from helpers import *  # noqa: F401,F403

EXPECTED = jread(os.path.join(FIXTURES, "expected.json"))["bad"]


class FixtureTests(unittest.TestCase):
    """The good page must stay clean and every bad page must keep failing for its reason.
    These guard against a rule change silently weakening the audit (false negatives) or
    flagging a clean page (false positives)."""

    def test_good_fixtures_have_no_findings(self):
        d = os.path.join(FIXTURES, "good")
        for f in sorted(os.listdir(d)):
            with self.subTest(f):
                code, out = audit(os.path.join(d, f), "--a11y", "--mobile")
                self.assertEqual(code, 0, out["errors"])
                self.assertEqual(out["errors"], [])
                self.assertEqual(out["warnings"], [], "good fixtures must be warning-free")

    def test_every_bad_fixture_is_listed(self):
        on_disk = set(os.listdir(os.path.join(FIXTURES, "bad")))
        self.assertEqual(on_disk, set(EXPECTED), "add new fixtures to tests/fixtures/expected.json")

    def test_bad_fixtures_report_expected_findings(self):
        for name, exp in EXPECTED.items():
            with self.subTest(name):
                flags = exp.get("flags", ["--a11y", "--mobile"])
                code, out = audit(os.path.join(FIXTURES, "bad", name), *flags)
                if exp.get("no_errors"):
                    self.assertEqual(code, 0)
                else:
                    self.assertEqual(code, 1)
                for needle in exp.get("errors", []):
                    self.assertTrue(any(needle in e for e in out["errors"]), f"missing error {needle!r} in {out['errors']}")
                for needle in exp.get("warnings", []):
                    self.assertTrue(any(needle in w for w in out["warnings"]), f"missing warning {needle!r} in {out['warnings']}")


class ContrastTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = load_module("audit")

    def test_black_on_white_is_21(self):
        self.assertAlmostEqual(self.a.contrast(self.a.rgb("000000"), self.a.rgb("ffffff")), 21.0, places=1)

    def test_same_color_is_1(self):
        self.assertAlmostEqual(self.a.contrast(self.a.rgb("777777"), self.a.rgb("777777")), 1.0, places=3)

    def test_is_symmetric(self):
        x, y = self.a.rgb("1f1a15"), self.a.rgb("f1eadd")
        self.assertAlmostEqual(self.a.contrast(x, y), self.a.contrast(y, x))

    def test_short_hex_expands(self):
        self.assertEqual(self.a.rgb("fff"), self.a.rgb("ffffff"))

    def test_alpha_blends_over_base(self):
        base = self.a.rgb("000000")
        c = self.a.to_rgb("rgba(255,255,255,.5)", over=base)
        self.assertAlmostEqual(c[0], 0.5, places=2)

    def test_known_aa_boundary(self):
        # #767676 on white is the classic smallest grey that passes AA (4.54:1)
        self.assertGreaterEqual(self.a.contrast(self.a.rgb("767676"), self.a.rgb("ffffff")), 4.5)
        self.assertLess(self.a.contrast(self.a.rgb("777777"), self.a.rgb("ffffff")), 4.6)


class HueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = load_module("audit")

    def test_violet_is_banned(self):
        h, s, _ = self.a.hls("6d28d9")
        self.assertTrue(self.a.HUE_LO <= h <= self.a.HUE_HI and s > self.a.HUE_SAT)

    def test_orange_is_allowed(self):
        h, _, _ = self.a.hls("b23a14")
        self.assertFalse(self.a.HUE_LO <= h <= self.a.HUE_HI)

    def test_grey_is_not_flagged_even_if_hue_is_in_range(self):
        _, s, _ = self.a.hls("808080")
        self.assertLessEqual(s, self.a.HUE_SAT)


class RuleThresholdTests(unittest.TestCase):
    def test_rules_json_has_required_sections(self):
        r = jread(os.path.join(ROOT, "core", "tokens", "rules.json"))
        for k in ("color", "contrast", "spacing_scale_px", "hero", "banned_words", "filler_text", "banned_symbols", "motion", "mobile"):
            self.assertIn(k, r)

    def test_banned_words_are_lowercase(self):
        r = jread(os.path.join(ROOT, "core", "tokens", "rules.json"))
        for w in r["banned_words"] + r["filler_text"]:
            self.assertEqual(w, w.lower(), "audit compares against lower-cased copy")


class ModeAndExplainTests(unittest.TestCase):
    def test_brand_first_demotes_hue_ban_but_not_contrast(self):
        code, out = audit(os.path.join(FIXTURES, "bad", "violet.html"), "--mode", "brand-first")
        self.assertEqual(code, 0)
        self.assertTrue(any("banned" in w for w in out["warnings"]))
        code, out = audit(os.path.join(FIXTURES, "bad", "low-contrast.html"), "--mode", "brand-first")
        self.assertEqual(code, 1)

    def test_balanced_allows_ten_word_headlines(self):
        code, out = audit(os.path.join(FIXTURES, "bad", "long-headline.html"), "--mode", "balanced")
        self.assertTrue(any("headline has 14 words" in w for w in out["warnings"]))

    def test_unknown_mode_is_rejected(self):
        from helpers import script
        r = script("audit.py", os.path.join(FIXTURES, "good", "landing.html"), "--mode", "nope")
        self.assertNotEqual(r.returncode, 0)

    def test_explain_adds_principle_and_fix(self):
        code, out = audit(os.path.join(FIXTURES, "bad", "gradient.html"), "--explain")
        self.assertTrue(out["explanations"])
        e = next(iter(out["explanations"].values()))
        self.assertIn("principle", e)
        self.assertIn("fix", e)

    def test_project_config_brand_color_is_exempt(self):
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(os.path.join(FIXTURES, "bad", "violet.html"), d)
            jwrite(os.path.join(d, "flawless.config.json"), {"brand_colors": ["#6d28d9"]})
            code, out = audit(os.path.join(d, "violet.html"))
            self.assertEqual(code, 0, out["errors"])

    def test_broken_config_is_reported(self):
        import tempfile, shutil
        from helpers import script
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(os.path.join(FIXTURES, "good", "landing.html"), d)
            jwrite_text(os.path.join(d, "flawless.config.json"), "{nope")
            r = script("audit.py", os.path.join(d, "landing.html"))
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("config error", r.stderr + r.stdout)


if __name__ == "__main__":
    unittest.main()
