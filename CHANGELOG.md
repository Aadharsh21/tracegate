# Changelog

All notable changes to tracegate are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-10-20

### Added

- Read requirement IDs and titles from Markdown headings, and report duplicated IDs (#7).
- Collect `Covers:` tags from Python, C and Markdown test files and attribute each one to its test (#9).
- Gate exit status: 0 when fully traced, 1 for uncovered, dangling or duplicated IDs, 2 when no
  requirements are found (#10).
- `--format markdown` traceability matrix, published to the GitHub Actions job summary (#11).
- `--format json` machine-readable report (#12).
- CI on Python 3.10 and 3.12, plus a traceability gate that runs tracegate on its own repository (#8, #10).
