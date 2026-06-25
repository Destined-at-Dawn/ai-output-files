# 隐私脱敏与信息泄露防护规则（Privacy Sanitization）

> **优先级**：最高（等同于 script-safety-check.md）
> **创建日期**：2026-05-26
> **来源**：GitHub 公开仓库发布中多次出现个人信息泄露风险
> **触发条件**：任何文件进入公开仓库 / 任何文件推送到 GitHub Public

---

## 铁律

**任何文件推送到公开仓库之前，必须通过脱敏扫描。没有"这次内容很简单不用扫"的例外。**

---

## 一、个人信息扫描清单（必须 grep 的关键词）

### 第一梯队：致命级（出现 = 禁止推送）

| 关键词 | 类型 | 替换方案 |
|--------|------|---------|
| `小黎` / `李兰源` / `兰源` | 姓名 | `[用户名]` / `your-name` |
| `13975` | 用户 ID | `[user-id]` |
| `C:\Users\13975` | 本地路径 | `[home]` / `/home/user` |
| `E:\ai产出` | 本地路径 | `[workspace]` / `~/workspace` |
| `.newmax` | 平台路径 | `[platform]` |
| `3.896` / `3.9/4.0` | GPA | `[GPA]` |
| `上海电力大学` / `上电` / `SUEP` | 学校 | `[学校]` / `your-university` |
| `上交` / `东南` | 目标院校 | `[目标院校]` |
| `常州市局` / `国网` | 职业目标 | `[目标单位]` |
| `威泊` | 实习公司 | `[实习公司]` |
| `集创赛` / `ICAN` / `皮影戏` | 竞赛 | `[竞赛名]` |

### 第二梯队：重要级（出现 = 需要人工判断）

| 关键词 | 类型 | 处理方式 |
|--------|------|---------|
| `wxid_` / `wechat` | 微信 ID | 删除或替换 |
| `飞书` / `feishu.cn` | 飞书链接 | 判断是否为公开链接 |
| `arXiv` 论文链接 | 学术链接 | 通常可保留 |
| 具体课程名/教师名 | 教育信息 | 按需脱敏 |
| 具体日期（非版本日期） | 时间信息 | 判断是否关联到个人 |

### 第三梯队：注意级（检查即可）

| 关键词 | 类型 | 处理方式 |
|--------|------|---------|
| `git config user.name/email` | Git 配置 | 确认用公开信息 |
| `GitHub token` / `gh auth` | 认证信息 | 绝对禁止 |
| `.env` 文件 | 环境变量 | 绝对禁止 |

---

## 二、文件级黑名单（禁止进入公开仓库）

以下文件/目录**绝对禁止**出现在 GitHub Public 仓库中：

```
memory/                    # 记忆文件（含个人信息、对话记录）
outputs/                   # 产出文件（可能含未脱敏内容）
CLAUDE.md                  # 工作区配置（含个人信息、路径）
.newmax/                   # 平台配置
.telos/                    # 个人身份档案
*.env                      # 环境变量
.env.*                     # 环境变量变体
credentials*               # 凭证文件
secrets*                   # 密钥文件
```

---

## 三、扫描脚本（每次推送前执行）

```bash
#!/bin/bash
# privacy-scan.sh - 隐私扫描脚本
# 用法：bash scripts/privacy-scan.sh [目录]

SCAN_DIR="${1:-.}"
FAIL=0

echo "=== 隐私扫描开始 ==="
echo "扫描目录：$SCAN_DIR"

# 第一梯队扫描
echo ""
echo "--- 第一梯队：致命级 ---"
for keyword in "小黎" "李兰源" "兰源" "13975" "C:\\\\Users\\\\13975" "E:\\\\ai产出" ".newmax" "3.896" "上海电力" "上电" "SUEP" "威泊"; do
    result=$(grep -ril "$keyword" "$SCAN_DIR" 2>/dev/null | grep -v ".git/" | head -5)
    if [ -n "$result" ]; then
        echo "🔴 发现：$keyword"
        echo "   文件：$result"
        FAIL=1
    fi
done

# 文件级黑名单检查
echo ""
echo "--- 文件级黑名单 ---"
for blocked in "memory/" "outputs/" "CLAUDE.md" ".newmax/" ".telos/" ".env"; do
    if [ -e "$SCAN_DIR/$blocked" ]; then
        echo "🔴 黑名单文件存在：$blocked"
        FAIL=1
    fi
done

echo ""
if [ $FAIL -eq 1 ]; then
    echo "❌ 扫描失败：发现隐私泄露风险，禁止推送"
    exit 1
else
    echo "✅ 扫描通过：未发现隐私泄露"
    exit 0
fi
```

---

## 四、脱敏替换规则

| 原始内容 | 替换为 | 说明 |
|---------|--------|------|
| `小黎` | `[用户名]` 或 `your-name` | 姓名脱敏 |
| `C:\Users\13975` | `[home]` 或 `/home/user` | 路径脱敏 |
| `E:\ai产出文件\牛马` | `[workspace]` 或 `~/workspace` | 工作区脱敏 |
| `上海电力大学` | `[学校]` 或 `your-university` | 学校脱敏 |
| `3.896/3.9` | `[GPA]` 或 `your-gpa` | 成绩脱敏 |
| `威泊机器人` | `[实习公司]` 或 `robotics-company` | 公司脱敏 |
| 具体微信/飞书 ID | 删除 | 不保留 |

---

## 五、README/文档中的脱敏

公开仓库的 README、文档、注释中：

- ✅ **可以写**：通用技术描述、功能列表、使用方法、架构图
- ❌ **禁止写**：个人经历细节、具体学校/公司名、成绩、竞赛名
- ⚠️ **需要判断**：GitHub 链接（指向其他公开仓库可以）、博客链接（如果是公开的可以）

---

## 六、事故响应

如果已经推送了含个人信息的内容到公开仓库：

```
1. 立即 gh repo edit {name} --visibility private（先隐藏）
2. 用 git rebase / git filter-branch 清除敏感 commit
3. git push --force（此时安全，因为仓库已 private）
4. 重新扫描确认干净
5. 用户确认后再 public
6. 记录到 memory 作为教训
```

---

## 与相关规则的关系

| 规则 | 关系 |
|------|------|
| `CLAUDE-技能规则.md` § 三十 | 本规则是 § 三十 "发布前安全检查" 的详细展开 |
| `script-safety-check.md` | 同级安全规则——一个管脚本安全，一个管信息安全 |
| `git-recovery.md` | 互补——一个防误删，一个防泄露 |
| `no-blind-overwrite.md` | 互补——一个防盲目覆写，一个防盲目公开 |

---

## 迭代日志

| 日期 | 变更 | 版本 |
|------|------|------|
| 2026-05-26 | 初版，基于 GitHub 发布中多次出现的脱敏问题 | v1.0 |
