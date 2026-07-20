# Visual task brief content model

## Contents

1. Authoring principles
2. Required JSON shape
3. Field guidance
4. Example

## 1. Authoring principles

- Treat the HTML as a reading layer, not as the canonical source of truth.
- Keep facts, recommendations, pending decisions, and risks separate.
- Optimize the first screen for a 60-second read.
- Use diagrams only for relationships; use prose for nuance.
- Never infer approval, completion, deployment, test results, revenue, or user feedback.

## 2. Required JSON shape

The generator accepts one JSON object with these required top-level fields:

| Field | Type | Purpose |
|---|---|---|
| `title` | string | Task-book title |
| `subtitle` | string | One-sentence context |
| `status` | status | Overall document state |
| `updated` | string | Date or timestamp shown to the reader |
| `audience` | string | Intended reader |
| `summary` | object | Four first-screen statements |
| `flow` | array | Ordered 3–7-step connected flow |
| `mindmap` | array | 3–6 scope or architecture branches |
| `scope` | object | Included and excluded boundaries |
| `phases` | array | Delivery stages and outcomes |
| `glossary` | array | Plain-language terminology |
| `decisions` | array | Questions that still require judgment |
| `risks` | array | Concrete risks and responses |
| `acceptance` | array | Observable acceptance evidence |

Allowed status values are:

- `confirmed`: 已确认
- `recommended`: 建议
- `pending`: 待决定
- `risk`: 有风险

Unknown status values are displayed as `待决定`.

## 3. Field guidance

### Summary

Use exactly these string fields:

- `goal`: what changes for the user
- `user`: who benefits and in what situation
- `deliverable`: what tangible artifact will exist
- `success`: what observable evidence means it worked

### Flow

Each item uses:

- `title`: short node label
- `description`: one-sentence explanation
- `status`: optional status

The array order defines the connector direction. If the real system branches heavily, show the dominant path here and use the mind map for branches.

### Mind map

Each branch uses:

- `title`: branch name
- `items`: array of short strings
- `status`: optional status

### Scope

Use `included` and `excluded`, each an array of short strings. Excluded scope is essential when readers might otherwise assume a feature is included.

### Phases

Each phase uses:

- `name`: stage label
- `outcome`: observable result at the end of the stage
- `items`: 1–5 concrete activities
- `status`: status value

### Glossary

Each entry uses:

- `term`: acronym or specialist term
- `plain`: one-sentence plain-language definition
- `why`: why the reader should care in this task

Do not define common words. Prefer 5–12 terms that block understanding.

### Decisions, risks, and acceptance

Decision entry:

- `question`: what must be decided
- `recommendation`: current recommendation or available choice
- `status`: usually `pending` or `recommended`

Risk entry:

- `title`: short risk name
- `impact`: concrete consequence
- `response`: prevention, fallback, or validation action

Acceptance entry:

- `title`: what must be true
- `proof`: observable evidence or artifact
- `status`: use `confirmed` only when already verified; otherwise use `recommended` or `pending`

## 4. Example

Use [../examples/example-task-brief.json](../examples/example-task-brief.json) as a complete input example. It is also the fixture used by the automated validation workflow.
