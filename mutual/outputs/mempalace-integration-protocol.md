# MemPalace 生态整合协议 v1.0

> **核心定位**：mempalace 是小黎 8 工具生态的**共享语义搜索引擎**——76 万+ 条向量记录覆盖所有工作区 + 知识中枢，提供跨工具、跨工作区的语义级信息检索能力。

---

## 一、架构全景

```
┌─────────────────────────────────────────────────────┐
│                   MemPalace 向量数据库                  │
│              D:\mempalace\palace\chroma.sqlite3        │
│              76 万+ 条嵌入，88K 向量记录                   │
└──────────┬──────────┬──────────┬──────────┬──────────┘
           │          │          │          │
     ┌─────┴────┐ ┌──┴───┐ ┌──┴────┐ ┌──┴────┐
     │ MCP 直连 │ │CLI调用│ │知识中枢│ │独立体系│
     │          │ │      │ │同步层  │ │(不接入)│
     └──────────┘ └──────┘ └───────┘ └───────┘
           │          │          │          │
    ┌──────┴──────┐   │    ┌────┴─────┐    │
    │Newmax      │   │    │Hermes    │    │
    │Claude Desk │   │    │          │    │
    │            │   │    └──────────┘    │
    └────────────┘   │                    │
                ┌────┴─────┐         ┌───┴────┐
                │Codex     │         │Marvis  │
                │Antigravity│        │WorkBuddy│
                └──────────┘         └────────┘
```

---

## 二、各工具接入方式

### 1. Newmax（牛马AI）— MCP 直连 ✅

**配置**：`~/.newmax/.mcp.json` → `mempalace` server
**包装脚本**：`~/.newmax/scripts/mempalace_mcp.py`
**环境变量**：`PYTHONUTF8=1` + `MEMPALACE_PALACE_PATH=D:\mempalace\palace`

**使用方式**：
- 对话中直接调用 `mempalace_search` MCP 工具
- 支持 30 个 MCP 工具（search / add_drawer / sync / kg_* / diary_*）

**自动触发场景**：
- 写 memory 前 → 搜"之前记录过什么类似的决策"
- debug 时 → 搜"这个错误以前遇到过没有"
- 创建 Skill 前 → 搜"有没有相关的已有 Skill"
- 做方案时 → 搜"某个技术方案的历史讨论"

### 2. Claude Desktop — MCP 直连 ✅

**配置**：`%APPDATA%\Claude\claude_desktop_config.json` → `mcpServers.mempalace`
**包装脚本**：复用 `~/.newmax/scripts/mempalace_mcp.py`
**环境变量**：`PYTHONUTF8=1` + `MEMPALACE_PALACE_PATH=D:\mempalace\palace`

**重启生效**：配好后需要重启 Claude Desktop。

### 3. Codex — CLI 调用 ✅

**配置**：`~/.codex/AGENTS.md` 已添加 MemPalace 引用段
**调用方式**：
```bash
PYTHONUTF8=1 MEMPALACE_PALACE_PATH="D:/mempalace/palace" \
  python -m mempalace search "查询内容" --limit 5 --agent xiaoli
```

**适用场景**：
- 写代码前查"之前有没有类似实现"
- 创建 Skill 前查"有没有相关的已有 Skill"
- 做技术方案时查"某个技术决策的历史讨论"

### 4. Antigravity (Gemini) — CLI 调用

**调用方式**：同 Codex，CLI 调用
**配置**：待 Antigravity 支持 MCP 后切换到 MCP 直连

### 5. Hermes — 知识中枢间接接入

**接入路径**：mempalace 索引知识中枢 → Hermes 读知识中枢 → 间接获得语义搜索能力

**Hermes 不直接调用 mempalace**，因为：
- Hermes 是记忆中枢，专注于跨工具状态追踪和记忆管理
- mempalace 的知识已通过索引融入知识中枢的内容
- Hermes 的 atomic-facts / cross-tool-state 已在 mempalace 索引范围内

**同步机制**：mempalace 每周自动索引知识中枢（见第四节）

### 6. Marvis — 独立知识库（不接入）

**原因**：Marvis 是腾讯应用宝桌面 AI，有独立的知识库系统，不支持外部 MCP 或 CLI 调用。
**替代方案**：Marvis 使用自己的 Knowledgebase 目录。

### 7. WorkBuddy — 飞书体系（不接入）

**原因**：WorkBuddy 使用 connector-proxy MCP 连接飞书，是 UI 展示层，不涉及语义搜索。
**替代方案**：飞书文档通过知识中枢间接被 mempalace 索引。

---

## 三、Wing 分类体系

| Wing | 索引目录 | 内容类型 |
|------|---------|---------|
| knowledge-hub | `E:\ai产出文件\牛马\知识中枢\` | 注册表、共享规则、hermes-memory、知识图谱 |
| mutual | `E:\ai产出文件\牛马\mutual\mutual\` | 生态优化、规则、记忆、SOP |
| personal | `E:\ai产出文件\牛马\个人\个人\` | 成长规划、认知书籍、考研准备 |
| creation | `E:\ai产出文件\牛马\创作\创作\` | 公众号、内容创作、文风 DNA |
| job | `E:\ai产出文件\牛马\求职\求职\` | 简历、面试、实习准备 |
| competition | `E:\ai产出文件\牛马\竞赛\竞赛\` | FPGA、YOLO、皮影、ICAN |
| study | `E:\ai产出文件\牛马\学习\` | 高数、物理、电路、英语 |
| daily-study | `E:\ai产出文件\牛马\日常学习\` | 解题、作业、LaTeX |
| skills | `~/.newmax/skills/` | li- skill 生态（111 个 skill） |
| memory | (跨 wing) | 记忆文件、教训档案、决策记录 |
| technical | (跨 wing) | 代码、脚本、技术文档 |

---

## 四、自动同步机制

### 每周日 23:00 — 全量增量索引

**触发方式**：定时任务（project-tools scheduled task）
**执行脚本**：`~/.newmax/scripts/mempalace_full_mine.py`
**覆盖范围**：9 个目录全部增量扫描
**预计耗时**：10-30 分钟（只处理新增/修改的文件）

### 手动触发

```bash
# 索引单个目录
PYTHONUTF8=1 MEMPALACE_PALACE_PATH="D:/mempalace/palace" \
  python -m mempalace mine "E:\ai产出文件\牛马\知识中枢" --wing knowledge-hub --agent xiaoli

# 全量索引
PYTHONUTF8=1 python ~/.newmax/scripts/mempalace_full_mine.py
```

---

## 五、使用协议

### 何时用 mempalace（AI 自动判断）

| 信号 | 动作 |
|------|------|
| 用户问"之前做过什么" | → mempalace_search |
| 用户问"这个错误见过没" | → mempalace_search |
| 写 memory 前 | → 搜"相关决策/教训" |
| 创建 Skill 前 | → 搜"类似的已有 Skill" |
| 做技术方案 | → 搜"相关技术讨论" |
| grep 3 次没找到 | → 切 mempalace 语义搜索 |

### 何时不用 mempalace

| 场景 | 原因 |
|------|------|
| 查最新文件（<24h） | 索引有延迟 |
| 精确文件路径已知 | 直接 Read 更快 |
| 简单关键词搜索 | Grep 更快更准 |
| 实时数据 | mempalace 是离线索引 |

### 搜索质量门禁

- 搜索结果必须标注来源（wing + 文件路径）
- cosine 相似度 < 0.3 的结果不可信
- 中文搜索质量待验证（BM25 模式下可能有乱码）

---

## 六、维护计划

| 事项 | 频率 | 负责人 |
|------|------|--------|
| 全量增量索引 | 每周日 23:00（自动） | mempalace_full_mine.py |
| HNSW 索引完整性检查 | 每月 1 日 | 手动/自动 |
| Wing 分类准确性 | 新工作区创建时 | AI 自动 |
| MCP 服务器健康检查 | 每次对话（MCP init 时） | Claude/Newmax |

---

## 七、已知限制

1. **HNSW 索引损坏**：2026-06-10 junction 迁移导致，正在重建（76 万向量，预计 30-60 分钟 CPU 时间）
2. **中文搜索乱码**：BM25 模式下中文查询可能返回乱码，HNSW 重建后语义模式应正常
3. **索引延迟**：新文件最多 24 小时后才被索引（每周日全量扫描）
4. **Marvis/WorkBuddy 不接入**：这两个工具有独立体系，无法使用 mempalace

---

> 创建日期：2026-06-17
> 版本：v1.0
> 触发原因：用户要求"将 MCP 跟知识中枢结合，跟所有工具一起协作"
