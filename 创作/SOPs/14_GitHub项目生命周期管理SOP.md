# SOP-14：GitHub 项目生命周期管理 SOP

> **适用场景**：创建/更新/维护 GitHub 公开仓库、发 Release、同步代码、项目退役
> **触发词**：github / 仓库 / release / 开源 / 推送 / 同步 / 发布
> **前置读取**：`_system/rules/CLAUDE-技能规则.md` § 三十（GitHub 开源发布铁律）
> **创建日期**：2026-05-26
> **版本**：v1.0

---

## 一、项目分类（推送前必做）

| 分类 | 目标仓库 | 示例 | .gitignore 要求 |
|------|---------|------|-----------------|
| **A 公开框架** | GitHub Public | niuma-engine, career-breakthrough | 严格脱敏（见隐私规则） |
| **B 公开工具** | GitHub Public | obsidian-ai-toolkit, research-daily | 严格脱敏 |
| **C 私有工作区** | GitHub Private 或本地 | 创作工作区, 个人项目 | 不公开即可 |
| **D 归档项目** | GitHub Private + Archive | 已完成的项目 | 只读，不再更新 |

**铁律**：A/B 类仓库必须先 Private → 检查 → 用户确认 → 才能 Public。

---

## 二、新项目发布流程（A/B 类）

### 阶段 1：创建与脱敏

```
1. gh repo create {name} --private --description "{中文描述}"
2. 本地 git init + 配置 .gitignore
3. 隐私扫描（调用 privacy-sanitization 规则）
   - grep 扫描：13975 / 小黎 / 上海电力 / 兰源 / C:\Users / E:\ai产出
   - 检查 README/LICENSE/.gitignore 是否齐全
4. git add + git commit
5. git push -u origin main
```

### 阶段 2：Release 发布

```
1. 确定版本号（语义化：v1.0.0 / v2.0.0）
2. gh release create {version} --title "{版本名}" --notes "{更新说明}"
3. gh release upload {version} {asset-files}
   - 注意：Asset 文件名必须用英文（GitHub API 不支持中文文件名）
4. 验证：gh release view {version}
```

### 阶段 3：公开确认

```
1. 列出仓库 URL + Release URL + 文件清单
2. 通知用户检查
3. 用户明确说"public"/"公开"/"可以了"
4. gh repo edit {name} --visibility public
5. 验证：gh repo view {name} --json visibility
```

### 阶段 4：发布后验证（铁律）

```bash
# 1. 确认可见性
gh repo view {owner}/{repo} --json visibility,name,description

# 2. 确认文件列表
gh api repos/{owner}/{repo}/contents --jq '.[].name'

# 3. 确认无敏感文件
gh api repos/{owner}/{repo}/contents --jq '.[].name' | grep -iE "memory|CLAUDE|personal|identity"

# 4. 确认 Release
gh release list --repo {owner}/{repo}
```

---

## 三、已有项目更新流程

### 3.1 内容更新（加文件/改文件）

```
1. cd 到本地仓库目录
2. git pull（先拉最新）
3. 修改/新增文件
4. 隐私扫描（新增文件必做）
5. git add + git commit（Conventional Commits 格式）
6. git push
7. 判断是否需要新 Release → 是则走 § 三.3
```

### 3.2 版本升级（发新 Release）

```
1. 确定版本号（参考 CHANGELOG.md 或 commit 历史）
2. 更新 CHANGELOG.md（如有）
3. git add + git commit + git push
4. gh release create {new-version} --title "{版本名}" --notes "{更新说明}"
5. gh release upload {new-version} {new-assets}（如有新 asset）
6. 验证：gh release view {new-version}
```

### 3.3 批量 Release 补发（存量项目无 Release）

```
1. gh release list --repo {owner}/{repo}（确认当前状态）
2. 如果无 Release：
   a. git log --oneline -5（看最近 commit）
   b. gh release create v1.0.0 --title "Initial Release" --notes "首次发布"
   c. gh release upload v1.0.0 {核心文件}
3. 验证
```

---

## 四、防误删与恢复机制

### 4.1 本地 Git 防误删

- **自动提交**：每 2 小时自动 commit（smart-commit.sh）
- **检查点提交**：删除文件前必须先 commit（见 `git-recovery.md` 规则）
- **恢复脚本**：`scripts/git-recover.sh`（30 秒内恢复任何被删文件）

### 4.2 远程同步防物理损坏

| 场景 | 推送目标 | 频率 |
|------|---------|------|
| A/B 类公开项目 | GitHub Public | 每次更新后 |
| C 类私有工作区 | GitHub Private | 每日一次 |
| 关键配置文件 | GitHub Private | 每次修改后 |

### 4.3 恢复流程

```bash
# 列出最近删除的文件
bash scripts/git-recover.sh --list .

# 恢复单个文件
bash scripts/git-recover.sh <文件相对路径>

# 恢复最近一次提交中所有被删文件
bash scripts/git-recover.sh --all
```

---

## 五、项目退役流程

```
1. gh repo edit {name} --visibility private（先隐藏）
2. gh repo archive {name}（归档，只读）
3. 本地备份：tar -czf {name}-archive.tar.gz {dir}
4. 归档到：E:\ai产出文件\牛马\归档\
```

---

## 六、隐私安全检查清单（每次发布必过）

> 详细规则见 `.claude/rules/privacy-sanitization.md`

| # | 检查项 | 工具 |
|---|--------|------|
| 1 | 姓名/学号/GPA | `grep -riE "小黎\|兰源\|13975\|3\.896\|3\.9"` |
| 2 | 文件路径泄露 | `grep -riE "C:\\Users\|E:\\ai产出\|\.newmax"` |
| 3 | 学校信息 | `grep -riE "上海电力\|上电\|SUEP"` |
| 4 | memory/ 目录 | `ls` 确认不在线上仓库 |
| 5 | CLAUDE.md | `ls` 确认不在线上仓库 |
| 6 | .gitignore 完整性 | 确认排除了 memory/ outputs/ CLAUDE.md .newmax/ |

---

## 七、现有仓库盘点与维护清单

| 仓库 | 类型 | Release | 下次操作 |
|------|------|---------|---------|
| career-breakthrough | B | ✅ v1.0.0 + v2.2.0 | 正常维护 |
| research-daily | B | ✅ v1.0.0 + v2.2.0 | 正常维护 |
| obsidian-ai-toolkit | B | ✅ v1.0.0 | 正常维护 |
| niuma-engine | A | ✅ v1.0.0 + v3.0 | 正常维护 |
| niuma-ecosystem | C | 无 | ⚠️ 设为 private 或删除 |
| mutual | C | 无 | ⚠️ 设为 private 或删除 |

---

## 认知科学支撑

| 认知机制 | 来源 | 在本 SOP 中的应用 |
|---------|------|-------------------|
| **检查清单效应** | 《清单革命》 | 每次发布必过隐私检查清单——飞行员不靠记忆靠清单，AI 也不应该靠"我觉得没问题" |
| **预承诺策略** | 《WOOP》| Private 先行铁律——在 AI 产生"直接 public"的冲动之前，用流程"绑住手" |
| **冗余设计** | 《反脆弱》| 本地 Git + 远程 GitHub 双重备份——单点故障不会导致数据丢失 |
| **外部化工作记忆** | 《认知负荷理论》| CHANGELOG/Release Notes = 项目记忆的外部化——不依赖人的回忆 |

---

## 迭代日志

| 日期 | 变更 | 版本 |
|------|------|------|
| 2026-05-26 | 初版，整合技能规则 § 三十 + AGENT.md Git Workflow + 防误删机制 | v1.0 |
