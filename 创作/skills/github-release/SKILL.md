# GitHub Release Skill

> **用途**：一键为 GitHub 仓库创建/更新 Release，含隐私扫描 + 版本管理
> **触发词**：release / 发布 / 版本 / 更新github / 推送到github
> **版本**：v1.0 | **创建日期**：2026-05-26

---

## 使用方式

用户说"发 release" / "更新 github" / "推送到 github"时，AI 自动执行以下流程。

---

## Phase 1：前置检查（必须通过）

### 1.1 确认仓库状态

```bash
# 确认在 git 仓库中
git status

# 确认有远程仓库
git remote -v

# 确认 gh 已登录
gh auth status

# 查看当前 Release 列表
gh release list --repo {owner}/{repo}
```

### 1.2 隐私扫描（公开仓库必须）

```bash
# 执行隐私扫描
bash scripts/privacy-scan.sh .

# 扫描失败 → 修复后才能继续
# 扫描通过 → 进入 Phase 2
```

### 1.3 确认版本号

**版本号规则**（语义化版本）：

| 变更类型 | 版本号 | 示例 |
|---------|--------|------|
| 新功能/新文件 | Minor +1 | v1.0.0 → v1.1.0 |
| Bug 修复/小改动 | Patch +1 | v1.0.0 → v1.0.1 |
| 重大重构 | Major +1 | v1.0.0 → v2.0.0 |
| 首次发布 | v1.0.0 | - |

**确定方法**：
1. `gh release list --repo {owner}/{repo}` 查看已有版本
2. 根据变更类型确定新版本号
3. 如果无 Release，从 v1.0.0 开始

---

## Phase 2：提交与推送

```bash
# 1. 确认变更内容
git status
git diff --stat

# 2. 提交（Conventional Commits 格式）
git add -A
git commit -m "feat(scope): 更新说明"

# 3. 推送
git push origin main

# 4. 验证推送成功
git status
```

---

## Phase 3：创建 Release

```bash
# 创建 Release（含功能说明）
gh release create {version} \
  --title "{版本名}" \
  --notes "$(cat <<'EOF'
## 更新内容
- 新增：xxx
- 修复：xxx
- 优化：xxx

## 安装方式
{安装说明}

## 相关链接
- {相关仓库链接}
EOF
)"

# 上传 Asset（如有）
gh release upload {version} {file1} {file2} --clobber

# 验证 Release
gh release view {version}
```

**Asset 文件名必须用英文**（GitHub API 不支持中文文件名）。

---

## Phase 4：发布后验证

```bash
# 1. 确认 Release 存在
gh release view {version}

# 2. 确认文件列表
gh api repos/{owner}/{repo}/contents --jq '.[].name'

# 3. 确认无敏感文件
gh api repos/{owner}/{repo}/contents --jq '.[].name' | grep -iE "memory|CLAUDE|personal|identity"

# 4. 如果是新仓库，确认可见性
gh repo view {owner}/{repo} --json visibility
```

---

## Phase 5：通知用户

输出格式：

```
✅ Release 已发布

📦 仓库：https://github.com/{owner}/{repo}
🏷 版本：{version}
📝 更新说明：{简述}
📎 Asset：{文件列表}

🔗 Release 链接：https://github.com/{owner}/{repo}/releases/tag/{version}
```

---

## 批量补发 Release（存量项目无 Release）

```
1. gh release list --repo {owner}/{repo}（确认无 Release）
2. git log --oneline -5（看最近 commit）
3. gh release create v1.0.0 --title "Initial Release" --notes "首次发布"
4. gh release upload v1.0.0 {核心文件}
5. 验证
```

---

## 禁止事项

- ❌ 禁止跳过隐私扫描直接推送公开仓库
- ❌ 禁止使用 `git push --force`（除非仓库已 private 且用户确认）
- ❌ 禁止未验证就报告"已发布"
- ❌ 禁止 Asset 使用中文文件名
- ❌ 禁止 Release Notes 中包含个人信息

---

## 与相关规则/SOP 的关系

| 文件 | 关系 |
|------|------|
| `SOP-14 GitHub项目生命周期管理SOP` | 本 Skill 是 SOP-14 的自动化执行层 |
| `.claude/rules/privacy-sanitization.md` | Phase 1.2 调用的隐私扫描规则 |
| `_system/rules/CLAUDE-技能规则.md` § 三十 | 本 Skill 实现了 § 三十 的发布流程 |
| `AGENT.md` Git Workflow | 本 Skill 的 commit 格式遵循 AGENT.md |

---

## 迭代日志

| 日期 | 变更 | 版本 |
|------|------|------|
| 2026-05-26 | 初版，整合发布流程 + 隐私扫描 + 版本管理 | v1.0 |
