import tempfile
import unittest
from pathlib import Path
from mdlinks import check


class LinkTests(unittest.TestCase):
    def test_paths_fragments_external_and_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a b.txt").write_text("ok")
            (root / "README.md").write_text(
                "[ok](a%20b.txt#part)\n[bad](missing.txt)\n"
                "[web](https://example.com) [anchor](#here)\n"
                "```md\n[ignored](absent)\n```\n`[code](nope)`\n", encoding="utf-8")
            result = check(root)
            self.assertEqual(result["checked_links"], 2)
            self.assertEqual(result["broken_links"], [{"file": "README.md", "line": 2, "target": "missing.txt"}])

    def test_nested_and_root_relative(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "README.md").write_text("hello")
            (root / "docs" / "guide.md").write_text("[a](../README.md) [b](/README.md)")
            self.assertEqual(check(root)["broken_links"], [])


if __name__ == "__main__":
    unittest.main()
