"""Tests for comparing requirements against tags."""

import unittest

from tracegate.check import check
from tracegate.parse import CoverTag, Requirement


def req(req_id, title="Title"):
    return Requirement(req_id, title, "reqs.md", 1)


def tag(req_id, test="test_x.py::test_x"):
    return CoverTag(req_id, test, "test_x.py", 1)


class CheckTest(unittest.TestCase):
    def test_passes_when_every_requirement_is_covered(self):
        """Covers: REQ-TG-005"""
        result = check([req("REQ-AB-001"), req("REQ-AB-002")], [tag("REQ-AB-001"), tag("REQ-AB-002")])
        self.assertTrue(result.passed)
        self.assertEqual(result.coverage, 1.0)

    def test_reports_uncovered_requirement(self):
        """Covers: REQ-TG-005"""
        result = check([req("REQ-AB-001"), req("REQ-AB-002")], [tag("REQ-AB-001")])
        self.assertFalse(result.passed)
        self.assertEqual([r.req_id for r in result.uncovered], ["REQ-AB-002"])
        self.assertEqual(result.coverage, 0.5)

    def test_matrix_lists_every_test_per_requirement(self):
        """Covers: REQ-TG-005"""
        result = check([req("REQ-AB-001")], [tag("REQ-AB-001", "a.py::test_a"), tag("REQ-AB-001", "b.py::test_b")])
        self.assertEqual([t.test for t in result.matrix["REQ-AB-001"]], ["a.py::test_a", "b.py::test_b"])

    def test_reports_dangling_reference(self):
        """Covers: REQ-TG-006"""
        result = check([req("REQ-AB-001")], [tag("REQ-AB-001"), tag("REQ-AB-099")])
        self.assertFalse(result.passed)
        self.assertEqual([t.req_id for t in result.dangling], ["REQ-AB-099"])

    def test_duplicate_ids_fail_the_check(self):
        """Covers: REQ-TG-002"""
        result = check([req("REQ-AB-001"), req("REQ-AB-001")], [tag("REQ-AB-001")])
        self.assertFalse(result.passed)
        self.assertEqual(result.duplicates, ["REQ-AB-001"])
        self.assertEqual(result.total, 1)


if __name__ == "__main__":
    unittest.main()
