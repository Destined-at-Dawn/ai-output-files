# 变量参考手册 (VARIABLE-REFERENCE.md)

## 路径变量定义

| 变量 | 含义 | 典型值 |
|------|------|--------|
| ${WORKSPACE_ROOT} | 当前工作区根目录 | F:i产出文件\mutual |
| ${AI_ROOT} | AI产出文件根目录 | F:i产出文件 |
| ${KNOWLEDGE_HUB} | 知识中枢目录 | F:i产出文件\知识中枢 |
| ${SHARED_RULES} | 共享规则目录 | F:i产出文件\_sharedules |
| ${SKILL_REGISTRY} | Skill路由表目录 | F:i产出文件\_shared\skill-registry |
| ${LEGACY_ROOT} | 旧E盘根目录（过渡期） | E:i产出文件\牛马 |
| ${NEWMAX_HOME} | Newmax配置目录 | ~/.newmax/ |
| ${CLAUDE_HOME} | Claude配置目录 | ~/.claude/ |
| ${WORK_ROOT} | F盘工作目录 | F:\work |

## 使用规则

### 1. 配置文件
CLAUDE.md、.claude/rules/、skill-routing-table.json 中使用变量占位符。

### 2. 记忆文件
memory/ 中的历史记录保留原样，不替换路径。

### 3. 产出文件
outputs/ 中的脚本和报告保留原样，不替换路径。

### 4. 新文件
新建文件时使用变量，不写硬编码路径。

## 过渡期说明

迁移期间，旧路径 ${LEGACY_ROOT} 仍然有效：
- E:i产出文件\牛马\ 下的文件保留不删除
- 新工作在 F:i产出文件\ 下进行
- 旧文件逐步迁移，预计 2026-07-31 前完成
