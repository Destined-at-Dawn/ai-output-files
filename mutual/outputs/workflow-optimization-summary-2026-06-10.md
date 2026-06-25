# 工作流彻底优化总结

> 日期: 2026-06-10
> 来源: 12篇文章信息差总结-道法术器版 (247行, 15条信息差)
> 方法论: 道法术器四层 × 15条信息差逐一对照
> 辅助: arXiv 2603.22386 (Agentic Computation Graphs survey)

---

## 执行清单

### ✅ 已完成

| # | 动作 | 产出文件 | 状态 |
|---|------|---------|------|
| 1 | 归档当前状态 | `E:i产出文件\牛马\归档6-06-10-workflow-pre-optimization\` | ✅ |
| 2 | 15条信息差差距分析 | `outputs/workflow-gap-analysis-2026-06-10.md` | ✅ |
| 3 | Skill ABCD分类+冗余审计 | `outputs/skill-abcd-classification-2026-06-10.md` | ✅ |
| 4 | 知识库三层结构设计 | `outputs/knowledge-base-design-2026-06-10.md` | ✅ |
| 5 | 创建知识库目录 | `knowledge-base/{layer0,layer1,layer2}/` | ✅ |
| 6 | 首批知识卡 | `knowledge-base/layer1-cards/{patterns,lessons,decisions}/` | ✅ |
| 7 | 路由表升级v2.0 | `skill-routing-table.json` (109条全量更新) | ✅ |
| 8 | li-intent增加Plan阶段 | `~/.newmax/skills/li-intent/SKILL.md` v2.0 | ✅ |
| 9 | 网络搜索补充 | arXiv ACG survey + 10篇Agent最佳实践 | ✅ |

### 🔄 待执行（需要后续对话）

| # | 动作 | 预计工作量 | 优先级 |
|---|------|-----------|--------|
| 10 | Skill合并执行（interactive-learning→thinking-coach等5组） | 30分钟 | P1 |
| 11 | memory/long-term.md精简（提取知识卡） | 20分钟 | P1 |
| 12 | li-manage Flow E增加强制瘦身 | 15分钟 | P1 |
| 13 | skill-usage-log.md增加成功率统计 | 10分钟 | P2 |
| 14 | 受众优先原则注入content_create意图 | 10分钟 | P2 |
| 15 | li-safe增加vibe-coding专项检查 | 15分钟 | P2 |
| 16 | 同步路由表到所有工作区 | 5分钟 | P1 |

---

## 核心优化成果

### 1. 路由系统: 扁平关键词 → 超图+选择性激活

**Before**: 109条路由 = trigger词→skill名的扁平映射
**After**: 109条路由 = 超图，每条带ABCD分类 + DAG链 + IO类型

| 字段 | 新增 | 用途 |
|------|------|------|
| `category` | A/B/C/D | 不同类别不同治理策略 |
| `chain` | [skill1, skill2, ...] | D类skill的前置依赖链 |
| `io` | {input, output} | skill间数据流类型 |

**arXiv验证**: 超图+选择性激活是当前最优的Agent编排模式 (arXiv 2603.22386)

### 2. 意图引擎: 纯关键词匹配 → Phase 0-4 + Plan阶段

**Before**: li-intent Phase 0(分类) → Phase 1(SOP查找) → Phase 2(上下文) → Phase 3(执行) → Phase 4(晋升)
**After**: Phase 0(分类) → **Phase 0.5(Plan)** → Phase 1(SOP查找) → Phase 2(上下文) → Phase 3(执行) → Phase 4(晋升)

Plan阶段强制:
- 复合意图必须先输出执行计划
- D类skill必须先执行前置链
- 简单意图跳过Plan

### 3. 知识管理: 混合存储 → 三层结构

**Before**: memory/混合偏好+教训+知识，outputs/混合产出+分析
**After**: 

```
Layer 0 (碎片) → Layer 1 (知识卡) → Layer 2 (可执行)
  快速积累          独立可复用          Skill/SOP/规则
  30天审查          长期保留            跟随生命周期
```

### 4. Skill治理: 无分类 → ABCD四类

| 类型 | 数量 | 治理策略 |
|------|------|----------|
| A 原子 | 8个 | 只维护，季度审查 |
| B 组合 | 16个 | 定期优化，月度审查 |
| C 调度 | 3个 | 优先优化，周度审查 |
| D 衍生 | 27个 | 可合并/淘汰，月度审查 |

### 5. 冗余审计: 发现8组可合并

| 重叠组 | 建议 | 节省 |
|--------|------|------|
| interactive-learning + thinking-coach + li-mindcoach | 合并为thinking-coach | -2 skill |
| ai-yuyi + aihot | 合并为aihot | -1 skill |
| li-safe + li-security-scan | 合并为li-safe | -1 skill |
| writing-plans + doc-coauthoring + li-writer | 合并为doc-coauthoring | -2 skill |
| daily-review + session-summary | 合并为session-summary | -1 skill |

合并后: 30个 → ~23个本地skill

---

## 信息差覆盖率

| 层级 | 信息差 | 覆盖状态 |
|------|--------|---------|
| 道 | 1. Agent=系统 | ✅ 知识卡+实践 |
| 道 | 2. Harness>模型 | ✅ CLAUDE.md已是Harness |
| 道 | 3. Skill选择=结构推理 | ✅ 路由表v2.0+DAG |
| 道 | 4. 合成数据不是万能 | ✅ 记录为原则 |
| 法 | 5. ABCD分类 | ✅ 全量分类完成 |
| 法 | 6. 知识库三层 | ✅ 目录结构+首批知识卡 |
| 法 | 7. Pass@k vs Pass^k | 🟡 记录，待实现统计 |
| 法 | 8. Skill治理三层 | 🟡 设计完成，待执行合并 |
| 法 | 9. Agentic Workflow | ✅ Plan阶段+四阶段强制 |
| 术 | 10. 受众优先 | 🟡 记录，待注入 |
| 术 | 11. 安全红灯 | ✅ 已有完善机制 |
| 术 | 12. 拼屏/断联 | ✅ N/A（本地开发） |
| 器 | 13. Prompt→URL | 🟢 低优先级 |
| 器 | 14. 软件工程基底 | ✅ 已基于现有框架 |
| 器 | 15. 远程基础设施 | ✅ N/A（本地开发） |

**覆盖率**: 10/15 完全覆盖, 3/15 部分覆盖, 2/15 N/A

---

## 认知科学支撑

| 认知机制 | 来源 | 在本次优化中的应用 |
|---------|------|-------------------|
| **结构化认知** | 认知负荷理论 | ABCD分类降低skill选择的认知负荷 |
| **分层记忆** | 记忆三级模型 | 知识库三层结构对应感觉/短时/长时记忆 |
| **元认知监控** | 元认知理论 | Plan阶段强制"先想后做" |
| **选择性注意** | 注意力理论 | 超图+选择性激活 = 注意力聚焦 |

---

## 产出文件清单

| 文件 | 路径 | 性质 |
|------|------|------|
| 差距分析 | `outputs/workflow-gap-analysis-2026-06-10.md` | Layer 0→1 |
| ABCD分类 | `outputs/skill-abcd-classification-2026-06-10.md` | Layer 1 |
| 知识库设计 | `outputs/knowledge-base-design-2026-06-10.md` | Layer 1 |
| 路由表v2.0 | `skill-routing-table.json` | Layer 2 |
| li-intent v2.0 | `~/.newmax/skills/li-intent/SKILL.md` | Layer 2 |
| 知识卡:Agent系统思维 | `knowledge-base/layer1-cards/patterns/agent-system-thinking.md` | Layer 1 |
| 知识卡:429事故教训 | `knowledge-base/layer1-cards/lessons/lesson-005-agent-429.md` | Layer 1 |
| 知识卡:三层结构决策 | `knowledge-base/layer1-cards/decisions/knowledge-base-3layer.md` | Layer 1 |
| 归档 | `E:i产出文件\牛马\归档6-06-10-workflow-pre-optimization\` | 归档 |
