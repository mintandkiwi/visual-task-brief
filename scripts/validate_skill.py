#!/usr/bin/env python3
"""Validate the portable Agent Skills package without third-party dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_PATHS = (
    "SKILL.md",
    "assets/task-brief-template.html",
    "references/content-model.md",
    "scripts/build_task_brief.py",
    "scripts/check_task_brief.py",
)


def parse_frontmatter(path: Path) -> dict[str, str]:
    source = path.read_text(encoding="utf-8")
    if not source.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    parts = source.split("---", 2)
    if len(parts) != 3:
        raise ValueError("SKILL.md frontmatter is not closed")
    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line.strip() or line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    root = args.skill_dir.resolve()
    failures: list[str] = []

    for relative in REQUIRED_PATHS:
        if not (root / relative).is_file():
            failures.append(f"missing {relative}")

    try:
        metadata = parse_frontmatter(root / "SKILL.md")
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name != root.name:
            failures.append(f"name must match directory name ({root.name})")
        if not NAME_PATTERN.fullmatch(name):
            failures.append("name must use lowercase letters, digits, and hyphens")
        if not 1 <= len(description) <= 1024:
            failures.append("description must contain 1 to 1024 characters")
    except (OSError, ValueError) as exc:
        failures.append(str(exc))

    skill_source = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").is_file() else ""
    hardcoded_paths = ("~/.codex/skills/visual-task-brief", "~/.claude/skills/visual-task-brief", "~/.kimi/skills/visual-task-brief")
    for path in hardcoded_paths:
        if path in skill_source:
            failures.append(f"SKILL.md contains client-specific runtime path: {path}")

    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        return 1
    print(f"[PASS] portable Agent Skill: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
