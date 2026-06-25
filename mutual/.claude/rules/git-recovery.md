# Git 检查点与恢复规则（数据安全 — 最高优先级）

> 任何被 AI 误删的文件，必须能在 30 秒内从 Git 恢复。
> 本规则确保：删前有快照，删后能恢复。

---

## 铁律

### 1. 删文件前：必须先 commit 检查点

**在以下操作之前**，必须先执行 git commit（称为"检查点提交"）：
- 删除文件（rm / remove / 删除目录）
- 覆写整个文件（write_project_file 替换已有内容）
- 批量移动/重命名文件
- 执行任何包含删除操作的脚本
- 清理目录

**检查点提交格式**：
```bash
git add -A
git commit -m "checkpoint: pre-<操作描述> ($(date))"
```

**不执行检查点就删除 = 违规。没有"这次很简单不用备份"的例外。**

### 2. 发现误删后：立即从 Git 恢复

恢复流程：
```bash
# 查看被删文件
bash scripts/git-recover.sh --list .

# 恢复单个文件
bash scripts/git-recover.sh <文件相对路径>

# 恢复最近一次提交中所有被删文件
bash scripts/git-recover.sh --all
```

恢复后必须：
1. 确认文件内容完整（Read 文件）
2. `git add` + `git commit` 保存恢复

### 3. 恢复后：记录到负结果日志

每次误删恢复后，记录到 `negative-results.md`：
```markdown
## [日期] 误删：[文件路径]
- 操作：[做了什么导致误删]
- 发现时间：[多久后发现]
- 恢复方式：[git checkout / git restore]
- 根因：[为什么删错了]
- 预防措施：[如何避免再次发生]
```

### 4. 忽略规则也是恢复风险

`.gitignore`、`git rm --cached`、批量清理脚本会制造一个隐蔽风险：文件仍在本地时看似安全，但一旦 AI 或脚本误删，Git 不再负责恢复。

**以下对象禁止默认忽略或取消跟踪**：
- `.tmp/`
- `**/.tmp/`
- `*.pyd`
- 任何 AI 生成中间产物、转换依赖、运行时插件、可复现性未知的二进制文件

执行前必须完成：
1. `git status --porcelain -uall` 与 `git ls-files` 双查，确认是否已跟踪
2. 输出清单：路径、大小、mtime、用途推断、恢复来源
3. 建立恢复点：归档 commit/tag 或单独归档包
4. 证明可再生成：安装脚本/锁文件/下载来源/生成命令至少有一项
5. 未证明可再生成时，默认保留跟踪，不加入 ignore

**口诀**：看起来临时 ≠ 没价值；忽略前先证明可恢复。

---

## 检查点策略

### 必须检查点的场景

| 场景 | 检查点方式 |
|------|-----------|
| 删除单个文件 | `git add -A && git commit -m "checkpoint: pre-delete <file>"` |
| 删除目录 | 同上，先 commit 再删 |
| 批量清理（>5 个文件） | commit + 列出清单给用户确认 |
| 覆写已有文件 | 先 commit 旧版本，再 Write |
| 执行清理脚本 | 脚本执行前 commit |

### 可以跳过检查点的场景

| 场景 | 原因 |
|------|------|
| 创建新文件 | 不涉及已有数据 |
| 修改文件的几行（用 Edit） | Edit 是精确替换，不删数据 |
| 工作区无未提交变更 | 最近一次 commit 就是快照 |

---

## 恢复工具

**脚本位置**：`scripts/git-recover.sh`

| 命令 | 用途 |
|------|------|
| `bash scripts/git-recover.sh --list [目录]` | 列出最近删除的文件 |
| `bash scripts/git-recover.sh --diff <文件>` | 查看文件修改历史 |
| `bash scripts/git-recover.sh --all` | 恢复最近一次提交中所有被删文件 |
| `bash scripts/git-recover.sh <文件路径>` | 恢复指定文件 |

---

## 与自动提交的配合

- **自动提交频率**：每 2 小时（NiumaAutoCommit 定时任务）
- **最大数据丢失窗口**：2 小时（如果 AI 没有执行检查点）
- **有检查点时**：0 数据丢失

**理想流程**：
```
AI 要删文件
  → 执行检查点 commit
  → 删除文件
  → 发现删错了
  → git-recover.sh 恢复
  → 验证文件完整
  → commit 恢复结果
```

---

## 违规检测信号

如果出现以下任何情况，说明检查点规则被违反了：
- [ ] 删除文件前没有 git commit
- [ ] 用户问"我的文件去哪了"时 AI 无法恢复
- [ ] AI 说"文件已经被删了，无法恢复"（在有 Git 的情况下）
- [ ] 恢复后没有验证文件内容是否完整

---

> 创建日期：2026-05-26
> 来源：用户需求"AI 发现删错文件时可以通过 Git 备份恢复"
> 相关规则：no-blind-overwrite.md, script-safety-check.md
