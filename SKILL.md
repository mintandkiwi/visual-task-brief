---
name: visual-task-brief
description: Create concise, self-contained visual HTML task briefs from application plans, project requirements, implementation task books, PRDs, build plans, or existing long-form task documents. Use whenever the user asks to 出具任务书, 写任务书, 应用开发任务书, 可视化任务书, 图文任务书, 项目任务说明, implementation brief, build brief, visual plan, or asks to turn a technical plan into diagrams, connected flows, a mind map, and plain-language terminology explanations. Always use for task-book requests unless the user explicitly requests text-only output.
---

# Visual Task Brief

Turn a dense implementation task into an HTML brief that a non-specialist can understand in about 60 seconds, while preserving expandable detail for execution.

## Output contract

Always deliver a standalone `.html` file that:

- Opens locally without a build step, network connection, CDN, external font, or third-party JavaScript.
- Leads with goal, audience, deliverable, and success criteria.
- Shows the main dependency or user flow with connected nodes.
- Shows scope or architecture as a compact mind map.
- Explains unfamiliar terms in plain language and states why each matters.
- Distinguishes `已确认`, `建议`, `待决定`, and `有风险` in text as well as color.
- Uses progressive disclosure so the first screen remains scannable.
- Prints cleanly to PDF and works at 375, 768, 1024, and 1440 px widths.

If the user also needs an exhaustive Markdown task book, retain it as a source artifact and produce the HTML as the primary reading view. Do not force the full technical detail onto the first screen.

## Workflow

1. Inspect the request, repository, and any existing task document. Do not invent completed work, approvals, validation, dates, owners, or metrics.
2. Separate facts into confirmed information, recommendations, pending decisions, and risks.
3. Read [references/content-model.md](references/content-model.md), then create a UTF-8 JSON input that follows it.
4. Keep the summary readable without specialist knowledge. Put implementation detail in phases, acceptance evidence, glossary entries, or expandable cards.
5. Include 5–12 glossary entries when specialist terms appear. Explain each term in one plain-language sentence and add a short “why it matters” note.
6. Use 3–7 nodes for the main flow and 3–6 branches for the mind map. Merge low-value nodes instead of creating a wall of boxes.
7. Resolve `<skill-dir>` to the directory containing this `SKILL.md`, then build the HTML. On POSIX systems run:

   ```bash
   python3 "<skill-dir>/scripts/build_task_brief.py" \
     --input "/absolute/path/task-brief.json" \
     --output "/absolute/path/task-brief.html"
   ```

   On Windows, use `py -3` instead of `python3` and native absolute paths.

8. Run the deterministic checker from the same resolved directory:

   ```bash
   python3 "<skill-dir>/scripts/check_task_brief.py" \
     "/absolute/path/task-brief.html"
   ```

9. Visually inspect the result when browser tooling is available. Check the first screen, all connector lines, 375 px mobile layout, keyboard focus, expanded glossary, and print preview. Repair any overflow, overlap, clipping, or unreadable contrast before delivery.
10. Return clickable links to the HTML and its JSON source. State validation accurately; distinguish structural checks from visual inspection and user acceptance.

## Writing rules

- Write for the user's stated knowledge level; otherwise assume an intelligent reader without software-engineering training.
- Prefer concrete verbs and outcomes: “保存项目数据” instead of “实现持久化层”.
- Put the plain-language explanation before an acronym.
- Express acceptance as observable evidence, not vague adjectives.
- Keep each card to one idea and each bullet to one sentence.
- Label uncertain content explicitly. Never present a recommendation as approved scope.
- Do not use emoji as structural icons. Use the inline SVG icons already included in the template.
- Do not add external assets unless the user explicitly asks for them.

## Bundled resources

- `assets/task-brief-template.html`: offline, responsive, accessible HTML renderer.
- `examples/example-task-brief.json`: complete input fixture and authoring example.
- `references/content-model.md`: JSON content contract and authoring guidance.
- `scripts/build_task_brief.py`: validate input and embed it safely into the template.
- `scripts/check_task_brief.py`: verify standalone structure and required visual sections.

## Client compatibility

Follow the same workflow in Codex, Claude Code, and Kimi Code. Do not assume a client-specific home directory; always derive resource paths from the active `SKILL.md`. Invocation syntax may differ:

- Codex: mention the skill by name or use `$visual-task-brief` when explicit invocation is supported.
- Claude Code: use `/visual-task-brief` or a matching natural-language request.
- Kimi Code: use `/skill:visual-task-brief` or a matching natural-language request.
