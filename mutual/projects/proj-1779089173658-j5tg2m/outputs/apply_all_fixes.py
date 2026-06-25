# -*- coding: utf-8 -*-
"""Complete niuma-engine v4.0 fix: CLAUDE.md + README + adapters + docs + templates."""
import os

REPO = r"C:\Users\13975\AppData\Local\Temp\niuma-engine"

# ============================================================
# P0.1: Create CLAUDE.md — adapted from mutual workspace, generic version
# ============================================================
CLAUDE_MD = """# Startup Sequence (Every Conversation — Mandatory)

| Step | Action | When |
|------|--------|------|
| 1 | Read `.claude/rules/` directory | Every conversation (Claude Code auto-loads) |
| 2 | Read `memory/long-term.md` | First conversation / after corrections |
| 3 | Read `memory/{today}.md` | First conversation of the day |
| 4 | Read `EVOLUTION.md` | Match pending tasks -> execute first |

> **Quick Mode**: If the user message contains a specific trigger word you've defined, skip startup and process directly. High-risk operations still require reading long-term.md.

---

# Project Rules

## Think Before Act
New problems require research before action. Never substitute "I think" for best practice.
-> See `.claude/rules/think-before-act.md`

## No Blind Overwrite (CRITICAL)
Read existing files before writing. Use Edit for partial changes, never Write without Read.
-> See `.claude/rules/no-blind-overwrite.md`

## Script Safety Check (CRITICAL)
Pipeline: write script -> safety check -> dry-run -> show -> confirm -> execute -> verify.
Deletions must target specific files, never directories.
-> See `.claude/rules/script-safety-check.md`

## Evidence Layering
Every "pass" claim must carry a calibration label (coarse/medium/full-audit).
-> See `.claude/rules/10-engineering-laws.md` Law 1

## Anti-Illusion Audit
Abnormally good numbers are assumed fake until proven real. Run the five-question check.
-> See `.claude/rules/anti-illusion-audit.md`

## Negative Result Archiving
Dead ends must be archived. An unrecorded dead end will be retried by every subsequent conversation.
-> See `.claude/rules/negative-results.md`

## Agent Prompt Iron Law
Every Agent call must include: specific goal + output format + stop condition.
-> See `.claude/rules/agent-prompt-ironclad.md`

## Agent Concurrency Fallback
When 429 rate limit hits: immediately fall back to sequential direct tool calls. Do not wait. Do not retry.
-> See `.claude/rules/agent-concurrency-fallback.md`

## Sub-Agent Strategy
Use sub-agents for investigation tasks, not decision tasks. Single agent first, scale only when needed.
-> See `.claude/rules/subagent-strategy.md`

## Search Decision Tree
Before searching: is this an immutable fact? A changing state? An unknown entity? Match search depth to question complexity.
-> See `.claude/rules/search-decision-tree.md`

## Lesson Auto-Update
User corrections must trigger workflow updates. Lessons recorded but not applied = wasted.
-> See `.claude/rules/lesson-auto-update.md`

## Boundary Declaration
Every deliverable must include a three-column boundary list: confirmed / reference-only / cannot claim.
-> See `.claude/rules/boundary-declaration.md`

## Git Checkpoint & Recovery
Commit a checkpoint before any file deletion. Recovery must be possible within 30 seconds.
-> See `.claude/rules/git-recovery.md`

---

# Compact Instructions

## Protection List (Never Drop During Compression)
1. User's latest request (verbatim)
2. All modified file absolute paths
3. Source: path#line citations
4. Key decisions and rationale
5. Error root causes and fixes
6. Task progress and next steps
7. User correction verbatim

## After Compression Recovery
1. Re-read CLAUDE.md + .claude/rules/ (automatic)
2. Actively re-read memory/long-term.md + memory/{today}.md
3. Check for unfinished tasks

---

# Rule Categories at a Glance

| Category | Rules | Purpose |
|----------|-------|---------|
| Core Engineering Laws | 10-engineering-laws, lifecycle-sop | Foundation — always active |
| Agent Management | agent-prompt-ironclad, subagent-strategy, agent-concurrency-fallback | Multi-agent coordination |
| Search & Info | search-decision-tree, lesson-auto-update, anti-info-overload | Information discipline |
| Safety & Ops | script-safety-check, no-blind-overwrite, chinese-path-safety, powershell-safety, pre-action-check, git-recovery, mcp-config-protocol | Prevention of known accidents |
| Memory & Quality | memory-candidate-protocol, memory-confidence, negative-results, anti-illusion-audit, boundary-declaration | Truth maintenance |
| Architecture | competition-workspace-architecture, dual-write-protocol, no-root-rules-dir | Project structure discipline |
| Skill Ecosystem | skill-auto-activation, skill-route-enforcement, skill-execution-discipline, skill-logging-enforcement | If you use skills/plugins |

---

> This framework is alive. Rules grow from real accidents. Each rule blocks one confirmed failure pattern.
> You are looking at a snapshot. The framework updates as new patterns are recognized in production.
"""

with open(os.path.join(REPO, "CLAUDE.md"), "w", encoding="utf-8") as f:
    f.write(CLAUDE_MD)
print("[OK] CLAUDE.md created")

# ============================================================
# P0.2: Fix .gitignore — remove CLAUDE.md from exclusions
# ============================================================
gitignore_path = os.path.join(REPO, ".gitignore")
with open(gitignore_path, encoding="utf-8") as f:
    gi = f.read()

# Remove CLAUDE.md from exclusion list
gi = gi.replace("CLAUDE.md\n.claude/*", ".claude/*")
# Also add explicit allow for CLAUDE.md and EVOLUTION.md
gi = gi.replace(
    "# === AI 工作区（禁止上传） ===",
    "# === AI 工作区（禁止上传） ===\n!CLAUDE.md\n!EVOLUTION.md"
)

with open(gitignore_path, "w", encoding="utf-8") as f:
    f.write(gi)
print("[OK] .gitignore: CLAUDE.md now allowed")

# ============================================================
# P0.3: Fix README law-10 dead reference + remove voice-dna from evolution log
# ============================================================
readme_path = os.path.join(REPO, "README.md")
with open(readme_path, encoding="utf-8") as f:
    readme = f.read()

# Fix 1: "法则 10 + 身份一致性" -> "法则 10 + 纪律框架"
readme = readme.replace(
    "| 每次对话 AI 的表现都不一样 | 法则 10 + 身份一致性 |",
    "| 每次对话 AI 的表现都不一样 | 法则 10 + 纪律框架（规则一致性） |"
)

# Fix 2: Remove "文风DNA自动注入" evolution entry (deleted rule, internal only)
voice_dna_line = "| 2026-06-15 | AI写作风格与用户不一致 | 文风DNA自动注入 (写作默认用用户风格) |\n"
if voice_dna_line in readme:
    readme = readme.replace(voice_dna_line, "")
    print("[OK] README: removed voice-dna from evolution log")

# Fix 3: Clarify "10条工程法则" framing in section header
readme = readme.replace(
    "## 10 条工程法则——它们是怎么连起来的",
    "## 10 条核心工程法则——它们是怎么连起来的"
)

# Fix 4: Add note about the full rule set
readme = readme.replace(
    "**这 10 条不是 10 个独立技巧，是一条流水线上的 10 个检查点。**",
    "**这 10 条是核心法则，是一条流水线上的 10 个检查点。** 仓库共包含 29 条规则——10 条核心法则贯穿全流程，其余 19 条是针对特定场景（Agent 管理、Skill 治理、安全运维等）的专项纪律。"
)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(readme)
print("[OK] README: law-10 fixed, voice-dna removed, 10-vs-29 clarified")

# ============================================================
# P1: Update all adapters to reference full rule directory
# ============================================================
print("\n=== Updating adapters ===")

# aider.md — update to reference directory, not 5 individual files
aider_content = """# Aider Adapter

## Integration Method

Aider uses `.aider.conf.yml` or command-line arguments to load context.

### Quick Integration (Recommended)

Add the entire rules directory as read-only context:

```yaml
# .aider.conf.yml
read:
  - CLAUDE.md
  - .claude/rules/10-engineering-laws.md
  - .claude/rules/lifecycle-sop.md
  - .claude/rules/think-before-act.md
  - .claude/rules/anti-illusion-audit.md
  - .claude/rules/negative-results.md
  - .claude/rules/no-blind-overwrite.md
  - .claude/rules/script-safety-check.md
  - .claude/rules/anti-info-overload.md
  - .claude/rules/boundary-declaration.md
  - .claude/rules/memory-candidate-protocol.md
  - .claude/rules/memory-confidence.md
  - .claude/rules/agent-prompt-ironclad.md
  - .claude/rules/agent-concurrency-fallback.md
  - .claude/rules/subagent-strategy.md
  - .claude/rules/search-decision-tree.md
  - .claude/rules/lesson-auto-update.md
  - .claude/rules/git-recovery.md
  - .claude/rules/chinese-path-safety.md
  - .claude/rules/powershell-safety.md
  - .claude/rules/pre-action-check.md
  - .claude/rules/mcp-config-protocol.md
```

### Minimal Install (pick by pain point)

```yaml
# Core only
read:
  - CLAUDE.md
  - .claude/rules/10-engineering-laws.md
  - .claude/rules/lifecycle-sop.md
  - .claude/rules/think-before-act.md
  - .claude/rules/no-blind-overwrite.md
  - .claude/rules/script-safety-check.md
```

### Notes
- Aider's `--read` files are read-only context
- Memory files (memory/) are managed separately
- Full rule list: 29 files in `.claude/rules/`
"""
with open(os.path.join(REPO, "adapters", "aider.md"), "w", encoding="utf-8") as f:
    f.write(aider_content)
print("[OK] adapters/aider.md")

# codex.md — update
codex_content = """# Codex Adapter

## Integration Method

Codex uses `AGENTS.md` as its root guide.

### Quick Integration

1. Create `AGENTS.md` in the project root, referencing the full rule set:

```markdown
> Engineering framework: This project uses niuma-engine v4.0 (29 rules).
> All rule files are in the .claude/rules/ directory.
> See CLAUDE.md for the startup sequence and core principles.
```

2. Append rule references to `AGENTS.md`:

```markdown
## Engineering Rules (niuma-engine v4.0)
- Core: .claude/rules/10-engineering-laws.md (10 cross-cutting laws)
- Lifecycle: .claude/rules/lifecycle-sop.md (6-stage project lifecycle)
- Audit: .claude/rules/anti-illusion-audit.md (anti-illusion five questions)
- Archive: .claude/rules/negative-results.md (dead end archiving)
- Safety: .claude/rules/script-safety-check.md + no-blind-overwrite.md
- Agents: .claude/rules/agent-prompt-ironclad.md + subagent-strategy.md + agent-concurrency-fallback.md
- Search: .claude/rules/search-decision-tree.md + lesson-auto-update.md
- Full set: 29 rules in .claude/rules/
```

### Notes
- Codex does not auto-load `.claude/rules/` — must be referenced in `AGENTS.md`
- All critical rules should have references in `AGENTS.md`
- Total: 29 rule files, ~124KB of engineering discipline
"""
with open(os.path.join(REPO, "adapters", "codex.md"), "w", encoding="utf-8") as f:
    f.write(codex_content)
print("[OK] adapters/codex.md")

# cursor.md — update
cursor_content = """# Cursor Adapter

## Integration Method

Cursor loads `.md` files under `.cursor/rules/` as project rules.

### Quick Integration

```bash
# Option 1: Symlink (recommended — auto-syncs)
mkdir -p .cursor/rules
ln -s ../../.claude/rules/* .cursor/rules/
ln -s ../../CLAUDE.md .cursor/rules/niuma-engine-entry.md

# Option 2: Copy (one-time)
cp .claude/rules/* .cursor/rules/
cp CLAUDE.md .cursor/rules/niuma-engine-entry.md
```

### Rule Loading
Cursor loads all `.md` files under `.cursor/rules/` as project rules. With niuma-engine v4.0, this means all 29 rules are active.

### Minimal Install
Not every project needs all 29 rules. Pick by pain point:
- Copy only the rules matching your current problems
- See README.md "按痛点安装" section for guidance

### Notes
- Symlinks keep rules in sync when you `git pull` updates
- Memory file paths (memory/) are unchanged
"""
with open(os.path.join(REPO, "adapters", "cursor.md"), "w", encoding="utf-8") as f:
    f.write(cursor_content)
print("[OK] adapters/cursor.md")

# gemini-cli.md — update
gemini_content = """# Gemini CLI Adapter

## Integration Method

Gemini CLI discovers `.md` files in the project root as context.

### Quick Integration

1. Create `GEMINI.md` in project root:

```markdown
> Engineering framework: niuma-engine v4.0 (29 rules).
> Rule files are in .claude/rules/ — 10 core laws + 19 specialized rules.
> See CLAUDE.md for the startup sequence and core principles.

## Key Rules (summary)
- Evidence Layering: every "pass" must carry a calibration label
- Anti-Illusion Audit: high scores first audit how they were produced
- Negative Result Archive: dead ends must be archived
- Agent Prompt Iron Law: specific goal + output format + stop condition
- Agent Concurrency Fallback: 429 rate limit -> immediate sequential mode
```

2. Gemini CLI automatically discovers `GEMINI.md` as context.

### Notes
- Gemini CLI's context discovery is loose — inline the most critical rules in GEMINI.md
- Full rule set: 29 files in `.claude/rules/` (~124KB total)
"""
with open(os.path.join(REPO, "adapters", "gemini-cli.md"), "w", encoding="utf-8") as f:
    f.write(gemini_content)
print("[OK] adapters/gemini-cli.md")

# ============================================================
# P1: Update docs/compatibility.md
# ============================================================
compat_content = """# Agent Compatibility

| Agent | Integration Method | Auto Load | Rule Count | Status |
|-------|-------------------|-----------|------------|--------|
| Claude Code | `.claude/rules/` | Automatic | 29 rules | Primary Target |
| Codex | `AGENTS.md` bridge | Automatic | Configurable | Supported |
| Cursor | `.cursor/rules` | Automatic | 29 rules (symlink) | Supported |
| Aider | `.aider.conf.yml` | Manual | Configurable | Supported |
| Gemini CLI | `GEMINI.md` | Automatic | Configurable | Supported |

## Rule Loading Priority

Universal across all agents:
1. User direct instructions (highest priority)
2. Project root guide (CLAUDE.md / AGENTS.md / GEMINI.md)
3. Rule files (.claude/rules/) — 29 files, ~124KB
4. Agent default behavior (lowest priority)

## Rule Categories

| Category | Count | Key Files |
|----------|-------|-----------|
| Core Engineering Laws | 2 | 10-engineering-laws, lifecycle-sop |
| Agent Management | 3 | agent-prompt-ironclad, subagent-strategy, agent-concurrency-fallback |
| Search & Info Discipline | 3 | search-decision-tree, lesson-auto-update, anti-info-overload |
| Safety & Operations | 7 | script-safety-check, no-blind-overwrite, chinese-path-safety, powershell-safety, pre-action-check, git-recovery, mcp-config-protocol |
| Memory & Quality | 5 | memory-candidate-protocol, memory-confidence, negative-results, anti-illusion-audit, boundary-declaration |
| Architecture & Governance | 5 | competition-workspace-architecture, dual-write-protocol, no-root-rules-dir, _MIGRATED-TO-RULES |
| Skill Ecosystem | 4 | skill-auto-activation, skill-route-enforcement, skill-execution-discipline, skill-logging-enforcement |

## Memory System Compatibility

niuma-engine's memory system is based on Markdown files. All agents can read/write `.md` files under `memory/`.
"""
with open(os.path.join(REPO, "docs", "compatibility.md"), "w", encoding="utf-8") as f:
    f.write(compat_content)
print("[OK] docs/compatibility.md")

# ============================================================
# P1: Update docs/agent-install.md
# ============================================================
install_content = """# Agent Installation Guide

## Automatic Installation (Recommended)

Clone the repo, then tell your AI agent:

```
Read CLAUDE.md and the .claude/rules/ directory.
Help me integrate niuma-engine into this project.
Show me the installation plan. Do not overwrite anything without my approval.
```

The AI will:
1. Read the startup sequence in CLAUDE.md
2. Load all 29 rules from .claude/rules/
3. Check for existing memory files
4. Propose an integration plan

## Manual Installation

### Claude Code (Primary Target)
```bash
git clone https://github.com/Destined-at-Dawn/niuma-engine.git
cp -r niuma-engine/.claude/rules/ your-project/.claude/rules/
cp niuma-engine/CLAUDE.md your-project/CLAUDE.md
cp -r niuma-engine/templates/zh-CN/ your-project/memory/
```

### Other Agents
See the corresponding adapter file:
- Codex: `adapters/codex.md`
- Cursor: `adapters/cursor.md`
- Aider: `adapters/aider.md`
- Gemini CLI: `adapters/gemini-cli.md`

## Pick by Pain Point

You don't need all 29 rules. Copy only what matches your problems:

| Pain Point | Install These |
|------------|--------------|
| AI numbers untrustworthy | anti-illusion-audit.md |
| AI says "done" but quality poor | 10-engineering-laws.md + lifecycle-sop.md |
| Same pitfall keeps recurring | negative-results.md |
| AI output too verbose | anti-info-overload.md |
| Script almost deleted wrong thing | script-safety-check.md |
| AI silently overwrites files | no-blind-overwrite.md |
| Multi-agent coordination chaos | agent-prompt-ironclad + subagent-strategy + agent-concurrency-fallback |
| Full discipline system | All 29 rules in .claude/rules/ |

## Post-Installation Verification

1. Start a new conversation
2. Ask: "What is evidence layering?" — AI should reference Law 1
3. Give the AI an abnormally good number — it should trigger an anti-illusion audit
4. Ask: "What rules are active?" — it should list rules from .claude/rules/
"""
with open(os.path.join(REPO, "docs", "agent-install.md"), "w", encoding="utf-8") as f:
    f.write(install_content)
print("[OK] docs/agent-install.md")

# ============================================================
# P2: Create EVOLUTION.md — lightweight evolution calendar
# ============================================================
evolution_content = """# Evolution Calendar

> Rules grow from accidents. This file tracks what to evolve next.

## How It Works

Each time a new failure pattern is discovered in your projects:
1. Add an entry below with status `[pending]`
2. After the corresponding rule is created/updated, mark it `[done]`
3. Rules that prove unnecessary get `[cancelled]`

## Evolution Log

| Date | Incident | Rule Created/Updated | Status |
|------|----------|---------------------|--------|
| — | (Your first incident goes here) | — | — |

## How to Contribute Back

If you discover a failure pattern and create a rule that isn't in this repo:
1. Sanitize it (remove personal paths/info)
2. Open a PR to `niuma-engine`
3. Add it to the evolution log above

## Rule Upgrade Path

```
Single incident -> Write it in memory/{date}.md
Same incident 2+ times -> Create/update a rule in .claude/rules/
Incident pattern across projects -> Propose addition to niuma-engine
```

---

> The framework is alive. Your accidents are its next rules.
"""
with open(os.path.join(REPO, "EVOLUTION.md"), "w", encoding="utf-8") as f:
    f.write(evolution_content)
print("[OK] EVOLUTION.md created")

# ============================================================
# P2: Create skill-routing-table.example.json
# ============================================================
routing_example = """{
  "_comment": "Example skill routing table. Customize for your own skills/plugins.",
  "_usage": "If you use AI skills/plugins, define trigger words here so the AI auto-activates the right skill.",
  "version": "1.0",
  "routes": [
    {
      "id": "r001",
      "triggers": ["example trigger", "another way to say it"],
      "skill": "your-skill-name",
      "priority": 1,
      "auto": true,
      "confidence": 0.9,
      "note": "Replace with your actual skill name and trigger words"
    }
  ]
}
"""
with open(os.path.join(REPO, "skill-routing-table.example.json"), "w", encoding="utf-8") as f:
    f.write(routing_example)
print("[OK] skill-routing-table.example.json created")

# ============================================================
# P2: Update templates/ MEMORY.md (Chinese version)
# ============================================================
memory_zh = """# 项目记忆

> 此文件记录项目级的重要决策、教训和偏好。
> AI 每次对话应读取此文件以保持连续性。

---

## 项目基本信息
- 项目名称：
- 项目目标：
- 关键约束：

## 重要决策
<!-- 格式: [日期] 决策内容 — 理由 -->

## 用户偏好
<!-- 格式: [日期] 偏好内容 -->

## 踩坑记录
<!-- 格式: [日期] 坑 — 根因 — 如何避免 -->

## 待跟进
<!-- 格式: [日期] 事项 -->
"""
with open(os.path.join(REPO, "templates", "zh-CN", "MEMORY.md"), "w", encoding="utf-8") as f:
    f.write(memory_zh)
print("[OK] templates/zh-CN/MEMORY.md")

memory_en = """# Project Memory

> This file records project-level decisions, lessons learned, and preferences.
> The AI should read this file at the start of each conversation for continuity.

---

## Project Info
- Name:
- Goal:
- Key Constraints:

## Important Decisions
<!-- Format: [Date] Decision — Rationale -->

## User Preferences
<!-- Format: [Date] Preference -->

## Lessons Learned (Pitfalls)
<!-- Format: [Date] Pitfall — Root Cause — How to Avoid -->

## Follow-ups
<!-- Format: [Date] Item -->
"""
with open(os.path.join(REPO, "templates", "en", "MEMORY.md"), "w", encoding="utf-8") as f:
    f.write(memory_en)
print("[OK] templates/en/MEMORY.md")

# ============================================================
# Final summary
# ============================================================
print("\n" + "=" * 60)
print("ALL FIXES APPLIED")
print("=" * 60)
print("P0: CLAUDE.md created, README law-10 fixed, .gitignore allows CLAUDE.md")
print("P1: All 4 adapters updated, compatibility.md updated, agent-install.md fixed")
print("P2: EVOLUTION.md, skill-routing-table.example.json, MEMORY.md templates updated")
