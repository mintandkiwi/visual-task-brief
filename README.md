# Visual Task Brief

[简体中文](README.zh-CN.md) | English

[![Test](https://github.com/mintandkiwi/visual-task-brief/actions/workflows/test.yml/badge.svg)](https://github.com/mintandkiwi/visual-task-brief/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An open Agent Skill that turns long application task documents, PRDs, and implementation plans into concise, standalone visual HTML briefs.

It is designed for **Codex**, **Claude Code**, and **Kimi Code** from one shared `SKILL.md` package.

## What it creates

- A 60-second summary: goal, user, deliverable, and success criteria
- Connected process diagrams
- A compact scope or architecture mind map
- Included and excluded scope
- Delivery phases and observable outcomes
- Plain-language explanations for technical terms
- Separate labels for confirmed facts, recommendations, pending decisions, and risks
- Responsive, keyboard-accessible, print-friendly HTML with no CDN or network dependency

## Compatibility

The repository follows the open [Agent Skills specification](https://agentskills.io/specification). The core package is identical across clients; only the installation path and explicit invocation syntax differ.

| Client | Personal installation path | Explicit invocation |
|---|---|---|
| Codex | `~/.codex/skills/visual-task-brief/` | `$visual-task-brief` |
| Claude Code | `~/.claude/skills/visual-task-brief/` | `/visual-task-brief` |
| Kimi Code | `~/.config/agents/skills/visual-task-brief/` | `/skill:visual-task-brief` |

All three clients can also select the skill automatically from a matching request such as “create a task brief” or “把这个应用任务书做成图文 HTML”.

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
请为这个应用出具可视化任务书。
```

The agent creates a structured JSON source and then runs:

```bash
python3 "<skill-dir>/scripts/build_task_brief.py" \
  --input "/absolute/path/task-brief.json" \
  --output "/absolute/path/task-brief.html"

python3 "<skill-dir>/scripts/check_task_brief.py" \
  "/absolute/path/task-brief.html"
```

See [examples/example-task-brief.json](examples/example-task-brief.json) for a complete input and [references/content-model.md](references/content-model.md) for the field contract.

## Design boundaries

- The HTML is a reading view; JSON, source documents, code, and test evidence remain the source of truth.
- The skill never turns a recommendation into an approved requirement.
- Test results, deployment, user acceptance, payment, and other evidence are only marked confirmed when the evidence actually exists.
- Generated HTML is self-contained and does not upload project data.

## Development and validation

```bash
python3 scripts/validate_skill.py .
python3 -m py_compile scripts/*.py
python3 scripts/build_task_brief.py \
  --input examples/example-task-brief.json \
  --output examples/example-task-brief.html
python3 scripts/check_task_brief.py examples/example-task-brief.html
```

GitHub Actions runs the same checks and verifies isolated installations for all three clients on Linux, macOS, and Windows.

## Official format references

- [Agent Skills specification](https://agentskills.io/specification)
- [Codex customization: skills](https://developers.openai.com/codex/concepts/customization#skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Kimi Code CLI skills](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/customization/skills.md)

## License

[MIT](LICENSE)
