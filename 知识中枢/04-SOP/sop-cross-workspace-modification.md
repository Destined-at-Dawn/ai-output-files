# SOP：跨工作区修改流程

> **版本**：v1.0 | 2026-05-18
> **来源**：从 2026-05-09 至 2026-05-18 的全部对话中提炼的修改流程和注意事项
> **核心理念**：改一个文件 = 改所有引用该文件的地方。没有"只改一处"这回事。

---

## 一、触发条件

| 场景 | 触发方式 | 修改深度 |
|------|---------|---------|
| 用户说"一改全改" | 明确意图 | 全量同步 |
| 修改共享规则/铁律 | 自动触发 | 4个工作区 + 模板 + 共享规则真源 |
| 修改个人信息（telos） | 自动触发 | telos + 4个CLAUDE.md + 分身YAML + 映射表 |
| 修改审计格式 | 自动触发 | 4个CLAUDE.md + long-term.md + session-summary + scaffold模板 |
| 修改skill路由规则 | 自动触发 | 4个skill-rules.json + skill-routing-rules-for-claude.md |

---

## 二、修改前必做（5步，不可跳过）

### Step 1：确认修改范围

```
问自己：这个修改会影响哪些文件？
  ├── 共享规则真源（shared-rules/）
  ├── 4个工作区的CLAUDE.md
  ├── 4个skill-rules.json
  ├── scaffold模板（_base.md + 领域模块）
  ├── session-summary/SKILL.md
  ├── memory/long-term.md（旧格式残留）
  └── 改进周期追踪器（improvement-cycle-tracker.md）
```

**铁律**：宁可多列不要漏列。漏一个 = FM-06（旧格式残留）。

### Step 2：备份

```bash
BACKUP_DIR="${LEGACY_ROOT}/归档/$(date +%Y%m%d)_修改备份"
mkdir -p "$BACKUP_DIR"
# 把要改的每个文件先 cp 到备份目录
```

### Step 3：Read 当前内容

**对每个要修改的文件，先 Read 当前内容。** 不是"我记得"，是 Read。

### Step 4：Grep 全量搜索

```bash
# 搜索所有可能包含相关内容的文件
grep -rn "关键词" "${LEGACY_ROOT}/" --include="*.md" | grep -v "归档"
```

**铁律**：搜索范围必须包括：
- 工作区根目录的 .md 文件
- `memory/` 目录
- `SOPs/` 目录
- `projects/` 子目录
- `mutual/mutual/` 中枢
- `C:\Users\13975\.newmax\skills\` 已安装skill

### Step 5：确认修改内容

用一句话说清楚：**"我要把 X 改成 Y，涉及 A/B/C/D 四个文件。"**

---

## 三、修改执行（Edit优先）

### 3.1 Edit vs Write 决策树

```
只改几行？ → Edit（精确替换）
需要大幅重写但保留部分内容？ → Read → 拼接新旧 → Write
全新文件（确实不存在）？ → 可以直接 Write
```

**铁律**：能用 Edit 就不要用 Write。Write 是覆写，Edit 是精确替换。

### 3.2 批量修改模式

当同一修改需要应用到多个文件时：

1. **先改一个** — 在第一个文件上完成 Edit，Read 验证
2. **复制模式** — 确认第一个文件改对后，用同样的 Edit 模式改其他文件
3. **逐个验证** — 每个文件改完后 Read 验证

**禁止**：一次性批量 Edit 所有文件然后只验证最后一个。

### 3.3 特殊情况：编码问题

| 编码 | 处理方式 |
|------|---------|
| UTF-8 | 直接 Edit/Write |
| 非UTF-8 | 用 Python 操作（见 FM-09） |
| 不确定 | 先用 `file -i` 检测编码 |

---

## 四、修改后验证（3步，不可跳过）

### Step 1：Read 验证

每个修改过的文件，立即 Read 确认内容正确。

### Step 2：Grep 搜索残留

```bash
# 搜索旧值是否还存在
grep -rn "旧值" "${LEGACY_ROOT}/" --include="*.md" | grep -v "归档"
```

### Step 3：更新索引

如果修改涉及：
- 新增/删除文件 → 更新对应的索引（SOP总索引、skill-catalog、MEMORY.md）
- 修改版本号 → 更新变更记录
- 修改触发条件 → 更新 skill-rules.json

---

## 五、跨工作区同步清单

### 5.1 共享规则同步（R01~R11）

修改任一共享规则时，必须同步到：

| 目标文件 | 路径 |
|---------|------|
| 真源文件 | `mutual/mutual/li-sync/shared-rules/R{NN}-*.md` |
| 注册表 | `mutual/mutual/li-sync/shared-rules-registry.md` |
| 创作区 CLAUDE.md | `创作/创作/CLAUDE.md` |
| 求职区 CLAUDE.md | `求职/求职/CLAUDE.md` |
| 个人区 CLAUDE.md | `个人/个人/CLAUDE.md` |
| 竞赛区 CLAUDE.md | `竞赛/竞赛/CLAUDE.md` |
| scaffold 模板 | `mutual/mutual/scaffold-workspace/templates/claude-md/_base.md` |
| session-summary | `C:\Users\13975\.newmax\skills\session-summary\SKILL.md` |

### 5.2 个人信息同步（telos）

修改个人信息时，必须同步到：

| 目标文件 | 路径 |
|---------|------|
| telos 源文件 | `C:\Users\13975\.claude\telos\*.md` |
| 创作区 CLAUDE.md §身份 | `创作/创作/CLAUDE.md` |
| 求职区 CLAUDE.md §身份 | `求职/求职/CLAUDE.md` |
| 个人区 CLAUDE.md §身份 | `个人/个人/CLAUDE.md` |
| 竞赛区 CLAUDE.md §身份 | `竞赛/竞赛/CLAUDE.md` |
| 分身 YAML | `个人/个人/分身/*.yaml` |
| telos 映射表 | `mutual/mutual/li-sync/telos-mapping.md` |

### 5.3 审计格式同步

修改 📋 技能审计格式时，必须同步到：

| 目标文件 | 位置 |
|---------|------|
| session-summary SKILL.md | 标准格式模板 + 示例 |
| 创作区 CLAUDE.md | F1 铁律层 |
| 求职区 CLAUDE.md | F1 铁律层 |
| 个人区 CLAUDE.md | F1 铁律层 |
| 竞赛区 CLAUDE.md | F1 铁律层 |
| 竞赛区 CLAUDE.md | §1.3（如果有第二处定义） |
| 竞赛项目级 CLAUDE.md | §1.3（如果有） |
| memory/long-term.md | §三.2（如果有旧格式模板） |
| scaffold 模板 | _base.md |

**铁律**：Grep 搜索 `📋 技能审计` + `已写入记忆` + `未调用但可用` + `下次改进` 四个关键词，确保旧格式完全清除。

### 5.4 PDF/文档处理规则同步

修改文档处理规则时，必须同步到：

| 目标文件 | 位置 |
|---------|------|
| 4个 CLAUDE.md | F2 文件操作铁律 |
| scaffold 模板 | F2 |
| shared-rules R03 | 3.5 文件类型强制调skill |
| 竞赛 CLAUDE.md §4.5 | 工具速查表 |
| 竞赛 SOP-11 | PDF读取流程 |

---

## 六、常见失败模式速查

| 编号 | 失败模式 | 一句话预防 |
|------|---------|-----------|
| FM-06 | 旧格式残留 | Grep 全量搜索，包括 long-term.md |
| FM-07 | Write 覆写丢数据 | Read before Write，Edit not Write |
| FM-08 | 声称完成没做 | Write 后立即 Read 验证 |
| FM-10 | 数字不一致 | 19个文件搜6种值，逐个修正 |
| FM-12 | 只承诺不行动 | 改进必须写入可执行机制 |

---

## 七、检查清单

每次跨工作区修改完成后，逐项勾选：

- [ ] 备份已创建（`E:\ai产出文件\牛马\归档\{日期}_修改备份\`）
- [ ] 所有要改的文件已 Read 当前内容
- [ ] Grep 全量搜索已完成（无残留）
- [ ] 每个修改过的文件已 Read 验证
- [ ] 共享规则真源已更新
- [ ] 注册表已更新
- [ ] 4个工作区 CLAUDE.md 已同步
- [ ] scaffold 模板已同步
- [ ] memory/long-term.md 中无旧格式残留
- [ ] 索引已更新（skill-catalog、SOP总索引、MEMORY.md）
- [ ] improvement-cycle-tracker 已更新

---

## 变更记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-05-18 | v1.0 | 从 2026-05-09~18 全部对话中提炼的修改流程 + 5步前置 + 3步验证 + 4类同步清单 |


---

## 认知科学支撑（百大认知书籍）

| 认知机制 | 来源 | 在跨工作区修改SOP中的应用 |
|---------|------|----------------------|
| **涟漪效应** | 008-协同智能 §概念1 | "改一个文件=改所有引用该文件的地方"=涟漪效应——信息在网络中传播，修改一个节点→波纹扩散到所有连接节点。SOP的目的=显式追踪涟漪→不漏掉任何受影响节点 |
| **变化传播** | 025-认知负荷理论 §概念4 | 4类同步清单(共享规则/个人信息/审计格式/PDF规则)=变化传播图式的外部化——人类工作记忆装不下"修改X需要同步到哪些文件"的完整图式→外部化到SOP→减少遗漏 |
| **预检清单** | 061-助推 §概念1 | "修改前5步"=预检清单的助推设计——把"应该做的事"变成"清单上打勾的事"。没有清单→依赖记忆→遗忘；有清单→依赖列表→零遗漏 |
| **确认偏误防御** | 010-思考快与慢 §概念3 | Step 4 Grep全量搜索=防御确认偏误——AI倾向于"觉得已经改完了"(因为"想不起来还有哪里")。Grep搜索=客观证据→打破"我觉得" |
| **失败模式目录** | 046-反脆弱 §概念1 | FM-06~FM-12的失败模式表=从错误中学习的系统化——每个失败模式=一个"反脆弱点"。目录越完整→系统越抗脆弱 |

---

## 🔗 相关链接
- [[sop-git-workflow]] · [[sop-skill-creation]] · [[sop-template]]
- 🟣 [[MASTER-路由中枢]] · [[共享规则注册表]]
- [[工作区对比]] · [[知识流动图]]
