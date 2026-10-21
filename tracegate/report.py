"""Render a TraceResult for people and for other tools."""

from __future__ import annotations

import json

from .check import TraceResult


def _plural(count: int, word: str) -> str:
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


def _summary(result: TraceResult) -> str:
    return (
        f"{_plural(result.total, 'requirement')}, {result.covered} covered "
        f"({result.coverage:.1%})"
    )


def _verdict(result: TraceResult) -> str:
    if result.passed:
        return "PASS: every requirement is covered by at least one test."
    problems = []
    if result.uncovered:
        ids = ", ".join(req.req_id for req in result.uncovered)
        problems.append(f"{_plural(len(result.uncovered), 'uncovered requirement')} ({ids})")
    if result.dangling:
        problems.append(_plural(len(result.dangling), "dangling tag"))
    if result.duplicates:
        problems.append(_plural(len(result.duplicates), "duplicate ID"))
    if not result.total:
        problems.append("no requirements found")
    return "FAIL: " + "; ".join(problems)


def format_text(result: TraceResult) -> str:
    """Return a human-readable report with one line per requirement."""
    width = min(max((len(req.title) for req in result.requirements), default=0), 44)
    lines = [f"tracegate: {_summary(result)}", ""]
    for req in result.requirements:
        tests = result.matrix[req.req_id]
        status = _plural(len(tests), "test") if tests else "MISSING"
        title = req.title if len(req.title) <= width else req.title[: width - 3] + "..."
        lines.append(f"  {req.req_id:<11} {title:<{width}}  {status}")
    for tag in result.dangling:
        lines.append(f"  dangling    {tag.req_id} in {tag.test} ({tag.path}:{tag.line})")
    for req_id in result.duplicates:
        lines.append(f"  duplicate   {req_id} is defined more than once")
    lines += ["", _verdict(result)]
    return "\n".join(lines)


def format_markdown(result: TraceResult) -> str:
    """Return the traceability matrix as a Markdown table (for GitHub job summaries)."""
    lines = [
        "### Traceability matrix",
        "",
        "| Requirement | Title | Covered by | Status |",
        "| --- | --- | --- | --- |",
    ]
    for req in result.requirements:
        tests = result.matrix[req.req_id]
        covered_by = "<br>".join(f"`{tag.test}`" for tag in tests) or "none"
        status = "✅ covered" if tests else "❌ missing"
        title = req.title.replace("|", "\\|")
        lines.append(f"| {req.req_id} | {title} | {covered_by} | {status} |")
    notes = [f"- ❌ dangling tag `{tag.req_id}` in `{tag.test}`" for tag in result.dangling]
    notes += [f"- ❌ `{req_id}` is defined more than once" for req_id in result.duplicates]
    if notes:
        lines += [""] + notes
    verdict = "PASS" if result.passed else "FAIL"
    lines += ["", f"**Coverage:** {_summary(result)}. **Result:** {verdict}"]
    return "\n".join(lines)


def format_json(result: TraceResult) -> str:
    """Return the full result as JSON for scripts and dashboards."""
    data = {
        "passed": result.passed,
        "requirements": result.total,
        "covered": result.covered,
        "coverage": round(result.coverage, 4),
        "uncovered": [req.req_id for req in result.uncovered],
        "dangling": [
            {"id": tag.req_id, "test": tag.test, "path": tag.path, "line": tag.line}
            for tag in result.dangling
        ],
        "duplicates": result.duplicates,
        "matrix": {req_id: [tag.test for tag in tags] for req_id, tags in result.matrix.items()},
    }
    return json.dumps(data, indent=2)
