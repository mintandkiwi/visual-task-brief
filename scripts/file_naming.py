#!/usr/bin/env python3
"""Shared deterministic numbering and naming for visual HTML artifacts."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path


NUMBERED_HTML = re.compile(r"^(?P<number>\d{2,})-(?P<label>.+)\.html$", re.IGNORECASE)


def safe_slug(value: str, fallback: str = "project") -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().lower()
    normalized = re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "-", normalized)
    normalized = re.sub(r"[\s_]+", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip("-. ")
    return (normalized or fallback)[:80].rstrip("-. ")


def next_sequence(directory: Path) -> int:
    maximum = 0
    if directory.exists():
        for candidate in directory.glob("*.html"):
            match = NUMBERED_HTML.match(candidate.name)
            if match:
                maximum = max(maximum, int(match.group("number")))
    return maximum + 1


def numbered_output(
    directory: Path,
    document_type: str,
    project: str,
    sequence: int | None = None,
) -> Path:
    if sequence is not None and sequence < 1:
        raise ValueError("sequence must be at least 1")
    number = sequence if sequence is not None else next_sequence(directory)
    width = max(2, len(str(number)))
    filename = f"{number:0{width}d}-{safe_slug(document_type)}-{safe_slug(project)}.html"
    output = directory / filename
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing numbered HTML: {output}")
    return output


def validate_explicit_output(output: Path) -> None:
    if output.suffix.lower() != ".html":
        raise ValueError("output must use the .html extension")
    if not NUMBERED_HTML.match(output.name):
        raise ValueError(
            "output filename must start with a two-digit sequence and a readable name, "
            "for example 01-task-brief-my-project.html"
        )


def document_metadata(output: Path, document_type: str) -> dict[str, str | int]:
    match = NUMBERED_HTML.match(output.name)
    return {
        "number": int(match.group("number")) if match else 0,
        "filename": output.name,
        "type": document_type,
    }
