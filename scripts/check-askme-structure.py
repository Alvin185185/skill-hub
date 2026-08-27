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
EXPLANATORY_TITLE_RE = re.compile(r"^\s*(?:成功结果|成功标准|非目标|验收指标)(?:[：: ]|$)")


def validate(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    decision_ids: dict[str, int] = {}
    in_a11 = False

    for line_number, line in enumerate(lines, start=1):
        if line.startswith("## "):
            in_a11 = False

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

            if decision_id.startswith("D-A11.") or EXPLANATORY_TITLE_RE.search(title):
                errors.append(
                    f"{path}:{line_number}: explanatory content must not be a "
                    f"dotted decision heading ({decision_id})"
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

            in_a11 = decision_id == "D-A11"

        if in_a11 and "独立决策项索引" in line:
            errors.append(
                f"{path}:{line_number}: D-A11 must not contain an independent "
                "decision index"
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
