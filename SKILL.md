---
name: visual-task-brief
description: Create concise, self-contained visual HTML task briefs and completed-delivery reports from application plans, project requirements, PRDs, build plans, implementation results, handoff notes, release summaries, or long Markdown documents. Use whenever the user asks to 出具任务书, 写任务书, 可视化任务书, 图文任务书, 项目任务说明, 交付书, 交付报告, 交付成果, 完成总结, 可视化交付, implementation brief, build brief, delivery report, handoff report, release summary, or asks to turn technical planning or completed work into numbered diagrams, connected flows, artifact maps, verification charts, and plain-language terminology. Always use for task-book and completed-delivery requests unless the user explicitly requests text-only output.
---

# Visual Task Brief

Turn dense planning and delivery information into numbered standalone HTML that a non-specialist can understand quickly.

## Choose the document mode

- Use **task brief** before implementation or when scope, milestones, architecture, decisions, risks, and acceptance criteria are being planned.
- Use **delivery report** after implementation or when explaining completed work, artifacts, usage, verification evidence, remaining boundaries, or handoff status.
- When one task includes both planning and implementation, create the task brief first and the delivery report after the work is actually complete.
- Produce a delivery report automatically for completed application work unless the user explicitly requests text-only delivery.

## Shared output contract

Always deliver a standalone `.html` file that:

- Opens locally without a build step, network connection, CDN, external font, or third-party JavaScript.
- Uses a mandatory sequence and readable name: `NN-document-type-project-name.html`.
- Uses the next available sequence in the chosen output directory instead of overwriting an earlier document.
- Leads with a 60-second plain-language summary.
- Uses connected flows, maps, comparison cards, or verification charts only where relationships benefit from visualization.
- Explains unfamiliar terms briefly.
- Uses text labels as well as color for status.
- Prints cleanly and works at 375, 768, 1024, and 1440 px widths.

Store the JSON source beside the HTML when practical. Treat Markdown as an optional detailed source or appendix; link the HTML first in the final response.

## Task brief workflow

1. Inspect the request, repository, and any existing task document. Do not invent approvals, dates, owners, metrics, or completed work.
2. Separate confirmed information, recommendations, pending decisions, and risks.
3. Read [references/content-model.md](references/content-model.md) and use [examples/example-task-brief.json](examples/example-task-brief.json) as the direct example.
4. Create the JSON source, then resolve `<skill-dir>` to the directory containing this `SKILL.md`.
5. Generate an automatically numbered HTML:

   ```bash
   python3 "<skill-dir>/scripts/build_task_brief.py" \
     --input "/absolute/path/task-brief.json" \
     --output-dir "/absolute/path/delivery-docs" \
     --project "Readable Project Name"
   ```

6. Run `scripts/check_task_brief.py` on the generated file.

## Delivery report workflow

1. Inspect the actual delivered files, code changes, executed checks, logs, build artifacts, commits, and deployment state.
2. Keep automated tests, static checks, manual inspection, user acceptance, commit/push, deployment, and release as separate evidence levels.
3. Read [references/delivery-content-model.md](references/delivery-content-model.md) and use [examples/example-delivery-report.json](examples/example-delivery-report.json) as the direct example.
4. Do not mark an item `confirmed` or `passed` without a real artifact or evidence statement. Use `partial`, `pending`, `manual`, `not-run`, or `risk` when appropriate.
5. Create the JSON source and generate the next numbered HTML in the same document directory:

   ```bash
   python3 "<skill-dir>/scripts/build_delivery_report.py" \
     --input "/absolute/path/delivery-report.json" \
     --output-dir "/absolute/path/delivery-docs" \
     --project "Readable Project Name"
   ```

6. Run `scripts/check_delivery_report.py` on the generated file.
7. Ensure the delivery report shows what was delivered, where files are, how to use them, what changed, which verification ran, and what remains unresolved.

On Windows, use `py -3` instead of `python3` and native absolute paths.

## Numbering and naming rules

- Use `01-task-brief-project-name.html` for the first planning document when the directory is empty.
- Use `02-delivery-report-project-name.html` for the following completed-delivery view.
- Continue with `03-...`, `04-...`, and so on for later revisions or additional visual documents.
- Let the generator scan the directory and assign the next sequence. Use `--sequence` only when the user explicitly requires a fixed number.
- Refuse silent overwrite. Preserve earlier numbered files as a readable history.
- Give non-HTML deliverables their own reader-facing indexes inside the delivery report.

## Writing and evidence rules

- Write for an intelligent reader without assumed software-engineering knowledge.
- Prefer concrete outcomes: “可以导入并搜索文件” instead of “实现持久化与检索层”.
- Express acceptance and verification as observable evidence.
- Keep each card to one idea and each item to one sentence where possible.
- Never turn a candidate, recommendation, test pass, or build artifact into user acceptance, deployment, release, or business validation.
- Do not use emoji as structural icons. Use the inline SVG assets in the templates.
- Do not add external resources unless the user explicitly asks.

## Validation and handoff

Visually inspect the generated page when browser tooling is available. Check first-screen readability, connector lines, mobile layout, keyboard focus, expandable glossary, file paths, and print preview. Repair overflow, overlap, clipping, or weak contrast.

Return clickable links in this order:

1. Numbered HTML visual document
2. JSON source
3. Optional Markdown detail or other artifacts

State validation accurately and keep user acceptance separate.

## Client compatibility

Use the same resources and workflow in Codex, Claude Code, and Kimi Code. Always derive resource paths from the active `SKILL.md`.

- Codex: mention the skill or use `$visual-task-brief` when explicit invocation is supported.
- Claude Code: use `/visual-task-brief` or a matching natural-language request.
- Kimi Code: use `/skill:visual-task-brief` or a matching natural-language request.
