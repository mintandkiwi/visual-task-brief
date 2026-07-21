# Visual delivery report content model

## Contents

1. Evidence rules
2. Required JSON shape
3. Status values
4. Field guidance
5. Example

## 1. Evidence rules

- Describe only artifacts and behavior that actually exist at delivery time.
- Separate automated test results, static checks, manual inspection, user acceptance, commit/push, deployment, and release.
- Use `passed` only when the named check ran successfully and evidence is available.
- Use `manual` when the user still needs to inspect permissions, hardware, visual behavior, or a real environment.
- Use `partial`, `pending`, `not-run`, or `risk` instead of rounding incomplete work up to “done”.
- Link or name the actual file, command, test log, commit, build artifact, screenshot, or recording used as evidence.

## 2. Required JSON shape

| Field | Type | Purpose |
|---|---|---|
| `title` | string | Delivery report title |
| `subtitle` | string | One-sentence outcome |
| `status` | status | Overall delivery state |
| `updated` | string | Delivery date or timestamp |
| `audience` | string | Intended reader |
| `summary` | object | Four first-screen statements |
| `deliverables` | array | Concrete artifacts delivered |
| `flow` | array | 3–7-step usage or outcome path |
| `map` | array | 3–6 delivery branches |
| `changes` | array | Before/after comparisons |
| `verification` | array | Checks and their evidence |
| `usage` | array | How to start using the delivery |
| `files` | array | Numbered file index |
| `limitations` | array | Remaining boundaries and next actions |
| `glossary` | array | Plain-language terminology |

## 3. Status values

- `confirmed`: 已交付 / 已确认
- `passed`: 已通过验证
- `partial`: 部分完成
- `pending`: 待处理
- `manual`: 待人工验收
- `not-run`: 未执行
- `risk`: 有风险

Unknown values are not accepted by the generator.

## 4. Field guidance

### Summary

Use exactly these string fields:

- `delivered`: the most important thing now available
- `value`: what the user can do with it
- `verification`: the strongest verified evidence
- `next`: the most important remaining action or “无需额外操作”

### Deliverables

Each item uses `name`, `type`, `description`, `path`, `evidence`, and `status`.
Do not use “complete” without a concrete path or evidence statement.

### Flow

Each item uses `title`, `description`, and `status`. Array order defines the connector direction. Prefer the reader's use path over an internal development chronology.

### Map

Each branch uses `title`, `items`, and optional `status`. Use this for delivered modules, files, interfaces, documentation, or quality evidence.

### Changes

Each item uses `area`, `before`, `after`, and `impact`. Keep the comparison observable.

### Verification

Each item uses `name`, `result`, `evidence`, and `status`. Never combine different evidence levels into one row.

### Usage

Each item uses `step`, `action`, and `result`. Use 1–6 concise steps.

### Files

Each item uses `number`, `name`, `purpose`, `path`, and `status`. The number is the reader-facing index for the artifact, not the HTML document sequence.

### Limitations

Each item uses `title`, `impact`, `next`, and `status`. This section must remain visible even when everything automated has passed.

### Glossary

Each item uses `term`, `plain`, and `why`. Use an empty array when no specialist term blocks understanding.

## 5. Example

Use [../examples/example-delivery-report.json](../examples/example-delivery-report.json) as the complete fixture.
