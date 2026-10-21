"""Command-line entry point: python -m tracegate."""

from __future__ import annotations

import argparse
import sys

from . import __version__, report
from .check import check
from .parse import DEFAULT_ID_PATTERN, collect_tags, parse_requirements


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracegate",
        description="Fail the build when a requirement has no test.",
    )
    parser.add_argument("--reqs", nargs="+", default=["docs"], metavar="PATH",
                        help="requirement files or folders (default: docs)")
    parser.add_argument("--tests", nargs="+", default=["tests"], metavar="PATH",
                        help="test files or folders (default: tests)")
    parser.add_argument("--id-pattern", default=DEFAULT_ID_PATTERN, metavar="REGEX",
                        help="regular expression for requirement IDs")
    parser.add_argument("--format", choices=["text", "markdown"], default="text",
                        help="report format (default: text)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    requirements = parse_requirements(args.reqs, args.id_pattern)
    if not requirements:
        print(f"tracegate: no requirements found in {' '.join(args.reqs)}", file=sys.stderr)
        return 2
    result = check(requirements, collect_tags(args.tests, args.id_pattern))
    if args.format == "markdown":
        print(report.format_markdown(result))
    else:
        print(report.format_text(result))
    return 0 if result.passed else 1
