"""Tests for collecting Covers: tags from test files."""

import tempfile
import unittest
from pathlib import Path

from tracegate.parse import collect_tags


def write(folder: Path, name: str, text: str) -> Path:
    path = folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class CollectTagsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def ids(self):
        return [tag.req_id for tag in collect_tags([self.root])]

    def test_reads_tags_from_comments_and_docstrings(self):
        """Covers: REQ-TG-003"""
        write(self.root, "test_pump.py",
              'def test_start():\n    """Covers: REQ-AB-001"""\n\n'
              "def test_stop():\n    # Covers: REQ-AB-002\n    pass\n")
        self.assertEqual(self.ids(), ["REQ-AB-001", "REQ-AB-002"])

    def test_reads_several_ids_on_one_line(self):
        """Covers: REQ-TG-003"""
        write(self.root, "test_pump.py", "def test_cycle():\n    # Covers: REQ-AB-001, REQ-AB-002\n")
        self.assertEqual(self.ids(), ["REQ-AB-001", "REQ-AB-002"])

    def test_ignores_covers_in_the_middle_of_a_line(self):
        """Covers: REQ-TG-003"""
        write(self.root, "test_pump.py",
              'def test_note():\n    text = "Covers: REQ-AB-001"\n    # This also Covers: REQ-AB-002\n')
        self.assertEqual(self.ids(), [])

    def test_attributes_tag_to_enclosing_test_function(self):
        """Covers: REQ-TG-004"""
        write(self.root, "test_pump.py", "def test_start():\n    # Covers: REQ-AB-001\n")
        self.assertEqual(collect_tags([self.root])[0].test, "test_pump.py::test_start")

    def test_names_markdown_test_cases_by_heading(self):
        """Covers: REQ-TG-004"""
        write(self.root, "spec.md", "## TC-07 Pump stops at high pressure\n\nCovers: REQ-AB-002\n")
        self.assertEqual(collect_tags([self.root])[0].test, "spec.md::TC-07 Pump stops at high pressure")

    def test_falls_back_to_file_and_line(self):
        """Covers: REQ-TG-004"""
        write(self.root, "test_misc.c", "/* Covers: REQ-AB-003 */\n")
        tag = collect_tags([self.root])[0]
        self.assertEqual((tag.req_id, tag.test, tag.line), ("REQ-AB-003", "test_misc.c:1", 1))


if __name__ == "__main__":
    unittest.main()
