# 可视化任务书与交付成果

简体中文 | [English](README.md)

[![Test](https://github.com/mintandkiwi/visual-task-brief/actions/workflows/test.yml/badge.svg)](https://github.com/mintandkiwi/visual-task-brief/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

一个开放的 Agent Skill，用来把冗长的计划文档和已完成交付说明转换为简明、自动编号、独立运行的可视化 HTML。

同一套 `SKILL.md` 核心包可供 **Codex、Claude Code 和 Kimi Code** 使用。

本次版本已经用新功能生成真实编号交付成果：[01-delivery-report-visual-task-brief-v0-2.html](docs/01-delivery-report-visual-task-brief-v0-2.html)。

## 能生成什么

- **实施前：**生成目标、范围、流程连线、阶段、决策、风险和验收标准组成的可视化任务书
- **实施后：**生成实际交付物、文件位置、使用步骤、前后变化、验证证据、限制和交接状态组成的可视化交付成果页
- 两种模式都提供 60 秒人话摘要
- 使用连接图、交付地图、前后对比卡和验证图表表达关系
- 严格区分测试通过、人工验收、提交推送、部署、发布等不同证据层级
- 自动生成 `01-task-brief-my-app.html`、`02-delivery-report-my-app.html` 等文件名
- 无 CDN、无需联网、支持响应式、键盘操作和打印的 HTML

## 兼容性

本仓库遵循开放的 [Agent Skills 规范](https://agentskills.io/specification)。三端使用完全相同的核心包，只有安装目录和显式调用方式不同。

| 客户端 | 个人级安装目录 | 显式调用方式 |
|---|---|---|
| Codex | `~/.codex/skills/visual-task-brief/` | `$visual-task-brief` |
| Claude Code | `~/.claude/skills/visual-task-brief/` | `/visual-task-brief` |
| Kimi Code | `~/.config/agents/skills/visual-task-brief/` | `/skill:visual-task-brief` |

三端也能根据“出具任务书”“生成可视化交付报告”“把已完成内容做成 HTML 图表”等自然语言请求自动选择此 Skill。

可选的 `agents/openai.yaml` 用于补充 Codex 界面元数据；Claude Code 和 Kimi Code 可以安全忽略它。

## 安装

生成器和安装器需要 Python 3.9 或更高版本。

```bash
git clone https://github.com/mintandkiwi/visual-task-brief.git
cd visual-task-brief
python3 scripts/install.py --targets codex claude kimi
```

Windows 使用 `py -3`：

```powershell
py -3 scripts/install.py --targets codex claude kimi
```

也可以只安装到指定客户端：

```bash
python3 scripts/install.py --targets codex
python3 scripts/install.py --targets claude kimi
```

安装器默认拒绝覆盖已有目录。升级时先拉取新版本，再使用 `--force`；旧目录会先被重命名为带时间戳的备份。

```bash
git pull
python3 scripts/install.py --targets codex claude kimi --force
```

你也可以将本仓库手动复制到兼容性表格列出的任一目录。

## 使用

自然语言调用示例：

```text
请为这个应用出具可视化任务书。
把这份实施计划转换成带流程图、思维导图和术语解释的 HTML。
把已完成的交付内容制作成可视化 HTML，并列出文件和验证证据。
Create a visual task brief for this application.
Create a visual HTML delivery report for the completed work.
```

生成任务书时，Agent 会先创建结构化 JSON，再运行：

```bash
python3 "<skill-dir>/scripts/build_task_brief.py" \
  --input "/absolute/path/task-brief.json" \
  --output-dir "/absolute/path/delivery-docs" \
  --project "Readable Project Name"

python3 "<skill-dir>/scripts/check_task_brief.py" \
  "/absolute/path/delivery-docs/01-task-brief-readable-project-name.html"
```

完成应用交付后，Agent 会创建单独的、以实际证据为依据的交付 JSON，再运行：

```bash
python3 "<skill-dir>/scripts/build_delivery_report.py" \
  --input "/absolute/path/delivery-report.json" \
  --output-dir "/absolute/path/delivery-docs" \
  --project "Readable Project Name"

python3 "<skill-dir>/scripts/check_delivery_report.py" \
  "/absolute/path/delivery-docs/02-delivery-report-readable-project-name.html"
```

生成器会扫描目录并分配下一个编号，同时拒绝静默覆盖；后续文档会继续使用 `03-...`、`04-...`。

示例和字段模型：

- [任务书输入示例](examples/example-task-brief.json)及[任务书字段模型](references/content-model.md)
- [交付成果输入示例](examples/example-delivery-report.json)及[交付成果字段模型](references/delivery-content-model.md)

## 设计边界

- HTML 是便于阅读的视图；JSON、原始文档、代码和测试证据仍然是事实来源。
- Skill 不会把“建议”自动写成“已批准需求”。
- 测试、部署、用户验收、付款等状态只有在真实证据存在时才标记为“已确认”。
- 完成后的交付 HTML 是主要阅读视图；Markdown 可以继续作为详细源文件或附件。
- 编号文件保留可追溯的阅读顺序，不会被静默覆盖。
- 生成的 HTML 完全离线，不会上传项目数据。

## 开发与验证

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

GitHub Actions 会在 Linux、macOS 和 Windows 上执行相同检查，并在隔离目录中验证三种客户端安装路径。

## 官方格式资料

- [Agent Skills 规范](https://agentskills.io/specification)
- [Codex 自定义：Skills](https://developers.openai.com/codex/concepts/customization#skills)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Kimi Code CLI Skills](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/zh/customization/skills.md)

## 许可证

[MIT](LICENSE)
