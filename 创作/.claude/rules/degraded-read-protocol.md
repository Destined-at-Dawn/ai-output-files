# 降级读取协议（Degraded Read Protocol）

> **优先级**：高（与 script-safety-check.md 同级）
> **创建日期**：2026-06-07
> **来源**：教训 086 §二2.3——Read 工具失败后盲目重试同一方法，锚定效应导致不愿切换策略
> **触发条件**：Read 工具返回错误/空内容/乱码时

---

## 铁律

**Read 工具失败后，同一方法最多试 2 次。第 2 次仍失败 = 必须换方法。禁止重试 3 次以上。**

---

## 决策树

```
Read 工具失败？
  ├── 第 1 次失败（文件不存在 / 权限错误 / 编码错误）
  │   └── 检查文件路径是否正确
  │       ├── 路径正确 → 换 Python open(encoding='utf-8')
  │       └── 路径可能有误 → os.path.exists() 确认文件存在
  │
  ├── 第 2 次失败（Python 也失败）
  │   └── 检查文件是否可读
  │       ├── os.path.exists() → False → 检查路径编码（中文路径常见问题）
  │       ├── os.path.exists() → True → 检查文件编码（可能是 GBK/UTF-16）
  │       └── 换编码重试：utf-8 → gbk → utf-16 → latin-1
  │
  └── 第 3 次仍失败 → 🔴 报告用户，不盲目重试
      └── 输出："无法读取 {路径}，原因：{最后一次错误}，需要你手动确认文件状态。"
```

---

## 根因：锚定效应

「系统1是自动的、快速的、直觉的、无意识的。」——《思考，快和慢》

第一次使用的方法成为"锚点"——即使失败了，系统1也不愿意放弃已投入的认知成本（沉没成本）。
AI 会不断重试同一方法，因为切换方法需要系统2的干预，而系统2是懒惰的。

**解决方案**：本规则强制在第二次失败时切换到系统2——必须换 Python，不能再盲试 Read。

---

## 禁止模式

| 禁止操作 | 原因 |
|----------|------|
| Read 失败后用 Bash cat/head/tail 再试同一文件 | 底层原因相同（路径/编码问题），不会突然变好 |
| 同一文件用 Read 重试 3+ 次 | 锚定效应——不愿意承认第一次选的方法错了 |
| "再试一次，可能刚才有问题" | 确定性错误不会因为重试变好——只有概率性错误（网络超时等）值得重试 |
| 不验证文件是否存在就换方法 | 换方法之前必须先确认文件存在——否则可能追一个不存在的文件 |

---

## 正确模式

**第 1 次 Read 失败** → Python 验证文件存在：
```python
import os
path = r"文件路径"
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"OK: {len(content)} chars")
else:
    print(f"MISSING: {path}")
```

**第 2 次 Python 也失败** → 检查编码：
```python
# 尝试不同编码
for enc in ['utf-8', 'gbk', 'utf-16', 'latin-1']:
    try:
        with open(path, 'r', encoding=enc) as f:
            content = f.read(100)
        print(f"SUCCESS with {enc}: {content[:50]}...")
        break
    except:
        continue
```

**文件确实不存在** → 检查拼写和路径：
```python
import glob
# 检查同目录下类似文件
dir_path = os.path.dirname(path)
pattern = os.path.basename(path)[:10] + "*"
matches = glob.glob(os.path.join(dir_path, pattern))
print(f"Similar files: {matches}")
```

---

## 自检清单

Read 失败后：

- [ ] 第 1 次失败 → 已换 Python？
- [ ] Python 失败 → 已确认文件存在？
- [ ] 文件不存在 → 已检查路径编码/中文路径？
- [ ] 已尝试不同编码？
- [ ] 第 3 次仍失败 → 已报告用户（不继续盲试）？
- [ ] 没有用同一方法重试 3+ 次？

---

## 与相关规则的关系

| 规则 | 关系 |
|------|------|
| `chinese-path-safety.md` | 互补——中文路径是 Read 失败的高频根因 |
| `script-safety-check.md` | 同级安全规则 |
| `see-name-stop.md` | 同级门禁规则 |
| 教训 086 §二2.3 | 来源——降级读取机制在此首次定义 |

---

## 迭代日志

| 日期 | 变更 | 版本 |
|------|------|------|
| 2026-06-07 | 初版。来源：教训 086（分段整理逐字稿 道法术器深度拆解）中的降级读取机制，从教训文件中的协议升级为独立规则。引用《思考，快和慢》（锚定效应）。 | v1.0 |
