# tracegate

[![CI](https://github.com/Aadharsh21/tracegate/actions/workflows/ci.yml/badge.svg)](https://github.com/Aadharsh21/tracegate/actions/workflows/ci.yml)

A small command-line tool that checks requirements-to-test traceability and works as a CI gate:
the build fails when a requirement has no test, or when a test points at a requirement that does not exist.

Python 3.10 or newer, no dependencies.

## Usage

```bash
python -m tracegate --reqs docs --tests tests
```

```text
tracegate: 9 requirements, 9 covered (100.0%)

  REQ-TG-001  Parse requirement headings        5 tests
  REQ-TG-002  Detect duplicate requirement IDs  2 tests
  ...
  REQ-TG-009  JSON report                       3 tests

PASS: every requirement is covered by at least one test.
```

| Option | Default | Meaning |
| --- | --- | --- |
| `--reqs PATH...` | `docs` | Requirement files or folders (every `.md` file is read) |
| `--tests PATH...` | `tests` | Test files or folders (`.py`, `.md`, `.c`, `.h`, `.cpp`) |
| `--id-pattern REGEX` | `REQ-[A-Z][A-Z0-9]*-\d+` | Your project's requirement ID scheme |
| `--format` | `text` | `text`, `markdown` (a requirement-to-test table) or `json` (for scripts and dashboards) |

### Exit status

| Code | Meaning |
| --- | --- |
| 0 | Every requirement is covered, and nothing is dangling or duplicated |
| 1 | A requirement is uncovered, a tag points at an unknown ID, or an ID is duplicated |
| 2 | No requirements were found (usually a wrong `--reqs` path) |

In CI, the `Traceability gate` job fails on a non-zero exit status and appends the Markdown matrix to
the summary page of every run.

## How tagging works

Requirements are Markdown headings that start with an ID, for example `### REQ-TG-005: Detect uncovered requirements`.
A test names the requirements it verifies on a line that starts with `Covers:`:

```python
def test_reports_uncovered_requirement(self):
    """Covers: REQ-TG-005"""
```

tracegate checks itself: every requirement in [docs/requirements.md](docs/requirements.md) is covered by
a unit test, and the `Traceability gate` job in CI enforces it on every pull request.

## Contributing

The branching model, commit conventions and the requirements rule are in [CONTRIBUTING.md](CONTRIBUTING.md).
Release notes are in [CHANGELOG.md](CHANGELOG.md).

## License

MIT, see [LICENSE](LICENSE).
