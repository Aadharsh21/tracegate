# tracegate requirements

Every requirement has a stable ID. Tests name the requirements they verify on a `Covers:` line,
so each requirement below can be traced to the tests that prove it.

### REQ-TG-001: Parse requirement headings

The tool shall record every Markdown heading whose text starts with a requirement ID, together
with the heading's title, file and line number. IDs follow the pattern `REQ-<AREA>-<NUMBER>`
by default, and a project can supply its own pattern.

### REQ-TG-002: Detect duplicate requirement IDs

The tool shall report every requirement ID that is defined more than once.

### REQ-TG-003: Collect Covers tags

The tool shall record every requirement ID listed on a line that starts with `Covers:`, either
directly or right after a comment or docstring marker. A `Covers:` that appears in the middle of
a line shall be ignored, so prose and test fixtures do not create false links.

### REQ-TG-004: Attribute tags to tests

The tool shall attribute each `Covers:` tag to the nearest preceding test function
(`def test_...` in Python, `void test_...` in C) or, in a Markdown test specification, to the
nearest preceding heading. A tag outside any test is reported by file and line.
