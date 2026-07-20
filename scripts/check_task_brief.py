#!/usr/bin/env python3
"""Run deterministic structural checks on a generated visual task brief."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path


class BriefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.tags: list[str] = []
        self.external_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        for key in ("src", "href"):
            value = values.get(key) or ""
            if re.match(r"^(?:https?:)?//", value):
                self.external_urls.append(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    source = args.html.read_text(encoding="utf-8")
    parsed = BriefParser()
    parsed.feed(source)

    required_ids = {
        "overview", "flow", "mindmap", "scope", "phases",
        "glossary", "decisions", "risks", "acceptance",
    }
    checks = {
        "doctype": source.lstrip().lower().startswith("<!doctype html>"),
        "language": 'lang="zh-CN"' in source,
        "viewport": 'name="viewport"' in source,
        "all visual sections": required_ids.issubset(parsed.ids),
        "inline SVG": "<svg" in source,
        "print stylesheet": "@media print" in source,
        "mobile breakpoint": "@media (max-width: 720px)" in source,
        "reduced motion": "prefers-reduced-motion" in source,
        "skip link": 'class="skip-link"' in source,
        "no unresolved marker": "__TASK_BRIEF_DATA__" not in source,
        "no external resources": not parsed.external_urls,
        "no horizontal overflow hack": "user-scalable=no" not in source,
    }
    failed = [name for name, ok in checks.items() if not ok]
    for name, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if failed:
        print(f"Structural validation failed: {', '.join(failed)}")
        return 1
    print(f"Validated {args.html.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
