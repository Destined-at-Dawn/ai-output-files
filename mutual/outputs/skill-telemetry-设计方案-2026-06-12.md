# Skill 遥测 + 项目脉搏系统 · 完整设计方案

> 日期：2026-06-12 ｜ 作者：li-research ｜ 状态：待审核（审完再动手建）
> 决策前提：① 两套工具（Newmax + Claude Code）**共享同一份数据** ② 顺序硬约束 数据采集→看板→优化

---

## 0. 为什么要建（一句话根因）

你现在有 **三套残缺的追踪系统**，没一套在真正工作：

| 系统 | 实际状态 | 致命缺陷 |
|------|---------|---------|
| `.claude.json → skillUsage` | 真自动，18 个技能 | 只在「原生选择器」点击时 +1，**路由/关键词触发不计数**（漏掉 90% 实际调用）|
| `skill-usage-log.md` | 手写，停更 06-08 | 表头自称「自动记录」=**假自动** |
| `skill-ledger.db` | 22 行 | **只是安装目录**，零调用数据 |
| `hermes-tasks.db` | 0 行 | 建好从没写入 |

**实测：106 个已安装技能里，96 个调用次数 = 0。** 整套 `li-*` 生态在原生计数器里一次没出现。

→ 结论：**先有真实全量采集，才谈得上"高频/低频/我在忙啥/怎么优化"。**

---

## 1. 总体架构（一份数据，多源写入）

```
                    ┌─────────────────────────────────────┐
                    │  共享数据中枢（唯一真相源）            │
                    │  C:\Users\13975\.skill-telemetry\     │
                    │     telemetry.db   (SQLite)           │
                    └─────────────────────────────────────┘
                       ▲          ▲              ▲
        ┌──────────────┘          │              └──────────────┐
        │ 源A：实时              │ 源B：批量同步        │ 源C：脉搏聚合
   ┌────┴─────┐          ┌───────┴────────┐    ┌──────┴───────┐
   │Claude Code│          │ Newmax          │    │ li-pulse      │
   │PreToolUse │          │ skill-sync.py   │    │ 读DB+memory   │
   │hook(Skill)│          │ 读.claude.json  │    │ +git → 看板   │
   └───────────┘          └────────────────┘    └──────────────┘
```

- **源A**：Claude Code 原生 hooks，每次 Skill 调用实时落库（最可靠）。
- **源B**：Newmax 不确定支持 hooks → 用同步脚本周期性把 `.claude.json` 增量 + 手写日志灌进 DB。
- **源C**：`li-pulse` 只读 DB + 各工作区 memory + git，产出「我在忙什么」看板。

---

## 2. 数据库 Schema

文件：`C:\Users\13975\.skill-telemetry\telemetry.db`

```sql
-- 表1：调用流水（每次调用一行，永不删除）
CREATE TABLE IF NOT EXISTS invocations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ts          INTEGER NOT NULL,         -- Unix 毫秒
    skill       TEXT    NOT NULL,         -- 技能名
    tool        TEXT    NOT NULL,         -- 'claudecode' | 'newmax'
    workspace   TEXT,                     -- mutual/竞赛/求职/创作/个人/unknown
    trigger     TEXT,                     -- 'native' | 'routing' | 'keyword' | 'manual'
    session_id  TEXT,
    status      TEXT DEFAULT 'invoked',   -- invoked | success | fail
    UNIQUE(ts, skill, tool)               -- 防同步重复
);
CREATE INDEX IF NOT EXISTS idx_skill ON invocations(skill);
CREATE INDEX IF NOT EXISTS idx_ts    ON invocations(ts);

-- 表2：同步水位（源B去重用，记住每个技能已同步到的 lastUsedAt）
CREATE TABLE IF NOT EXISTS sync_state (
    source      TEXT PRIMARY KEY,         -- 'newmax-skillusage'
    skill       TEXT,
    watermark   INTEGER                   -- 已同步到的最大 lastUsedAt
);
```

设计要点：
- **流水表不存计数**，计数永远靠 `COUNT(*) GROUP BY skill` 实时算 → 永不失真。
- `UNIQUE(ts, skill, tool)` 让源B可反复跑而不重复插入（幂等）。

---

## 3. 源A：Claude Code 实时 Hook

### 3.1 settings.json 配置（追加，勿覆盖）

路径：`C:\Users\13975\.claude\settings.json` 的 `hooks` 段：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Skill",
        "hooks": [
          { "type": "command",
            "command": "python C:\\Users\\13975\\.skill-telemetry\\log_invocation.py" }
        ]
      }
    ]
  }
}
```

> 注：matcher 是否精确命中 Skill 工具，需在真机验证一次（不同 Claude Code 版本工具名可能为 `Skill`）。验证方法见 §7。

### 3.2 log_invocation.py（hook 脚本骨架）

```python
#!/usr/bin/env python3
# 由 Claude Code PreToolUse hook 调用，stdin 收到工具调用 JSON
import sys, json, sqlite3, time, os, re

DB = os.path.expanduser(r"~\.skill-telemetry\telemetry.db")

def detect_workspace(cwd:str)->str:
    # 用户工作区清单：mutual、竞赛、创作、个人、求职、日常学习、论文
    for k in ["mutual", "竞赛", "创作", "个人", "求职", "日常学习", "论文"]:
        if k in (cwd or ""): return k
    return "unknown"

def main():
    raw = sys.stdin.read()
    try: payload = json.loads(raw)
    except Exception: return                       # 静默失败，绝不阻塞主流程
    tool_input = payload.get("tool_input", {})
    skill = tool_input.get("skill") or tool_input.get("name")
    if not skill: return
    cwd = payload.get("cwd","")
    con = sqlite3.connect(DB)
    con.execute("""INSERT OR IGNORE INTO invocations
        (ts,skill,tool,workspace,trigger,session_id,status)
        VALUES (?,?,?,?,?,?,?)""",
        (int(time.time()*1000), skill, "claudecode",
         detect_workspace(cwd), "native",
         payload.get("session_id"), "invoked"))
    con.commit(); con.close()

if __name__ == "__main__":
    main()      # 任何异常都不得让 hook 返回非0（否则阻塞工具）
```

**铁律**：hook 脚本必须 try/except 全包、永远 exit 0，**绝不能因记录失败而打断你正常用技能**。

---

## 4. 源B：Newmax 批量同步

Newmax hook 支持不确定 → 不赌，改用**周期同步**。每次 Newmax 启动 / 定时任务跑一次。

### skill-sync.py（骨架）

```python
#!/usr/bin/env python3
# 把 Newmax 的 .claude.json→skillUsage 增量灌进共享 DB
import json, sqlite3, os

DB  = os.path.expanduser(r"~\.skill-telemetry\telemetry.db")
SRC = os.path.expanduser(r"~\.newmax\.claude.json")

def main():
    su = json.load(open(SRC, encoding="utf-8")).get("skillUsage", {})
    con = sqlite3.connect(DB)
    for skill, v in su.items():
        last = v.get("lastUsedAt", 0)
        cnt  = v.get("usageCount", 0)
        # 取该技能已同步水位
        row = con.execute(
            "SELECT watermark FROM sync_state WHERE source=? AND skill=?",
            ("newmax-skillusage", skill)).fetchone()
        wm = row[0] if row else 0
        if last > wm:
            # 原生只给总数+最后时间，无法还原每次时刻 → 用 lastUsedAt 补1条增量
            # （够用：高频榜按 COUNT 算；精确每次时刻 Newmax 原生拿不到，如实标注）
            con.execute("""INSERT OR IGNORE INTO invocations
                (ts,skill,tool,workspace,trigger,status)
                VALUES (?,?,?,?,?,?)""",
                (last, skill, "newmax", "unknown", "native", "invoked"))
            con.execute("""INSERT OR REPLACE INTO sync_state
                (source,skill,watermark) VALUES (?,?,?)""",
                ("newmax-skillusage", skill, last))
    con.commit(); con.close()

if __name__ == "__main__":
    main()
```

> **口径声明**：Newmax 原生只存「总次数+最后时间」，无法还原每一次调用的时刻。所以源B只能保证**高频榜准确**，无法给 Newmax 侧精确时间线。如要全精度，须确认 Newmax 是否支持 hook（待验证），支持就复用源A脚本。这是诚实边界，不假装。

---

## 5. 统计工具 skill-stats.py

一条命令出三张榜：

```python
#!/usr/bin/env python3
import sqlite3, os, time, argparse
DB = os.path.expanduser(r"~\.skill-telemetry\telemetry.db")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    days = ap.parse_args().days
    cut = int((time.time() - days*86400)*1000)
    con = sqlite3.connect(DB)

    print(f"=== 近{days}天 高频榜 ===")
    for s,n in con.execute(
        "SELECT skill,COUNT(*) c FROM invocations WHERE ts>=? "
        "GROUP BY skill ORDER BY c DESC LIMIT 15",(cut,)):
        print(f"{n:>3}  {s}")

    print(f"\n=== 僵尸技能榜（>{days}天 0 调用，但已安装）===")
    # 已安装清单从 ~/.newmax/skills + ~/.claude/skills 目录扫
    import glob
    installed=set()
    for base in [r"~\.newmax\skills", r"~\.claude\skills"]:
        for p in glob.glob(os.path.expanduser(base)+r"\*"):
            if os.path.isdir(p): installed.add(os.path.basename(p))
    active = {r[0] for r in con.execute(
        "SELECT DISTINCT skill FROM invocations WHERE ts>=?",(cut,))}
    zombies = sorted(installed - active)
    print(f"{len(zombies)} 个僵尸 / {len(installed)} 已安装")
    for z in zombies[:30]: print("  -",z)

if __name__ == "__main__":
    main()
```

用法：`python skill-stats.py --days 7` / `--days 30`。
→ 直接回答「哪些用得多、哪些用得少、哪些该下架」。

---

## 6. li-pulse：项目脉搏看板（诉求2）

### 定位
不是任务管理器，是**只读聚合器**：扫已有痕迹 → 回答「我在忙什么 / 进度 / 卡点 / 下一步」。

### 数据源（全部已存在，零额外维护负担）
1. 各工作区 `memory/{近7天}.md` —— 你每天的进展记录
2. `git log --since="7 days ago"` （各工作区）—— 真实产出
3. `telemetry.db` 近7天高频技能 —— 你在用什么工具 = 在做什么类型的事
4. `scheduled-tasks.db` / `hermes-tasks.db` —— 待办（如有）

### 产出（每天定时刷新一次）
`outputs/pulse-{date}.md`，结构：

```markdown
# 我在忙什么 · 2026-06-12

## 🔥 当前主线（3-5 个）
| 项目 | 工作区 | 进度 | 最近动作 | 卡点 | 下一步 |
|------|--------|------|---------|------|--------|
| YOLO竞赛 | 竞赛 | 60% | 6-12 改 SKILL | 数据集标注 | 跑baseline |
| ...

## 📊 本周技能使用 TOP5（来自遥测）
## ⚠️ 漏调提醒（该用skill却用了原生）
## 🧭 方向判断：你这周 70% 时间在「竞赛」，建议……
```

### 实现
一个 `li-pulse` skill + `pulse.py` 聚合脚本，挂 Claude Code 定时任务（`/schedule` 或 cron）每天早上跑。

---

## 7. 诉求3：数据驱动优化（必须排最后）

积累 **1-2 周真实数据**后，交给 `li-improve` 做：

| 信号 | 自动动作 |
|------|---------|
| 某技能 30 天 0 调用 | 进「僵尸候选」清单 → 你确认后软删除（DEPRECATED，不真删）|
| 某技能近 7 天 Top3 | 优先打磨/补 references |
| 漏调（指令该触发但用了原生）| 路由表补触发词 |
| 某方向连续高频 | li-pulse 升级为长期项目立项 |

> 没有 §3-5 的数据，这步=拍脑袋。**严禁提前做。**

---

## 8. 顺带清理（低风险先减熵）

| 对象 | 现状 | 动作 |
|------|------|------|
| `.newmax/shell-snapshots/` | 138 个环境快照 | 保留最近 3 个，其余备份后清 |
| `.newmax/projects/` | 26 个乱码 `proj-*` 目录 | **违反你全局 CLAUDE.md 禁令**；备份后清，改用 li-pulse |
| `skills/` 根目录 | `li-analyze.zip`/`li-devil.zip`/`_final_*.txt` | 备份到归档后清 |

> 所有清理遵守你的「备份铁律」：先备份高风险对象到 `归档/`，AI 只备份不删除，删除由你执行。

---

## 9. 落地顺序（验证驱动）

**硬约束：有 3 个假设必须真机验证，不能猜。**

```
第0.0步：验证三个硬前提（决定后续脚本写法）             [验证关键 ⚠️]
  - Claude Code 的 PreToolUse 工具名：是 "Skill" 还是别的？
  - hook stdin 实际格式：tool_input 字段叫什么？
  - shell 环境：powershell 还是别的？
  
第0.1步：建 debug 版 hook 打日志，跑一次看真实输入       [10分钟]
  脚本见 §9.A，生成 C:\Users\13975\.skill-telemetry\debug.log
  
第0.2步：根据 debug.log 修正 log_invocation.py 的解析逻辑 [5分钟]
  
第1步：建 ~/.skill-telemetry/ + telemetry.db（含 WAL）  [建库]
  脚本见 §9.B，包含 PRAGMA journal_mode=WAL 防并发
  
第2步：配 Claude Code hook，跑一个 Skill 看是否记录      [验证]

第3步：跑 skill-sync.py 把 Newmax 历史灌进来              [立即有数据]
  脚本加重试逻辑，见 §9.C
  
第4步：观察 3-7 天，确认采集真实                          [攒数据]

第5步：建 li-pulse + 定时任务                             [看板上线]

第6步：数据满 1-2 周 → li-improve 数据驱动优化            [闭环]
```

---

## 9.A 调试 Hook（第 0.1 步）

**目标**：打桩看清 stdin 真实格式，再写正式脚本。

文件：`C:\Users\13975\.skill-telemetry\debug_hook.py`

```python
#!/usr/bin/env python3
# 调试版：把 stdin 原文 + 解析结果写到日志
import sys, json, os, datetime

LOG = os.path.expanduser(r"~\.skill-telemetry\debug.log")

def main():
    ts = datetime.datetime.now().isoformat()
    raw = sys.stdin.read()
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"\n=== {ts} ===\n")
        f.write(f"RAW_STDIN_LEN: {len(raw)}\n")
        f.write(f"RAW_STDIN:\n{raw[:2000]}\n")  # 前 2000 字
        try:
            payload = json.loads(raw)
            f.write(f"PARSED_KEYS: {list(payload.keys())}\n")
            f.write(f"tool_input_keys: {list(payload.get('tool_input', {}).keys())}\n")
            f.write("SUCCESS\n")
        except Exception as e:
            f.write(f"PARSE_ERROR: {e}\n")

if __name__ == "__main__":
    main()      # 永不失败
```

**用法**：
1. 把这个脚本放到 `~/.skill-telemetry/debug_hook.py`
2. 临时改 `settings.json` hook 的 command 为 `python C:\Users\13975\.skill-telemetry\debug_hook.py`
3. 在 Claude Code 里手动调用一个 Skill（比如 `/li-bestskill`），观察一次调用
4. 检查 `~/.skill-telemetry/debug.log`，看 RAW_STDIN 和 PARSED_KEYS
5. **把 debug.log 内容反馈回来**，我据此修正正式脚本

---

## 9.B 建库脚本（第 1 步）

文件：`C:\Users\13975\.skill-telemetry\init_db.py`

```python
#!/usr/bin/env python3
import sqlite3, os

DB = os.path.expanduser(r"~\.skill-telemetry\telemetry.db")
os.makedirs(os.path.dirname(DB), exist_ok=True)

con = sqlite3.connect(DB, timeout=5)  # 并发锁超时 5 秒

# WAL 模式防并发写锁死
con.execute("PRAGMA journal_mode=WAL")
con.execute("PRAGMA synchronous=NORMAL")  # 稍微快一点，但仍安全

con.execute("""CREATE TABLE IF NOT EXISTS invocations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ts          INTEGER NOT NULL,
    skill       TEXT    NOT NULL,
    tool        TEXT    NOT NULL,
    workspace   TEXT,
    trigger     TEXT,
    session_id  TEXT,
    status      TEXT DEFAULT 'invoked',
    UNIQUE(ts, skill, tool)
)""")

con.execute("""CREATE INDEX IF NOT EXISTS idx_skill ON invocations(skill)""")
con.execute("""CREATE INDEX IF NOT EXISTS idx_ts    ON invocations(ts)""")

con.execute("""CREATE TABLE IF NOT EXISTS sync_state (
    source      TEXT PRIMARY KEY,
    skill       TEXT,
    watermark   INTEGER
)""")

con.commit()
con.close()

print(f"✓ DB 初始化完成：{DB}")
print(f"✓ WAL 模式已启用（并发写入安全）")
```

**用法**：`python init_db.py`

---

## 9.C skill-sync.py 修正版（第 3 步）

加重试逻辑处理 SQLite 锁超时。

```python
#!/usr/bin/env python3
import json, sqlite3, os, time

DB  = os.path.expanduser(r"~\.skill-telemetry\telemetry.db")
SRC = os.path.expanduser(r"~\.newmax\.claude.json")
RETRY = 3

def sync_once():
    """一次同步尝试，返回 True 如果成功"""
    if not os.path.exists(SRC):
        print(f"! {SRC} 不存在，跳过")
        return False
    
    su = json.load(open(SRC, encoding="utf-8")).get("skillUsage", {})
    con = sqlite3.connect(DB, timeout=5000)  # 5 秒超时
    
    try:
        for skill, v in su.items():
            last = v.get("lastUsedAt", 0)
            con.execute("""INSERT OR IGNORE INTO invocations
                (ts,skill,tool,workspace,trigger,status)
                VALUES (?,?,?,?,?,?)""",
                (last, skill, "newmax", "unknown", "native", "invoked"))
            con.execute("""INSERT OR REPLACE INTO sync_state
                (source,skill,watermark) VALUES (?,?,?)""",
                ("newmax-skillusage", skill, last))
        con.commit()
        print(f"✓ 同步成功：{len(su)} 个技能")
        return True
    except sqlite3.OperationalError as e:
        if "locked" in str(e).lower():
            print(f"! SQLite 锁超时：{e}（稍后重试）")
            return False
        raise
    finally:
        con.close()

def main():
    for attempt in range(1, RETRY+1):
        if sync_once():
            return
        if attempt < RETRY:
            print(f"  等待 1 秒后重试... ({attempt}/{RETRY-1})")
            time.sleep(1)
    print("! 同步失败（已重试 3 次）")

if __name__ == "__main__":
    main()
```

---

## 10. 待你执行和反馈的步骤

**现在**：
1. ✅ 审核方案 ← 你已完成
2. ⏳ **执行第 0.1 步：跑 debug_hook.py 一次**
   - 用脚本见 §9.A，临时改 hook command
   - 在 Claude Code 调一个 Skill
   - 检查 `~/.skill-telemetry/debug.log`，把 RAW_STDIN 全文反馈给我
3. ⏳ **根据 debug.log 确认三个值**：
   - `PARSED_KEYS` 里有什么（可能是 tool_name/tool_input/cwd/session_id）
   - tool_input 内容（Skill 的参数叫 skill/name/还是别的）
   
**然后**：我据此改正 log_invocation.py → 第 1-2 步可正式开始。

---

## 11. 修正项总结

| 原方案问题 | 改进 |
|---------|------|
| matcher: "Skill" 未验证 | 改为第 0.1 步 debug，看真实工具名 |
| stdin 格式假设 | debug.log 看原文，防解析错 |
| SQLite 并发 | 加 WAL 模式 + timeout=5000 + PRAGMA synchronous=NORMAL |
| shell 类型不明 | debug 脚本是纯 Python（不依赖 shell），正式脚本由你验证后再加 shell 声明 |
| detect_workspace 漏了"学习" | 待你反馈工作区完整清单，统一改 |

**这样改的好处**：没有猜测，完全靠实测驱动，风险最低。

---

## 旧的第 10 节（保留作参考）

开放问题（待日后）：

1. **共享 DB 路径**：定 `C:\Users\13975\.skill-telemetry\telemetry.db` 行不行？
2. **Newmax hook 支持**：验证后确认是否支持 PreToolUse
3. **li-pulse 刷新频率**：每天 1 次 vs 手动
4. **清理授权**：§8 清理什么时候做

---

> 口径：本文档为设计稿 `@设计层`，脚本为骨架 `@未运行`，需经第1步真机验证才能宣称「采集可用」。所有调用数据引用自 `.claude.json` 真实原生记录，但该计数器系统性低估（仅覆盖原生触发路径）——这正是本方案要修的根因。
