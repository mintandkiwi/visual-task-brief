#!/usr/bin/env python3
"""Build a standalone visual task brief from validated JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "title": str,
    "subtitle": str,
    "status": str,
    "updated": str,
    "audience": str,
    "summary": dict,
    "flow": list,
    "mindmap": list,
    "scope": dict,
    "phases": list,
    "glossary": list,
    "decisions": list,
    "risks": list,
    "acceptance": list,
}
SUMMARY_FIELDS = ("goal", "user", "deliverable", "success")
VALID_STATUSES = {"confirmed", "recommended", "pending", "risk"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_string_list(value: Any, path: str) -> None:
    require(isinstance(value, list), f"{path} must be an array")
    require(all(isinstance(item, str) and item.strip() for item in value),
            f"{path} must contain non-empty strings")


def validate_records(value: Any, path: str, required: tuple[str, ...]) -> None:
    require(isinstance(value, list), f"{path} must be an array")
    for index, item in enumerate(value):
        require(isinstance(item, dict), f"{path}[{index}] must be an object")
        for field in required:
            require(isinstance(item.get(field), str) and item[field].strip(),
                    f"{path}[{index}].{field} must be a non-empty string")
        status = item.get("status")
        require(status is None or status in VALID_STATUSES,
                f"{path}[{index}].status must be one of {sorted(VALID_STATUSES)}")


def validate(data: Any) -> dict[str, Any]:
    require(isinstance(data, dict), "Input must be a JSON object")
    for key, expected_type in REQUIRED_TOP_LEVEL.items():
        require(key in data, f"Missing required field: {key}")
        require(isinstance(data[key], expected_type),
                f"{key} must be {expected_type.__name__}")

    for key in ("title", "subtitle", "updated", "audience"):
        require(data[key].strip(), f"{key} must not be empty")
    require(data["status"] in VALID_STATUSES,
            f"status must be one of {sorted(VALID_STATUSES)}")

    for field in SUMMARY_FIELDS:
        require(isinstance(data["summary"].get(field), str)
                and data["summary"][field].strip(),
                f"summary.{field} must be a non-empty string")

    require(3 <= len(data["flow"]) <= 7, "flow must contain 3 to 7 nodes")
    validate_records(data["flow"], "flow", ("title", "description"))

    require(3 <= len(data["mindmap"]) <= 6,
            "mindmap must contain 3 to 6 branches")
    for index, branch in enumerate(data["mindmap"]):
        require(isinstance(branch, dict), f"mindmap[{index}] must be an object")
        require(isinstance(branch.get("title"), str) and branch["title"].strip(),
                f"mindmap[{index}].title must be a non-empty string")
        validate_string_list(branch.get("items"), f"mindmap[{index}].items")

    validate_string_list(data["scope"].get("included"), "scope.included")
    validate_string_list(data["scope"].get("excluded"), "scope.excluded")

    validate_records(data["phases"], "phases", ("name", "outcome"))
    for index, phase in enumerate(data["phases"]):
        validate_string_list(phase.get("items"), f"phases[{index}].items")
    validate_records(data["glossary"], "glossary", ("term", "plain", "why"))
    validate_records(data["decisions"], "decisions", ("question", "recommendation"))
    validate_records(data["risks"], "risks", ("title", "impact", "response"))
    validate_records(data["acceptance"], "acceptance", ("title", "proof"))
    return data


def safe_json_for_script(data: dict[str, Any]) -> str:
    rendered = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return (rendered.replace("<", "\\u003c")
            .replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 JSON source")
    parser.add_argument("--output", required=True, type=Path, help="Output HTML path")
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "assets" / "task-brief-template.html",
        help="Optional template override",
    )
    args = parser.parse_args()

    try:
        data = validate(json.loads(args.input.read_text(encoding="utf-8")))
        template = args.template.read_text(encoding="utf-8")
        marker = "/*__TASK_BRIEF_DATA__*/"
        require(template.count(marker) == 1, "Template must contain exactly one data marker")
        output = template.replace(marker, safe_json_for_script(data))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Built {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
