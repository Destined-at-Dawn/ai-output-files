# 对外交付脱敏门禁（Outbound Delivery Sanitization）

> 优先级：高（与 no-blind-overwrite / script-safety-check 同级）
> 创建：2026-06-19
> 来源：给超算中心朋友打包"高密度学习材料工作流"资料包时，完整复制本机 li-* skill 的 SKILL.md，内嵌 `C:/Users/13975`、`E:\ai产出文件`、`小黎`、`考研`、`telos` 等可反推身份的串。脱敏扫描发现 9 个文件命中。

---

## 铁律

**任何要离开本机、交付给外部对象的资料包，发送前必须过脱敏门禁。门禁不过 = 禁止发送。**

"外部对象"包括：朋友 / 客户 / 同学、开源仓库、云盘分享、邮件附件、上传任何第三方平台。

---

## 触发条件

命中任一即触发：

- 打包 skill / SOP / memory / 文档 / 脚本给外人
- 上传 GitHub / Gitee / 任何公开或半公开仓库
- 发给客户 / 合作方 / 同学的交付物
- **特别高危**：完整复制本机 `~/.newmax/skills/`、`~/.codex/skills/`、`~/.claude/skills/` 下的 SKILL.md——这些文件几乎必然内嵌本机绝对路径和个人信息

---

## 强制流程（五步，不可跳过）

```
1. dry-run 扫描   → 列出所有命中文件 + 模式 + 次数（不改动）
2. apply 替换     → 敏感串替换为占位符（{HOME}/{USER}/{ROOT}/{USER_NAME}…）
3. 重扫验证       → RESIDUAL_HITS 必须 = 0，否则补模式重跑
4. 删构建临时报告 → _build_report.json / _sanitize_report.json 等不得留在包里
5. 人工复核       → 命中最多的 Top 3 文件人眼再看一遍（模式匹配会漏变体）
```

中文路径全程用 Python（见 [[chinese-path-safety]]）；替换脚本先 dry-run（见 [[script-safety-check]]）。

---

## 敏感模式清单（最小集，按需扩充）

| 类别 | 模式示例 | 替换占位符 |
|------|---------|-----------|
| 用户名路径 | `C:\Users\<name>`、`Users/<name>` | `{HOME}` |
| 用户名串 | 纯数字/字母用户名 | `{USER}` |
| 盘符工作区 | `E:\ai产出文件\牛马`、`E:/...` | `{ROOT}` |
| 真实姓名 | 中文名 / 昵称 | `{USER_NAME}` |
| 机构 | 学校 / 公司 / 单位名 | `{UNIVERSITY}`/`{ORG}` |
| 职业目标 | 考研 / 考公 / 目标岗位 | `{EXAM}` |
| 个人档案 | telos / 邮箱 / 电话 | `{PROFILE}` |

---

## 禁止事项

- ❌ 未脱敏直接发送
- ❌ 只跑 dry-run 不 apply 就声称"已脱敏"
- ❌ apply 后不重扫验证 RESIDUAL=0
- ❌ 把构建临时报告（含本机路径）留在交付包里
- ❌ 只信任脚本、跳过人工复核高命中文件

---

## 与现有规则的关系

| 规则 | 关系 |
|------|------|
| [[no-blind-overwrite]] | 脱敏修改的是**副本**，原 skill 在 skills 目录完好；但替换前仍须确认改的是包内副本而非原件 |
| [[chinese-path-safety]] | 脱敏脚本处理中文路径必须用 Python，脚本文件落英文路径避免 bash 编码炸 |
| [[script-safety-check]] | 替换脚本先 dry-run 再 apply，符合"写脚本→检查→dry-run→执行→验证" |

---

## 违规检测信号

- [ ] 交付包里能搜到本机用户名 / 盘符 / 真实姓名
- [ ] 包内残留 `_build_report.json` / `_sanitize_report.json`
- [ ] 声称"已脱敏"但没有 RESIDUAL=0 的重扫证据
