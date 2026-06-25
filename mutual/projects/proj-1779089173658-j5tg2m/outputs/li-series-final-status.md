---
title: li-series-final-status
date: 2026-06-11
---

# li-series Final Status Report

> Generated: 2026-06-11 | Method: Python full scan

## Core Metrics

| Metric | Value |
|--------|-------|
| li-* directories | **48** |
| Active (no DEPRECATED.md) | **40** |
| Deprecated (30-day buffer) | **8** |
| Quality pass rate (active only) | **40/40 (100%)** |
| All <=300 lines | YES |
| All have _meta.json | YES |
| All have eval.json | YES |
| All have golden_rules.md | YES |
| Total routes | 73 |
| Total triggers | 1312 |
| Cross-skill duplicates | **0** |
| Synced workspaces | **67** |

## All Skills

| # | Skill | Lines | Refs | Trigs | Role |
|---|-------|-------|------|-------|------|
| 1 | li-analyze | 224 | 7 | 63 | dao-fa-shu-qi + 100-cognition analysis |
| 2 | li-bestskill | 296 | 4 | 26 | cross-platform skill discovery |
| 3 | li-code | 171 | 1 | 13 |  |
| 4 | li-competition | 149 | 3 | 33 | competition workflow |
| 5 | li-data | 146 | 2 | 12 | data analysis |
| 6 | li-dbs | 127 | 3 | 12 | DBS diagnosis method |
| 7 | li-debug | 270 | 3 | 40 | disciplined debug loop |
| 8 | li-design | 147 | 3 | 18 | design tasks |
| 9 | li-devil | 212 | 3 | 12 | cold water / pre-mortem |
| 10 | li-diagnose | 230 | 3 | 40 | system entropy diagnosis |
| 11 | li-docs | 292 | 1 | 0 | documentation management |
| 12 | li-frontend | 116 | 1 | 0 | frontend development |
| 13 | li-hardware | 228 | 27 | 132 | FPGA/Arduino/embedded |
| 14 | li-image | 142 | 3 | 23 | image generation |
| 15 | li-improve | 299 | 17 | 45 | evolution engine |
| 16 | li-industry | 297 | 5 | 24 | industry research |
| 17 | li-infra | 299 | 4 | 15 | infrastructure management |
| 18 | li-intent | 187 | 5 | 17 | SOP-driven intent engine |
| 19 | li-local-search | 236 | 3 | 9 | local skill search |
| 20 | li-manage | 246 | 12 | 26 | skill lifecycle |
| 21 | li-memory | 284 | 6 | 20 | 3-layer memory + contradiction |
| 22 | li-mindcoach | 260 | 11 | 24 | mental coaching |
| 23 | li-office | 168 | 3 | 27 | Office documents |
| 24 | li-personal | 109 | 1 | 0 | personal decisions |
| 25 | li-plan | 292 | 3 | 10 | task + long-term planning |
| 26 | li-platform | 105 | 1 | 0 | platform operations |
| 27 | li-prompt | 300 | 5 | 30 | cross-AI prompt building |
| 28 | li-research | 297 | 9 | 58 | deep research + iterative |
| 29 | li-search | 106 | 1 | 0 | semantic search |
| 30 | li-session | 105 | 1 | 0 | session management |
| 31 | li-skillcreate | 291 | 12 | 22 | skill creation (search-first) |
| 32 | li-skillfusion | 285 | 6 | 17 | skill fusion/split |
| 33 | li-skills-mgmt | 145 | 1 | 14 | skill management |
| 34 | li-storyboard | 294 | 4 | 34 | storyboard scripts |
| 35 | li-study | 205 | 3 | 47 | learning + exams |
| 36 | li-sync | 300 | 4 | 25 | cross-workspace sync |
| 37 | li-transcript | 231 | 5 | 30 | transcript cleaning |
| 38 | li-triage | 258 | 2 | 37 | issue triage state machine |
| 39 | li-video | 149 | 3 | 21 | video production |
| 40 | li-visual | 295 | 3 | 33 | visual style prompts |
| 41 | li-voice | 113 | 1 | 0 | voice transcription |
| 42 | li-web | 146 | 3 | 18 | web development |
| 43 | li-webtest | 234 | 4 | 26 | web testing |
| 44 | li-wechat | 145 | 3 | 14 | WeChat ecosystem |
| 45 | li-workflow | 195 | 2 | 23 | automated workflows |
| 46 | li-workspace | 206 | 12 | 14 | workspace ops (3 modes) |
| 47 | li-writing | 118 | 1 | 0 | writing tools |
| 48 | li-xhs | 162 | 3 | 28 | Xiaohongshu content |

## Architecture Tiers

### Tier 1: Core Engine (5)
- **li-research** -- deep research entry point
- **li-hardware** -- FPGA/Arduino/embedded
- **li-analyze** -- dao-fa-shu-qi + 100-cognition
- **li-improve** -- post-conversation self-audit
- **li-manage** -- lifecycle management

### Tier 2: Capability Modules (42)
All other li-* as sub-routines or independent modules.

### Tier 3: SOP Orchestration
- **li-intent** -- reads SOP indexes from each workspace
- **SOP indexes** -- IF/ELSE routing + chain calls + self-learning

## Honest Boundary Declaration

### Can Claim
- 48 skills pass structural quality gates
- 0 duplicate triggers, 67 workspaces synced
- li-intent connected to real SOP data

### Cannot Claim
- 8 个 skill 已标记 DEPRECATED（li-writing/li-session/li-voice/li-search/li-personal/li-docs/li-frontend/li-platform），不应计入"活跃"总数
- ~30 skills never triggered in real tasks; cases are inferred
- Some golden_rules are domain-common-sense, not battle-tested

### Unknown
- 80%% task coverage claim needs real usage validation
- li-intent matching accuracy needs real data calibration