"""Read requirement definitions and Covers: tags from text files."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

#: Matches IDs such as REQ-TG-001 or REQ-NET-12.
DEFAULT_ID_PATTERN = r"REQ-[A-Z][A-Z0-9]*-\d+"

REQUIREMENT_SUFFIXES = (".md",)


@dataclass(frozen=True)
class Requirement:
    """A requirement defined by a Markdown heading such as '### REQ-TG-001: Title'."""

    req_id: str
    title: str
    path: str
    line: int


def iter_files(paths: Iterable[str | Path], suffixes: tuple[str, ...]) -> Iterator[Path]:
    """Yield each file in *paths*, descending into folders, in a stable order."""
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            yield from sorted(
                p for p in path.rglob("*") if p.is_file() and p.suffix in suffixes
            )
        elif path.is_file():
            yield path


def _heading_regex(id_pattern: str) -> re.Pattern[str]:
    return re.compile(
        rf"^\s{{0,3}}#{{1,6}}\s+(?P<id>{id_pattern})(?![\w-])[\s:.-]*(?P<title>.*?)(?:\s+#+)?\s*$"
    )


def parse_requirements(
    paths: Iterable[str | Path], id_pattern: str = DEFAULT_ID_PATTERN
) -> list[Requirement]:
    """Return every requirement heading found in the Markdown files under *paths*."""
    heading = _heading_regex(id_pattern)
    found: list[Requirement] = []
    for file in iter_files(paths, REQUIREMENT_SUFFIXES):
        text = file.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), start=1):
            match = heading.match(line)
            if match:
                found.append(Requirement(match["id"], match["title"], str(file), number))
    return found


def find_duplicates(requirements: Iterable[Requirement]) -> list[str]:
    """Return the IDs that are defined more than once, sorted."""
    counts = Counter(req.req_id for req in requirements)
    return sorted(req_id for req_id, count in counts.items() if count > 1)
