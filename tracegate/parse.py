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


TEST_SUFFIXES = (".py", ".md", ".c", ".h", ".cpp")


@dataclass(frozen=True)
class CoverTag:
    """One requirement ID listed on a 'Covers:' line, and the test it belongs to."""

    req_id: str
    test: str
    path: str
    line: int


# 'Covers:' must start the line, or start the comment or docstring on it, so
# prose and string fixtures that merely mention the word are not counted.
_COVERS_LINE = re.compile(
    r"""^\s*(?:\#+|//+|/?\*+|-|>|"{3}|'{3})?\s*Covers:\s*(?P<ids>.*?)\s*(?:"{3}|'{3}|\*/)?\s*$"""
)
_TEST_DEF = re.compile(
    r"^\s*(?:async\s+def|def|(?:static\s+)?(?:void|int))\s+(?P<name>test\w*)\s*\("
)
_MD_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(?P<name>.+?)\s*$")


def collect_tags(
    paths: Iterable[str | Path], id_pattern: str = DEFAULT_ID_PATTERN
) -> list[CoverTag]:
    """Return every requirement ID listed on a 'Covers:' line in the test files.

    Each tag is attributed to the nearest preceding test function (or, in a
    Markdown test specification, the nearest preceding heading).
    """
    id_regex = re.compile(id_pattern)
    id_list = re.compile(rf"(?:{id_pattern})(?:\s*[,;]?\s*(?:{id_pattern}))*[.,;]?")
    tags: list[CoverTag] = []
    for file in iter_files(paths, TEST_SUFFIXES):
        enclosing = _MD_HEADING if file.suffix == ".md" else _TEST_DEF
        current_test: str | None = None
        text = file.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), start=1):
            match = _COVERS_LINE.match(line)
            if match and id_list.fullmatch(match["ids"]):
                name = f"{file.name}::{current_test}" if current_test else f"{file.name}:{number}"
                tags.extend(
                    CoverTag(req_id, name, str(file), number)
                    for req_id in id_regex.findall(match["ids"])
                )
                continue
            definition = enclosing.match(line)
            if definition:
                current_test = definition["name"]
    return tags
