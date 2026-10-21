"""End-to-end tests for the command-line interface."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tracegate.cli import main


def write(folder: Path, name: str, text: str) -> Path:
    path = folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class CliTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, *extra):
        out, err = io.StringIO(), io.StringIO()
        argv = ["--reqs", str(self.root / "docs"), "--tests", str(self.root / "tests"), *extra]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_exit_zero_when_fully_traced(self):
        """Covers: REQ-TG-007"""
        write(self.root, "docs/reqs.md", "### REQ-AB-001: Start the pump\n")
        write(self.root, "tests/test_pump.py", "def test_start():\n    # Covers: REQ-AB-001\n")
        code, out, _ = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIn("PASS", out)

    def test_exit_one_when_a_requirement_is_uncovered(self):
        """Covers: REQ-TG-005, REQ-TG-007"""
        write(self.root, "docs/reqs.md", "### REQ-AB-001: Start the pump\n### REQ-AB-002: Stop the pump\n")
        write(self.root, "tests/test_pump.py", "def test_start():\n    # Covers: REQ-AB-001\n")
        code, out, _ = self.run_cli()
        self.assertEqual(code, 1)
        self.assertIn("REQ-AB-002", out)

    def test_exit_one_when_a_tag_dangles(self):
        """Covers: REQ-TG-006, REQ-TG-007"""
        write(self.root, "docs/reqs.md", "### REQ-AB-001: Start the pump\n")
        write(self.root, "tests/test_pump.py", "def test_start():\n    # Covers: REQ-AB-001, REQ-AB-404\n")
        code, out, _ = self.run_cli()
        self.assertEqual(code, 1)
        self.assertIn("dangling    REQ-AB-404", out)

    def test_exit_two_when_no_requirements_are_found(self):
        """Covers: REQ-TG-007"""
        write(self.root, "docs/notes.md", "# Nothing to trace here\n")
        code, _, err = self.run_cli()
        self.assertEqual(code, 2)
        self.assertIn("no requirements found", err)

    def test_markdown_format_prints_a_table(self):
        """Covers: REQ-TG-008"""
        write(self.root, "docs/reqs.md", "### REQ-AB-001: Start the pump\n")
        write(self.root, "tests/test_pump.py", "def test_start():\n    # Covers: REQ-AB-001\n")
        code, out, _ = self.run_cli("--format", "markdown")
        self.assertEqual(code, 0)
        self.assertIn("| Requirement | Title | Covered by | Status |", out)


if __name__ == "__main__":
    unittest.main()
