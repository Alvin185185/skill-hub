#!/usr/bin/env python3
"""Regression tests for the AskMe structure validator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "scripts" / "check-askme-structure.py"


def run_checker(content: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        document = Path(directory) / "fixture.md"
        document.write_text(content, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(CHECKER), str(document)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )


def main() -> int:
    dotted = run_checker("### 决策点 D-B1.1：角色\n")
    assert dotted.returncode == 1, dotted.stdout + dotted.stderr
    assert "dotted decision id is not allowed" in dotted.stderr

    dotted_reference = run_checker("| D-B1.1 | 旧索引 |\n")
    assert dotted_reference.returncode == 1, dotted_reference.stdout + dotted_reference.stderr
    assert "outside migration history" in dotted_reference.stderr

    conditional_heading = run_checker("### 条件决策点 M1.1：目标\n")
    assert conditional_heading.returncode == 1, (
        conditional_heading.stdout + conditional_heading.stderr
    )
    assert "conditional decision headings are not allowed" in conditional_heading.stderr

    conditional_reference = run_checker("| M1.1 | 目标 |\n")
    assert conditional_reference.returncode == 1, (
        conditional_reference.stdout + conditional_reference.stderr
    )
    assert "dotted conditional id is not allowed" in conditional_reference.stderr

    decision_index = run_checker("**关联决策项索引**：\n")
    assert decision_index.returncode == 1, decision_index.stdout + decision_index.stderr
    assert "decision indexes are not allowed" in decision_index.stderr

    single_level = run_checker(
        "### 决策点 D-B1：一\n"
        "### 决策点 D-B2：二\n"
        "### 决策点 D-B3：三\n"
        "### 决策点 D-B4：角色\n"
    )
    assert single_level.returncode == 0, single_level.stdout + single_level.stderr

    duplicate = run_checker(
        "### 决策点 D-B4：角色\n\n### 决策点 D-B4：重复\n"
    )
    assert duplicate.returncode == 1, duplicate.stdout + duplicate.stderr
    assert "duplicate decision id D-B4" in duplicate.stderr

    gap = run_checker(
        "### 决策点 D-B1：一\n\n### 决策点 D-B3：三\n"
    )
    assert gap.returncode == 1, gap.stdout + gap.stderr
    assert "continuous document order" in gap.stderr

    reordered = run_checker(
        "### 决策点 D-B2：二\n\n### 决策点 D-B1：一\n"
    )
    assert reordered.returncode == 1, reordered.stdout + reordered.stderr
    assert "continuous document order" in reordered.stderr

    ordered_dependency = run_checker(
        "### 决策点 D-B1：前置\n"
        "\n**前置依赖**：无。\n"
        "\n### 决策点 D-B2：后置\n"
        "\n**前置依赖**：D-B1。\n"
    )
    assert ordered_dependency.returncode == 0, (
        ordered_dependency.stdout + ordered_dependency.stderr
    )

    forward_dependency = run_checker(
        "### 决策点 D-B1：错误前置\n"
        "\n**前置依赖**：D-B2。\n"
        "\n### 决策点 D-B2：被依赖项\n"
        "\n**前置依赖**：无。\n"
    )
    assert forward_dependency.returncode == 1, (
        forward_dependency.stdout + forward_dependency.stderr
    )
    assert "must appear before the dependent decision" in forward_dependency.stderr

    missing_dependency = run_checker(
        "### 决策点 D-B1：缺失前置\n"
        "\n**前置依赖**：D-C1。\n"
    )
    assert missing_dependency.returncode == 1, (
        missing_dependency.stdout + missing_dependency.stderr
    )
    assert "prerequisite D-C1 referenced by D-B1 does not exist" in (
        missing_dependency.stderr
    )

    print("AskMe structure validator tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
