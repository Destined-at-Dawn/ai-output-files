# Goal 模式全流程协议（CRITICAL — v2.0 2026-06-12）

> **触发场景**：用户消息含 "Goal 模式" / "最多N轮" / "token预算" / "GOAL_STATUS"
> **事故来源**：9 轮 Goal 模式中 5 轮重复下载 CPLID、3 次重复创建 Skill、任务完成但不停止
> **根因**：上下文压缩失忆 + 中文路径幽灵文件 + 完成判定缺失 + 没有 checkpoint 机制

---

## 一、Goal 模式生命周期（6 步，不可跳步）

```
收到 Goal 消息
  │
  ├─ Step 0：磁盘验证（铁律 1）     ← 每轮开始必做
  ├─ Step 1：计划对齐（铁律 5）     ← 对照原始目标分解子任务
  ├─ Step 2：路由扫描（铁律 0）     ← Goal 不豁免
  ├─ Step 3：执行子任务             ← 逐个完成，每完成一个验证落盘
  ├─ Step 4：完成判定（铁律 7）     ← 任务完成 → 立即停止
  └─ Step 5：Checkpoint + 下轮规划（铁律 6） ← 每轮结束必做
```

---

## 二、铁律（8 条，违反 = 事故）

### 铁律 0：Goal 模式不豁免路由扫描

**铁律**：Goal 模式豁免 CLAUDE.md 的 Step 0-4（runtime-snapshot / memory / evolution），**不豁免 Step 4.5 路由扫描**。
每条 Goal 消息处理前，必须花 5 秒扫描 skill-routing-table.json。
匹配到 P1 路由 → 立即调用，即使在 Goal 模式下。

### 铁律 1：每轮开始必须先验证磁盘

**强制执行，不可跳过。**

```python
# 每轮 Goal 开始时的 FIRST 操作
import os, glob
checks = {
    'CPLID': 'D:/AICompData/CPLID_YOLO/',
    'InsPLAD': 'D:/AICompData/InsPLAD_det/',
    'IDD': 'D:/AICompData/IDD_YOLO/',
    'Merged': 'D:/AICompData/Merged_4Class/',
    'runs': 'D:/AI竞赛数据集/runs/',
    'skill_competition': os.path.expanduser('~/.newmax/skills/competition-yolo/SKILL.md'),
    'skill_li': os.path.expanduser('~/.newmax/skills/li-competition/SKILL.md'),
}
for name, path in checks.items():
    if os.path.isdir(path):
        print(f'{name}: EXISTS, {len(os.listdir(path))} items')
    elif os.path.isfile(path):
        print(f'{name}: EXISTS, {os.path.getsize(path)} bytes')
    else:
        print(f'{name}: NOT FOUND')
```

**决策**：
- 全部 EXISTS → 跳过下载，直接进入训练/分析
- 部分缺失 → 只下载缺失部分
- 全部 NOT FOUND → 才执行完整下载流程

### 铁律 2：Skill/文件创建前必须 Glob 检查

想创建 xxx.md → Glob 搜索是否已存在 → 已存在：Read → Edit 增量更新 → 不存在：Write 新文件。

### 铁律 3：中文路径永远用 Python，永远正斜杠

| 操作 | 正确 | 错误 |
|------|------|------|
| 检查目录存在 | `os.path.isdir('D:/AICompData/')` | `bash ls` |
| 复制文件 | `shutil.copy2(src, dst)` | `cp` / `copy` |
| 读取文件 | `open(path, encoding='utf-8')` | `cat` |
| 写入文件 | `open(path, 'w', encoding='utf-8')` | `echo` / heredoc |

### 铁律 4：每步产出必须锚定到磁盘 + 立即写 checkpoint

| 要求 | 验证方式 |
|------|---------|
| 数据集下载完成 | `len(os.listdir(images_dir)) > 0` |
| VOC→YOLO 转换完成 | `len(labels) == len(images)` |
| 训练启动 | `results.csv` 存在且行数 > 1 |
| ONNX 导出 | `.onnx` 文件存在且 > 1MB |
| Skill 创建 | `SKILL.md` 存在且 > 1KB |
| 论文下载 | PDF 文件存在且 > 100KB |

**每完成一个子任务，立即执行验证 + 写 checkpoint（铁律 6）。**

### 铁律 5：计划对齐——每轮对照原始目标分解子任务

**问题**：9 轮 Goal 中，第 7-9 轮完全不知道自己在做什么——目标和执行完全脱节。

**协议**：

```
Step 1: 提取原始目标（从用户第一条 Goal 消息中解析）
Step 2: 将原始目标分解为可验证的子任务清单（含磁盘路径）
Step 3: 对照磁盘验证结果（铁律 1），划掉已完成的子任务
Step 4: 只执行未完成的子任务
Step 5: 每完成一个，划掉 + 写 checkpoint
```

**子任务模板**：
```markdown
## Goal 子任务清单（本轮）

| # | 子任务 | 验证路径 | 状态 |
|---|--------|---------|------|
| 1 | CPLID 下载+转换 | `D:/AICompData/CPLID_YOLO/images/train/` len > 0 | ⬜ |
| 2 | CPLID 训练完成 | `runs/yolo12n_cplid/results.csv` 行数 = 100 | ⬜ |
| 3 | ONNX 导出 | `runs/yolo12n_cplid/weights/best.onnx` > 1MB | ⬜ |
| ... | ... | ... | ⬜ |
```

**禁止**：
- ❌ 不对照原始目标就开始执行
- ❌ 执行和目标无关的"顺便"任务
- ❌ 子任务没有对应的磁盘验证路径

### 铁律 6：每轮结束必须写 Checkpoint + 下轮计划

**问题**：上下文压缩后，下一轮完全不知道上一轮做了什么、做到哪了、下一步做什么。

**强制产出文件**：每轮 Goal 结束前，必须写入 `outputs/goal-checkpoints/round-N.md`

```markdown
# Goal Checkpoint — Round N

## 时间
YYYY-MM-DD HH:MM

## 本轮完成的子任务
| # | 子任务 | 产出路径 | 验证状态 |
|---|--------|---------|---------|
| 1 | xxx | `path/to/file` | ✅ 已验证（len=X） |

## 本轮未完成/遇到问题的子任务
| # | 子任务 | 问题描述 | 解决方案 |
|---|--------|---------|---------|
| 2 | xxx | 具体问题 | 下轮如何解决 |

## 磁盘变化摘要
- 新增文件：[list]
- 修改文件：[list]
- 删除文件：[无]

## 下轮计划（紧接本轮末尾）
| 优先级 | 子任务 | 前置条件 |
|--------|--------|---------|
| P0 | xxx | 无 |
| P1 | yyy | xxx 完成 |

## 累计进度
- 总子任务数：X
- 已完成：Y
- 进行中：Z
- 未开始：W
- 完成率：Y/X = XX%
```

**认知科学支撑**：外化记忆——《009-认知天性》§概念4："将记忆外部化到环境中"比依赖内部记忆可靠 100 倍。Checkpoint 就是 Goal 模式的外化记忆。

### 铁律 7：任务完成即停止——不要"轮次预算思维"

**问题**：9 轮 Goal 中，第 2 轮核心任务已全部完成（CPLID 训练 99.3% + ONNX 导出 + 调研报告），但因为"还有轮次预算"，后续 7 轮变成了无效重复。

**铁律**：**Goal 模式的结束条件是"子任务全部完成"，不是"轮次用完"。**

```python
# 完成判定逻辑
def should_continue(round_n, max_rounds, subtasks):
    completed = [t for t in subtasks if t['status'] == 'done']
    remaining = [t for t in subtasks if t['status'] != 'done']

    if len(remaining) == 0:
        return False, "所有子任务已完成，Goal 模式结束"

    if round_n >= max_rounds:
        return False, f"已达最大轮次 {max_rounds}，剩余 {len(remaining)} 个子任务"

    return True, f"继续：{len(remaining)} 个子任务待完成"
```

**GOAL_STATUS 判定规则**：
- `complete` = 所有子任务都有磁盘验证证据证明已完成
- `continue` = 还有子任务未完成且未达轮次上限
- `blocked` = 确实需要人工介入（不是"我想不出下一步"）

**禁止**：
- ❌ 任务完成后继续"优化"（除非用户明确要求）
- ❌ 因为"还有预算"就继续跑（预算 ≠ 必须用完）
- ❌ 把"已经做过了"当"已经验证了"

### 铁律 8：每个子任务完成后立即验证+记录，不等"最后一起"

**问题**：第 4 轮声称"数据集转换完成"但标签全是 class 0（质量灾难），直到第 8 轮才发现。

**协议**：每完成一个子任务：
1. **验证**：Glob/Read 确认磁盘状态和内容质量
2. **记录**：立即写入 checkpoint（铁律 6）
3. **判断**：验证通过 → 划掉子任务；验证失败 → 记录问题 + 调整计划

**质量验证检查清单**：
- 数据集转换后 → 抽样读 10 个标签文件，检查 class_id 是否非零且合理
- 训练启动后 → 读 results.csv 前 3 行，确认 loss 在下降
- ONNX 导出后 → 检查文件大小（>1MB）和 opset 版本
- Skill 创建后 → Read 文件确认有实质内容（>1KB）

---

## 三、上下文压缩阈值（何时开新对话）

**铁律**：以下任一条件满足时，**强制结束当前对话，开新对话**：

| 条件 | 阈值 | 原因 |
|------|------|------|
| 对话轮次 | > 15 轮 | 上下文过长，压缩后失忆严重 |
| 总 token 消耗 | > 80% 预算 | 剩余预算不够做任何实质工作 |
| 连续重复检测 | ≥ 2 轮做同一件事 | 已陷入重复循环 |
| 磁盘验证失败 | ≥ 3 次对同一文件判断错误 | 说明上下文已经完全不可信 |
| 训练长时间运行 | > 30 分钟等待 | 不应轮询，应开新对话或后台执行 |

**开新对话时必须**：
1. 写完当前 round 的 checkpoint
2. 在 checkpoint 末尾注明"对话结束原因"
3. 新对话第一句话引用上一个 checkpoint 文件路径

---

## 四、li- 改进机制接入

### 每轮结束必须执行

```
Step 5a: 写 checkpoint（铁律 6）
Step 5b: 检查本轮是否有教训 → 有则写入 memory/{today}.md
Step 5c: 检查教训是否需要回写 Skill/SOP → 需要则执行（F6 铁律）
Step 5d: 评估是否需要开新对话（阈值检查）
```

### 教训自动沉淀路径

```
发现踩坑
  → 立即记入 checkpoint 的"问题"列
  → 对话结束前汇总到 memory/{today}.md
  → 同类教训 ≥2 次 → 回写到对应 SOP/Skill
  → 同类教训 ≥3 次 → 升级为 .claude/rules/ 级规则
```

---

## 五、Goal 模式轮次执行模板

```markdown
## Round N 开始

### Step 0: 磁盘验证
[运行 Python 验证脚本，记录 EXISTS/NOT FOUND]

### Step 1: 计划对齐
[读取原始目标 → 分解子任务 → 对照磁盘状态 → 划掉已完成]

### Step 2: 路由扫描
[扫描 skill-routing-table.json → 匹配 → 调用]

### Step 3: 执行
[逐个执行未完成子任务]
- 子任务 1：[操作] → [验证] → ✅/❌
- 子任务 2：[操作] → [验证] → ✅/❌

### Step 4: 完成判定
[检查是否所有子任务都已完成 → 是则 GOAL_STATUS: complete]

### Step 5: Checkpoint + 下轮计划
[写 outputs/goal-checkpoints/round-N.md]
[评估是否有教训 → 写入 memory]
[评估是否需要开新对话]
```

---

## 六、教训来源（从 9 轮事故提炼）

| 轮次 | 事故 | 根因 | 对应铁律 |
|------|------|------|---------|
| 1 | 路由扫描被跳过 | Goal 模式误解"不做管理动作" | 铁律 0 |
| 2 | 最佳轮次，但后续没锚定 | checkpoint 缺失 | 铁律 6 |
| 3 | CPLID 已存在但重新下载 | 磁盘未验证 | 铁律 1 |
| 4 | 标签全是 class 0 | 转换后没验证质量 | 铁律 8 |
| 5 | 不知道 v2 何时跑出来的 | 上下文断裂 | 铁律 6 |
| 6 | 只是汇报，没有新产出 | 完成判定缺失 | 铁律 7 |
| 7 | 又重新下载 CPLID | 磁盘未验证 | 铁律 1 |
| 8 | 又又重新下载 CPLID | 磁盘未验证 + 计划脱节 | 铁律 1+5 |
| 9 | 又又又重新下载 CPLID | 磁盘未验证 + 计划脱节 + 不停止 | 铁律 1+5+7 |

**总计浪费**：~1GB 带宽 + ~250 万 token + 3 次 Skill 改进丢失 + 7 轮无效劳动

---

## 七、版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-06-12 | v2.0 | **重大重写**：新增铁律 5（计划对齐）、铁律 6（Checkpoint）、铁律 7（完成即停）、铁律 8（逐步验证）；新增 §三 上下文压缩阈值（开新对话条件）；新增 §四 li-改进机制接入；新增 §五 轮次执行模板 |
| 2026-06-12 | v1.1 | 新增铁律 0：Goal 模式不豁免路由扫描 |
| 2026-06-12 | v1.0 | 从 Goal 模式 9 轮事故中提炼，关联 F10/F11 |
