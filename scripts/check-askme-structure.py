#!/usr/bin/env python3
"""Validate structural rules for the AskMe design draft."""

from __future__ import annotations

import re
import sys
from pathlib import Path


DEFAULT_DOCUMENT = Path("drafts/devflow/asdm-devflow-skill-askme-design.md")
HEADING_RE = re.compile(
    r"^###\s+(?:决策点|条件决策点)\s+(D-[A-Z0-9]+)(?::|：)(.+)$"
)
DOTTED_HEADING_RE = re.compile(
    r"^###\s+(?:决策点|条件决策点)\s+(D-[A-Z0-9]+)\.([0-9]+)(?::|：)(.+)$"
)
DOTTED_ID_RE = re.compile(r"\bD-[A-Z0-9]+\.[0-9]+\b")
DECISION_INDEX_RE = re.compile(r"(?:独立|关联)决策项索引")


def validate(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    decision_ids: dict[str, int] = {}
    domain_numbers: dict[str, list[int]] = {}
    for line_number, line in enumerate(lines, start=1):
        dotted_heading = DOTTED_HEADING_RE.match(line)
        heading = HEADING_RE.match(line) if not dotted_heading else None

        if dotted_heading:
            decision_id = f"{dotted_heading.group(1)}.{dotted_heading.group(2)}"
            title = dotted_heading.group(3)
            if decision_id in decision_ids:
                errors.append(
                    f"{path}:{line_number}: duplicate decision id {decision_id} "
                    f"(first at line {decision_ids[decision_id]})"
                )
            else:
                decision_ids[decision_id] = line_number

            errors.append(
                f"{path}:{line_number}: decision headings must use a single-level "
                f"id; dotted decision id is not allowed ({decision_id})"
            )

        elif heading:
            decision_id = heading.group(1)
            if decision_id in decision_ids:
                errors.append(
                    f"{path}:{line_number}: duplicate decision id {decision_id} "
                    f"(first at line {decision_ids[decision_id]})"
                )
            else:
                decision_ids[decision_id] = line_number
            match = re.fullmatch(r"D-([A-Z])(\d+)", decision_id)
            if match:
                domain_numbers.setdefault(match.group(1), []).append(
                    int(match.group(2))
                )

        if not dotted_heading:
            dotted_reference = DOTTED_ID_RE.search(line)
            if dotted_reference:
                errors.append(
                    f"{path}:{line_number}: dotted decision id is not allowed "
                    f"outside migration history ({dotted_reference.group(0)})"
                )

        if DECISION_INDEX_RE.search(line):
            errors.append(
                f"{path}:{line_number}: decision indexes are not allowed; keep "
                "explanatory content inside its parent decision"
            )

    for domain, numbers in domain_numbers.items():
        expected = list(range(1, len(numbers) + 1))
        if numbers != expected:
            errors.append(
                f"{path}: decision ids in domain {domain} must appear in "
                f"continuous document order; found {numbers}, expected {expected}"
            )

    return errors


def main(argv: list[str]) -> int:
    paths = [Path(value) for value in argv] or [DEFAULT_DOCUMENT]
    errors: list[str] = []
    for path in paths:
        if not path.is_file():
            errors.append(f"{path}: file does not exist")
            continue
        errors.extend(validate(path))

    if errors:
        print("AskMe structure check failed:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("AskMe structure check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
