# 学术论文 LaTeX 模板调研报告

> 调研日期：2026-06-11
> 调研场景：学术 + 技能
> 调研方法：li-research 方法论（多平台搜索 + 官方验证）

---

## 一、调研结论

### 1.1 官方来源验证

| 模板 | 官方来源 | 版本 | 许可证 | 最后更新 |
|------|---------|------|--------|----------|
| IEEEtran.cls | [CTAN](https://ctan.org/pkg/IEEEtran) | 1.8b | LPPL 1.3 ✅ | 2015-08-28 |
| elsarticle.cls | [CTAN](https://ctan.org/pkg/elsarticle) | 3.5 | LPPL 1.3 ✅ | 2026-01-09 |
| sn-jnl.cls | [Springer Nature](https://www.springernature.com/gp/authors/campaigns/latex-author-support) | 2024-12 | 允许本地使用 ✅ | 2024-12 |

**验证结果**：三个模板均为官方最新版本，许可证允许本地存储和使用。

### 1.2 最佳存储方案

**问题**：模板放在 C 盘 skill 目录，论文写作在 E 盘 → 每次都要跨盘复制

**解决方案**：
```
E:\ai产出文件\论文\
├── templates/                    ← 官方模板库（唯一真源）
│   ├── IEEE/
│   ├── Elsevier/
│   └── Springer-Nature/
├── papers/                       ← 每篇论文独立目录
└── README.md                     ← 模板选择指南
```

**已完成**：
- ✅ 模板文件已复制到 E 盘
- ✅ 每个模板目录创建了 README 说明
- ✅ 论文目录创建了总 README.md
- ✅ li-office CATALOG.md 已更新指向 E 盘

### 1.3 关键发现

1. **IEEE Template Selector**（https://template-selector.ieee.org）是 IEEE 官方工具，可以按目标期刊选择正确模板
2. **Nature 系列没有独立 LaTeX 模板** — 使用 Springer Nature 通用模板（sn-jnl.cls），投稿时按期刊要求调整 .bst 文件
3. **Elsevier 3.5 版本已预编译** — 无需再从 .dtx 生成 .cls
4. **学术论文项目最佳组织方式**（基于 2025 年学术研究）：
   - 模块化文件结构
   - 按项目/论文独立目录
   - 语义化命名
   - figures/tables/data 分离

---

## 二、官方资源链接

### IEEE
- **Template Selector**: https://template-selector.ieee.org
- **Author Center Journals**: https://journals.ieeeauthorcenter.ieee.org
- **Author Center Magazines**: https://magazines.ieeeauthorcenter.ieee.org
- **Conference Templates**: https://www.ieee.org/conferences/publishing/templates
- **Overleaf IEEE Templates**: https://www.overleaf.com/latex/templates/tagged/ieee

### Elsevier
- **LaTeX Support**: https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions
- **CTAN Package**: https://ctan.org/pkg/elsarticle
- **Overleaf Elsevier Templates**: https://www.overleaf.com/latex/templates/tagged/elsevier

### Springer Nature
- **LaTeX Author Support**: https://www.springernature.com/gp/authors/campaigns/latex-author-support
- **Overleaf SN Template**: https://www.overleaf.com/latex/templates/springer-nature-latex-template/gsvvftmrppwq

### ML/AI 会议
- **NeurIPS 2026**: https://www.overleaf.com/latex/templates/formatting-instructions-for-neurips-2026/bjdwqfdkyftc
- **ICML 2026**: https://www.overleaf.com/latex/templates/icml2025-template/dhxrkcgkvnkt
- **arXiv**: https://www.overleaf.com/gallery/tagged/arxiv

---

## 三、模板选择指南

### 电气/电力电子
- **期刊** → IEEEtran.cls（TPEL/TIE）或 elsarticle.cls（Applied Energy/Energy）
- **会议** → IEEEtran.cls conference（APEC/ECCE）

### 具身智能/机器人
- **期刊** → IEEEtran.cls journal（TRO/RA-L）
- **会议** → IEEEtran.cls conference（ICRA/IROS）或各 ML 会议模板
- **顶刊** → sn-jnl.cls（Nature Machine Intelligence）或 Science

### 能源/化工
- **期刊** → elsarticle.cls（Applied Energy, Energy, Energy Conversion and Management）

### Nature 系列
- **期刊** → sn-jnl.cls + sn-nature.bst（Nature, Nature Communications, Nature Energy, Nature MI）

---

## 四、边界声明

### 可写入材料
- ✅ IEEEtran 1.8b、elsarticle 3.5、Springer Nature 2024-12 均为官方最新版本（证据：CTAN 页面 + Springer Nature 官网）
- ✅ 所有模板许可证允许本地存储和使用（证据：LPPL 1.3 许可证文本）
- ✅ 模板已正确迁移到 E:\ai产出文件\论文\templates\（证据：文件系统验证）

### 不可写入材料
- ⚠️ 期刊具体投稿要求可能随时间变化（原因：期刊政策会更新，需投稿前查阅官网）

### 尚不能声称
- ❓ 所有期刊是否接受本地编译的 PDF（需要：查阅目标期刊的具体投稿指南）

---

## 五、后续行动

### 立即执行
1. ✅ 模板文件已复制到 E 盘
2. ✅ README 文件已创建
3. ✅ li-office CATALOG.md 已更新

### 建议执行
1. 在 `E:\ai产出文件\论文\papers\` 下创建第一篇论文的目录结构
2. 测试模板编译是否正常（pdflatex + bibtex）
3. 考虑将 li-office 的 `references/templates/official/` 改为指向 E 盘的软链接

---

## 六、认知科学支撑

### 决策框架
- **双系统理论**：快速判断（模板选择）+ 慢速验证（官方来源确认）
- **锚定效应**：避免被 GitHub 第三方镜像锚定，坚持官方来源

### 学习机制
- **间隔重复**：模板选择指南应定期复习，直到形成肌肉记忆
- **检索式练习**：每次新建论文时，主动回忆模板选择流程而非直接查 README

---

## 七、相关资源

- **CATALOG.md**: `C:\Users\13975\.newmax\skills\li-office\references\templates\official\CATALOG.md`
- **论文目录**: `E:\ai产出文件\论文\`
- **模板目录**: `E:\ai产出文件\论文\templates\`
