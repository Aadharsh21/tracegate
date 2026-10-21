"""Tests for the reports."""

import unittest

from tracegate.check import check
from tracegate.parse import CoverTag, Requirement
from tracegate.report import format_text


def req(req_id, title="Title"):
    return Requirement(req_id, title, "reqs.md", 1)


def tag(req_id, test="test_x.py::test_x"):
    return CoverTag(req_id, test, "test_x.py", 1)


class TextReportTest(unittest.TestCase):
    def test_summary_shows_coverage_and_pass(self):
        """Covers: REQ-TG-007"""
        text = format_text(check([req("REQ-AB-001"), req("REQ-AB-002")], [tag("REQ-AB-001"), tag("REQ-AB-002")]))
        self.assertIn("2 requirements, 2 covered (100.0%)", text)
        self.assertIn("PASS", text)

    def test_summary_uses_singular_for_one_requirement(self):
        """Covers: REQ-TG-007"""
        text = format_text(check([req("REQ-AB-001")], [tag("REQ-AB-001")]))
        self.assertIn("tracegate: 1 requirement, 1 covered (100.0%)", text)

    def test_names_each_uncovered_requirement(self):
        """Covers: REQ-TG-005, REQ-TG-007"""
        text = format_text(check([req("REQ-AB-001"), req("REQ-AB-002", "Stop the pump")], [tag("REQ-AB-001")]))
        self.assertIn("REQ-AB-002  Stop the pump  MISSING", text)
        self.assertIn("FAIL: 1 uncovered requirement (REQ-AB-002)", text)

    def test_lists_dangling_tags_with_their_test(self):
        """Covers: REQ-TG-006"""
        text = format_text(check([req("REQ-AB-001")], [tag("REQ-AB-001"), tag("REQ-AB-099", "test_x.py::test_old")]))
        self.assertIn("dangling    REQ-AB-099 in test_x.py::test_old", text)
        self.assertIn("FAIL: 1 dangling tag", text)


if __name__ == "__main__":
    unittest.main()
