"""Tests for the JSON report."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tracegate.check import check
from tracegate.cli import main
from tracegate.parse import CoverTag, Requirement
from tracegate.report import format_json


def req(req_id, title="Title"):
    return Requirement(req_id, title, "reqs.md", 1)


def tag(req_id, test="test_x.py::test_x"):
    return CoverTag(req_id, test, "test_x.py", 1)


class JsonReportTest(unittest.TestCase):
    def test_report_has_coverage_numbers(self):
        """Covers: REQ-TG-008"""
        data = json.loads(format_json(check([req("REQ-AB-001"), req("REQ-AB-002")], [tag("REQ-AB-001")])))
        self.assertEqual((data["requirements"], data["covered"], data["coverage"]), (2, 1, 0.5))
        self.assertEqual(data["uncovered"], ["REQ-AB-002"])
        self.assertFalse(data["passed"])

    def test_matrix_maps_ids_to_test_names(self):
        """Covers: REQ-TG-008"""
        data = json.loads(format_json(check([req("REQ-AB-001")], [tag("REQ-AB-001", "test_pump.py::test_start")])))
        self.assertEqual(data["matrix"], {"REQ-AB-001": ["test_pump.py::test_start"]})

    def test_cli_prints_valid_json(self):
        """Covers: REQ-TG-008"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "tests").mkdir()
            (root / "docs" / "reqs.md").write_text("### REQ-AB-001: Start the pump\n", encoding="utf-8")
            (root / "tests" / "test_pump.py").write_text("def test_start():\n    # Covers: REQ-AB-001\n", encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main(["--reqs", str(root / "docs"), "--tests", str(root / "tests"), "--format", "json"])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out.getvalue())["passed"])


if __name__ == "__main__":
    unittest.main()
