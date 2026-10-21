# tracegate

[![CI](https://github.com/Aadharsh21/tracegate/actions/workflows/ci.yml/badge.svg)](https://github.com/Aadharsh21/tracegate/actions/workflows/ci.yml)

A small command-line tool that checks requirements-to-test traceability and works as a CI gate:
the build fails when a requirement has no test, or when a test points at a requirement that does not exist.

## Usage

```bash
python -m tracegate --reqs docs --tests tests
```

tracegate prints one line per requirement with the number of tests that cover it, then `PASS` or `FAIL`.
It exits with status 1 when a requirement is uncovered, a tag points at an unknown ID, or an ID is
duplicated, so the CI step fails on its own.

Add `--format markdown` to print the same result as a requirement-to-test table. CI appends that
table to the summary page of every run.

Add `--format json` for a machine-readable report that scripts and dashboards can consume.

## How tagging works

Requirements are Markdown headings that start with an ID, for example `### REQ-TG-005: Detect uncovered requirements`.
A test names the requirements it verifies on a line that starts with `Covers:`:

```python
def test_reports_uncovered_requirement(self):
    """Covers: REQ-TG-005"""
```

tracegate checks itself: every requirement in [docs/requirements.md](docs/requirements.md) is covered by
a unit test, and the `Traceability gate` job in CI enforces it on every pull request.

## License

MIT, see [LICENSE](LICENSE).
