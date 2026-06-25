# Agent PR Template

<!-- 使用说明：Agent 在创建 PR 时必须填写以下所有部分 -->

## Task Description

<!-- 原始任务描述，包括 task-id 和需求来源 -->

## What Changed

<!-- 核心变更摘要，聚焦「做了什么」而非「改了哪些文件」 -->

## Key Design Decisions

<!-- Agent 做出的关键设计决策及理由 -->
- Decision 1: ... because ...
- Decision 2: ... because ...

## Alternatives Considered

<!-- 考虑过但未采用的方案，以及为什么没有选择 -->

## Test Coverage

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed: <描述>

## Known Limitations / Follow-up Tasks

<!-- 当前实现的局限，后续需要跟进的工作 -->

## Review Guidance

<!-- 建议 reviewer 重点关注的部分 -->

## Agent Metadata

- **Agent-Model**: <!-- 使用的模型，如 claude-3.5-sonnet -->
- **Agent-Task**: <!-- 任务 ID -->
- **Commit Count**: <!-- 提交数量 -->
- **Files Changed**: <!-- 修改的文件数量 -->

---

<!-- 
Checklist for Agent before submitting PR:
1. [ ] All commits follow Conventional Commits format
2. [ ] All commits include Agent-Task / Agent-Decision trailers
3. [ ] History is cleaned up (WIP commits squashed)
4. [ ] Each commit is atomic (one logical change)
5. [ ] Code builds and tests pass
6. [ ] No sensitive information (API keys, tokens, passwords)
-->
