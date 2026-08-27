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
DEPENDENCY_FIELD_RE = re.compile(r"^\*\*前置依赖\*\*：(.+)$")
DEPENDENCY_ID_RE = re.compile(r"\bD-[A-Z]\d+\b")


def validate(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    decision_ids: dict[str, int] = {}
    domain_numbers: dict[str, list[int]] = {}
    dependencies: list[tuple[str, str, int]] = []
    current_decision_id: str | None = None
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
            current_decision_id = None

        elif heading:
            decision_id = heading.group(1)
            current_decision_id = decision_id
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
        elif line.startswith("### "):
            current_decision_id = None

        dependency_field = DEPENDENCY_FIELD_RE.match(line)
        if dependency_field and current_decision_id:
            for dependency_id in DEPENDENCY_ID_RE.findall(
                dependency_field.group(1)
            ):
                dependencies.append(
                    (current_decision_id, dependency_id, line_number)
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

    for decision_id, dependency_id, line_number in dependencies:
        dependency_line = decision_ids.get(dependency_id)
        if dependency_line is None:
            errors.append(
                f"{path}:{line_number}: prerequisite {dependency_id} referenced "
                f"by {decision_id} does not exist"
            )
        elif dependency_line >= decision_ids[decision_id]:
            errors.append(
                f"{path}:{line_number}: prerequisite {dependency_id} for "
                f"{decision_id} must appear before the dependent decision "
                f"(found at line {dependency_line})"
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
