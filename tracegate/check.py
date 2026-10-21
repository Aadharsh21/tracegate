"""Compare requirements against Covers: tags."""

from __future__ import annotations

from dataclasses import dataclass

from .parse import CoverTag, Requirement, find_duplicates


@dataclass
class TraceResult:
    """The outcome of a traceability check."""

    requirements: list[Requirement]
    matrix: dict[str, list[CoverTag]]
    uncovered: list[Requirement]
    dangling: list[CoverTag]
    duplicates: list[str]

    @property
    def total(self) -> int:
        return len(self.requirements)

    @property
    def covered(self) -> int:
        return self.total - len(self.uncovered)

    @property
    def coverage(self) -> float:
        return self.covered / self.total if self.total else 0.0

    @property
    def passed(self) -> bool:
        return self.total > 0 and not (self.uncovered or self.dangling or self.duplicates)


def check(requirements: list[Requirement], tags: list[CoverTag]) -> TraceResult:
    """Map every requirement to the tags that cover it, and collect the gaps."""
    unique: dict[str, Requirement] = {}
    for req in requirements:
        unique.setdefault(req.req_id, req)
    matrix: dict[str, list[CoverTag]] = {req_id: [] for req_id in unique}
    dangling: list[CoverTag] = []
    for tag in tags:
        if tag.req_id in matrix:
            matrix[tag.req_id].append(tag)
        else:
            dangling.append(tag)
    uncovered = [req for req in unique.values() if not matrix[req.req_id]]
    return TraceResult(
        list(unique.values()), matrix, uncovered, dangling, find_duplicates(requirements)
    )
