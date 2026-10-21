# tracegate requirements

Every requirement has a stable ID. Tests name the requirements they verify on a `Covers:` line,
so each requirement below can be traced to the tests that prove it.

### REQ-TG-001: Parse requirement headings

The tool shall record every Markdown heading whose text starts with a requirement ID, together
with the heading's title, file and line number. IDs follow the pattern `REQ-<AREA>-<NUMBER>`
by default, and a project can supply its own pattern.

### REQ-TG-002: Detect duplicate requirement IDs

The tool shall report every requirement ID that is defined more than once.
