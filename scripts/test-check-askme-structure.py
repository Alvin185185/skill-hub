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
    assert "missing D-B2" in gap.stderr

    print("AskMe structure validator tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
