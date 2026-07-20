#!/usr/bin/env python3
"""Install Visual Task Brief for Codex, Claude Code, and Kimi Code."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


SKILL_NAME = "visual-task-brief"
COPY_ENTRIES = (
    "SKILL.md",
    "agents",
    "assets",
    "examples",
    "references",
    "scripts",
    "LICENSE",
)


def target_paths(home: Path) -> dict[str, Path]:
    return {
        "codex": home / ".codex" / "skills" / SKILL_NAME,
        "claude": home / ".claude" / "skills" / SKILL_NAME,
        "kimi": home / ".config" / "agents" / "skills" / SKILL_NAME,
    }


def same_location(left: Path, right: Path) -> bool:
    try:
        return left.resolve() == right.resolve()
    except OSError:
        return False


def copy_entry(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def install(source_root: Path, destination: Path, force: bool) -> str:
    if same_location(source_root, destination):
        return f"SKIP {destination} (already running from this installation)"

    backup: Path | None = None
    if destination.exists() or destination.is_symlink():
        if not force:
            raise FileExistsError(
                f"{destination} already exists; rerun with --force to back it up and replace it"
            )
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = destination.with_name(f"{destination.name}.backup-{stamp}")
        if backup.exists():
            raise FileExistsError(f"Backup path already exists: {backup}")
        destination.rename(backup)

    destination.mkdir(parents=True, exist_ok=False)
    try:
        for entry in COPY_ENTRIES:
            source = source_root / entry
            if source.exists():
                copy_entry(source, destination / entry)
        if not (destination / "SKILL.md").is_file():
            raise RuntimeError("Installed package is missing SKILL.md")
    except Exception:
        shutil.rmtree(destination, ignore_errors=True)
        if backup is not None:
            backup.rename(destination)
        raise

    suffix = f" (backup: {backup})" if backup else ""
    return f"OK   {destination}{suffix}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=("all", "codex", "claude", "kimi"),
        default=("all",),
        help="Clients to install for (default: all)",
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Home directory override, useful for testing",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Back up and replace an existing installation",
    )
    args = parser.parse_args()

    selected = ["codex", "claude", "kimi"] if "all" in args.targets else list(dict.fromkeys(args.targets))
    source_root = Path(__file__).resolve().parent.parent
    paths = target_paths(args.home.expanduser().resolve())

    try:
        for name in selected:
            print(f"{name:7} {install(source_root, paths[name], args.force)}")
    except (OSError, RuntimeError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
