# 可视化任务书

简体中文 | [English](README.md)

[![Test](https://github.com/mintandkiwi/visual-task-brief/actions/workflows/test.yml/badge.svg)](https://github.com/mintandkiwi/visual-task-brief/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

一个开放的 Agent Skill，用来把冗长的应用任务书、PRD 和实施计划转换为简明、独立运行的可视化 HTML。

同一套 `SKILL.md` 核心包可供 **Codex、Claude Code 和 Kimi Code** 使用。

## 能生成什么

- 60 秒摘要：目标、用户、交付物和成功标准
- 带连接线的主流程图
- 紧凑的范围或架构思维导图
- 本次包含和暂不包含的范围
- 分阶段交付路线及可观察结果
- 专业术语的人话解释
- 明确区分已确认、建议、待决定和风险
- 无 CDN、无需联网、支持响应式、键盘操作和打印的 HTML

## 兼容性

本仓库遵循开放的 [Agent Skills 规范](https://agentskills.io/specification)。三端使用完全相同的核心包，只有安装目录和显式调用方式不同。

| 客户端 | 个人级安装目录 | 显式调用方式 |
|---|---|---|
| Codex | `~/.codex/skills/visual-task-brief/` | `$visual-task-brief` |
| Claude Code | `~/.claude/skills/visual-task-brief/` | `/visual-task-brief` |
| Kimi Code | `~/.config/agents/skills/visual-task-brief/` | `/skill:visual-task-brief` |

三端也能根据“出具任务书”“把实施计划做成图文 HTML”等自然语言请求自动选择此 Skill。

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
Create a visual task brief for this application.
```

Agent 会先创建结构化 JSON 源文件，再运行：

```bash
python3 "<skill-dir>/scripts/build_task_brief.py" \
  --input "/absolute/path/task-brief.json" \
  --output "/absolute/path/task-brief.html"

python3 "<skill-dir>/scripts/check_task_brief.py" \
  "/absolute/path/task-brief.html"
```

完整输入示例见 [examples/example-task-brief.json](examples/example-task-brief.json)，字段约定见 [references/content-model.md](references/content-model.md)。

## 设计边界

- HTML 是便于阅读的视图；JSON、原始文档、代码和测试证据仍然是事实来源。
- Skill 不会把“建议”自动写成“已批准需求”。
- 测试、部署、用户验收、付款等状态只有在真实证据存在时才标记为“已确认”。
- 生成的 HTML 完全离线，不会上传项目数据。

## 开发与验证

```bash
python3 scripts/validate_skill.py .
python3 -m py_compile scripts/*.py
python3 scripts/build_task_brief.py \
  --input examples/example-task-brief.json \
  --output examples/example-task-brief.html
python3 scripts/check_task_brief.py examples/example-task-brief.html
```

GitHub Actions 会在 Linux、macOS 和 Windows 上执行相同检查，并在隔离目录中验证三种客户端安装路径。

## 官方格式资料

- [Agent Skills 规范](https://agentskills.io/specification)
- [Codex 自定义：Skills](https://developers.openai.com/codex/concepts/customization#skills)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Kimi Code CLI Skills](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/zh/customization/skills.md)

## 许可证

[MIT](LICENSE)
