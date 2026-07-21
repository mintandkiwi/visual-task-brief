#!/usr/bin/env python3
"""Build a numbered standalone visual delivery report from validated JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from file_naming import document_metadata, numbered_output, validate_explicit_output


VALID_STATUSES = {"confirmed", "passed", "partial", "pending", "manual", "not-run", "risk"}
REQUIRED_TOP_LEVEL = {
    "title": str,
    "subtitle": str,
    "status": str,
    "updated": str,
    "audience": str,
    "summary": dict,
    "deliverables": list,
    "flow": list,
    "map": list,
    "changes": list,
    "verification": list,
    "usage": list,
    "files": list,
    "limitations": list,
    "glossary": list,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_records(value: Any, path: str, required: tuple[str, ...], *, allow_empty: bool = False) -> None:
    require(isinstance(value, list), f"{path} must be an array")
    require(allow_empty or bool(value), f"{path} must contain at least one item")
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
        require(isinstance(data[key], expected_type), f"{key} must be {expected_type.__name__}")
    for key in ("title", "subtitle", "updated", "audience"):
        require(data[key].strip(), f"{key} must not be empty")
    require(data["status"] in VALID_STATUSES,
            f"status must be one of {sorted(VALID_STATUSES)}")

    for field in ("delivered", "value", "verification", "next"):
        require(isinstance(data["summary"].get(field), str) and data["summary"][field].strip(),
                f"summary.{field} must be a non-empty string")

    validate_records(data["deliverables"], "deliverables",
                     ("name", "type", "description", "path", "evidence", "status"))
    require(3 <= len(data["flow"]) <= 7, "flow must contain 3 to 7 nodes")
    validate_records(data["flow"], "flow", ("title", "description", "status"))
    require(3 <= len(data["map"]) <= 6, "map must contain 3 to 6 branches")
    for index, branch in enumerate(data["map"]):
        require(isinstance(branch, dict), f"map[{index}] must be an object")
        require(isinstance(branch.get("title"), str) and branch["title"].strip(),
                f"map[{index}].title must be a non-empty string")
        items = branch.get("items")
        require(isinstance(items, list) and items,
                f"map[{index}].items must be a non-empty array")
        require(all(isinstance(item, str) and item.strip() for item in items),
                f"map[{index}].items must contain non-empty strings")

    validate_records(data["changes"], "changes", ("area", "before", "after", "impact"))
    validate_records(data["verification"], "verification", ("name", "result", "evidence", "status"))
    validate_records(data["usage"], "usage", ("step", "action", "result"))
    validate_records(data["files"], "files", ("number", "name", "purpose", "path", "status"))
    validate_records(data["limitations"], "limitations", ("title", "impact", "next", "status"))
    validate_records(data["glossary"], "glossary", ("term", "plain", "why"), allow_empty=True)
    return data


def safe_json_for_script(data: dict[str, Any]) -> str:
    rendered = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return (rendered.replace("<", "\\u003c")
            .replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 JSON source")
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("--output", type=Path, help="Explicit numbered HTML path")
    destination.add_argument("--output-dir", type=Path, help="Directory for automatic numbering")
    parser.add_argument("--project", help="Readable project name used with --output-dir")
    parser.add_argument("--sequence", type=int, help="Optional explicit sequence with --output-dir")
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "assets" / "delivery-report-template.html",
        help="Optional template override",
    )
    args = parser.parse_args()

    try:
        data = validate(json.loads(args.input.read_text(encoding="utf-8")))
        if args.output_dir:
            require(bool(args.project and args.project.strip()), "--project is required with --output-dir")
            output_path = numbered_output(args.output_dir, "delivery-report", args.project, args.sequence)
        else:
            require(args.sequence is None, "--sequence requires --output-dir")
            require(args.project is None, "--project requires --output-dir")
            output_path = args.output
            validate_explicit_output(output_path)
            require(not output_path.exists(), f"Refusing to overwrite existing HTML: {output_path}")
        data["_document"] = document_metadata(output_path, "delivery-report")
        template = args.template.read_text(encoding="utf-8")
        marker = "/*__DELIVERY_REPORT_DATA__*/"
        require(template.count(marker) == 1, "Template must contain exactly one data marker")
        output = template.replace(marker, safe_json_for_script(data))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Built {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
