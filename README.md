# Visual Task Brief & Delivery Report

[简体中文](README.zh-CN.md) | English

[![Test](https://github.com/mintandkiwi/visual-task-brief/actions/workflows/test.yml/badge.svg)](https://github.com/mintandkiwi/visual-task-brief/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An open Agent Skill that turns long planning documents and completed-delivery notes into concise, numbered, standalone visual HTML.

It is designed for **Codex**, **Claude Code**, and **Kimi Code** from one shared `SKILL.md` package.

## What it creates

- **Before implementation:** a visual task brief with goals, scope, connected flows, milestones, decisions, risks, and acceptance criteria
- **After implementation:** a visual delivery report with actual artifacts, file locations, usage steps, before/after changes, verification evidence, limitations, and handoff status
- A 60-second plain-language summary for both modes
- Connected diagrams, artifact maps, comparison cards, and verification charts
- Clear separation between test passes, manual acceptance, commit/push, deployment, release, and other evidence levels
- Automatic filenames such as `01-task-brief-my-app.html` and `02-delivery-report-my-app.html`
- Responsive, keyboard-accessible, print-friendly HTML with no CDN or network dependency

## Compatibility

The repository follows the open [Agent Skills specification](https://agentskills.io/specification). The core package is identical across clients; only the installation path and explicit invocation syntax differ.

| Client | Personal installation path | Explicit invocation |
|---|---|---|
| Codex | `~/.codex/skills/visual-task-brief/` | `$visual-task-brief` |
| Claude Code | `~/.claude/skills/visual-task-brief/` | `/visual-task-brief` |
| Kimi Code | `~/.config/agents/skills/visual-task-brief/` | `/skill:visual-task-brief` |

All three clients can also select the skill automatically from a matching request such as “create a task brief”, “create a visual delivery report”, or “把已完成的交付内容做成 HTML 图表”.

The optional `agents/openai.yaml` file adds Codex UI metadata. Claude Code and Kimi Code can ignore it safely.

## Install

Python 3.9 or newer is required for the generator and installer.

```bash
git clone https://github.com/mintandkiwi/visual-task-brief.git
cd visual-task-brief
python3 scripts/install.py --targets codex claude kimi
```

On Windows, use `py -3` instead of `python3`:

```powershell
py -3 scripts/install.py --targets codex claude kimi
```

Install only selected clients when needed:

```bash
python3 scripts/install.py --targets codex
python3 scripts/install.py --targets claude kimi
```

The installer refuses to overwrite an existing installation. For an upgrade, pull the repository and use `--force`; the existing directory is renamed to a timestamped backup first.

```bash
git pull
python3 scripts/install.py --targets codex claude kimi --force
```

You may also copy the repository manually to any path in the compatibility table.

## Use

Natural-language invocation:

```text
Create a visual task brief for this application.
Turn the implementation plan into an HTML brief with diagrams and a plain-language glossary.
Create a visual HTML delivery report for the completed work.
请为这个应用出具可视化任务书。
把已完成的交付内容做成可视化 HTML。
```

For a task brief, the agent creates structured JSON and runs:

```bash
python3 "<skill-dir>/scripts/build_task_brief.py" \
  --input "/absolute/path/task-brief.json" \
  --output-dir "/absolute/path/delivery-docs" \
  --project "Readable Project Name"

python3 "<skill-dir>/scripts/check_task_brief.py" \
  "/absolute/path/delivery-docs/01-task-brief-readable-project-name.html"
```

For completed work, the agent creates a separate evidence-grounded delivery JSON and runs:

```bash
python3 "<skill-dir>/scripts/build_delivery_report.py" \
  --input "/absolute/path/delivery-report.json" \
  --output-dir "/absolute/path/delivery-docs" \
  --project "Readable Project Name"

python3 "<skill-dir>/scripts/check_delivery_report.py" \
  "/absolute/path/delivery-docs/02-delivery-report-readable-project-name.html"
```

The generator scans the directory and assigns the next sequence. It refuses silent overwrite, so later visual documents become `03-...`, `04-...`, and so on.

Examples and schemas:

- [Task brief input](examples/example-task-brief.json) and [task content model](references/content-model.md)
- [Delivery report input](examples/example-delivery-report.json) and [delivery content model](references/delivery-content-model.md)

## Design boundaries

- The HTML is a reading view; JSON, source documents, code, and test evidence remain the source of truth.
- The skill never turns a recommendation into an approved requirement.
- Test results, deployment, user acceptance, payment, and other evidence are only marked confirmed when the evidence actually exists.
- Completed-delivery HTML is the primary reading view; Markdown can remain as a detailed source or appendix.
- Numbered files preserve a readable document history and are never silently overwritten.
- Generated HTML is self-contained and does not upload project data.

## Development and validation

```bash
python3 scripts/validate_skill.py .
python3 -m py_compile scripts/*.py
python3 scripts/build_task_brief.py \
  --input examples/example-task-brief.json \
  --output-dir examples/generated \
  --project "Example Project"
python3 scripts/build_delivery_report.py \
  --input examples/example-delivery-report.json \
  --output-dir examples/generated \
  --project "Example Project"
python3 scripts/check_task_brief.py examples/generated/01-task-brief-example-project.html
python3 scripts/check_delivery_report.py examples/generated/02-delivery-report-example-project.html
```

GitHub Actions runs the same checks and verifies isolated installations for all three clients on Linux, macOS, and Windows.

## Official format references

- [Agent Skills specification](https://agentskills.io/specification)
- [Codex customization: skills](https://developers.openai.com/codex/concepts/customization#skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Kimi Code CLI skills](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/customization/skills.md)

## License

[MIT](LICENSE)
