"""Tests for reading requirement headings."""

import tempfile
import unittest
from pathlib import Path

from tracegate.parse import find_duplicates, parse_requirements


def write(folder: Path, name: str, text: str) -> Path:
    path = folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class ParseRequirementsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_reads_heading_ids_titles_and_lines(self):
        """Covers: REQ-TG-001"""
        write(self.root, "reqs.md", "# Spec\n\n### REQ-AB-001: Start the pump\n\ntext\n\n## REQ-AB-002 Stop the pump\n")
        reqs = parse_requirements([self.root])
        self.assertEqual(
            [(r.req_id, r.title, r.line) for r in reqs],
            [("REQ-AB-001", "Start the pump", 3), ("REQ-AB-002", "Stop the pump", 7)],
        )

    def test_ignores_ids_outside_headings(self):
        """Covers: REQ-TG-001"""
        write(self.root, "reqs.md", "See REQ-AB-001 for details.\n### Overview of REQ-AB-002\n")
        self.assertEqual(parse_requirements([self.root]), [])

    def test_reads_every_markdown_file_in_a_folder(self):
        """Covers: REQ-TG-001"""
        write(self.root, "a.md", "### REQ-AB-001: One\n")
        write(self.root, "sub/b.md", "### REQ-AB-002: Two\n")
        write(self.root, "notes.txt", "### REQ-AB-003: Not Markdown\n")
        ids = [r.req_id for r in parse_requirements([self.root])]
        self.assertEqual(ids, ["REQ-AB-001", "REQ-AB-002"])

    def test_strips_closing_hashes_from_titles(self):
        """Covers: REQ-TG-001"""
        write(self.root, "reqs.md", "### REQ-AB-001: Start the pump ###\n")
        self.assertEqual(parse_requirements([self.root])[0].title, "Start the pump")

    def test_accepts_a_custom_id_pattern(self):
        """Covers: REQ-TG-001"""
        write(self.root, "reqs.md", "## SRS-12: Custom scheme\n")
        reqs = parse_requirements([self.root], id_pattern=r"SRS-\d+")
        self.assertEqual(reqs[0].req_id, "SRS-12")

    def test_finds_duplicate_ids(self):
        """Covers: REQ-TG-002"""
        write(self.root, "reqs.md", "### REQ-AB-001: One\n### REQ-AB-002: Two\n### REQ-AB-001: Again\n")
        self.assertEqual(find_duplicates(parse_requirements([self.root])), ["REQ-AB-001"])


if __name__ == "__main__":
    unittest.main()
