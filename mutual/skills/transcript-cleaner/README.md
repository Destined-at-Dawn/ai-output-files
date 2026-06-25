# 逐字稿清洗与道法术器拆解技能

把2小时的讲座录音，10分钟变成结构化的知识资产

## 核心能力（4个自动）

1. **自动识别发言人** —— 多人对话也能分段整理
2. **自动校正AI术语** —— ChatGPT不是"chatgpt"，API不是"api"，100+词条精准修正
3. **自动过滤语气词** —— 去除"对吧"、"我觉得"、"然后"等冗余表达
4. **自动结构化输出** —— 按"道法术器"框架生成会议纪要

## 使用方法

### 1. 基础使用（命令行）

```bash
# 使用道法术器格式输出
python scripts/clean_transcript.py <逐字稿文件路径> "标题" --daofashuqi

# 使用简单格式输出
python scripts/clean_transcript.py <逐字稿文件路径> "标题"
```

### 2. 转换为其他格式

```bash
# 生成HTML网页（带"树根蔓延"动画）
python scripts/generate_html.py <Markdown文件路径>

# 生成Word文档
python scripts/generate_docx.py <Markdown文件路径>

# 生成PPT演示文稿
python scripts/generate_ppt.py <Markdown文件路径>
```

### 3. 完整流程示例

```bash
# 步骤1: 清洗逐字稿并生成Markdown
python scripts/clean_transcript.py my_transcript.txt "演讲标题" --daofashuqi

# 步骤2: 转换为HTML（推荐，有动画效果）
python scripts/generate_html.py my_transcript_cleaned_cleaned.md

# 步骤3: 在浏览器中打开HTML查看
```

## 输出格式说明

### 道法术器结构

```
文章主旨概览
├── 一句话总结
└── 核心主题

第一部分：值不值得学/做（四维打分）
├── 钱（变现能力）
├── 关系（人脉链接）
├── 技能（能力获取）
└── 影响力（个人品牌）

第二部分：能学到什么（道法术器拆解）
├── 道（底层认知，跨场景复用）
├── 法（方法论框架，可迁移）
├── 术（具体执行，可直接上手）
└── 器（工具与资源）

第三部分：我的收获与行动
├── 核心收获
├── 立即行动
└── 需要深入研究
```

### 新增功能

1. **文章主旨概览** - 快速了解内容核心
2. **新颖趋势洞察** - 识别未来商业趋势
3. **四维打分** - 客观评估学习/做这件事的价值
4. **多格式输出** - 支持HTML、Word、PPT格式

## HTML网页特色

生成的HTML网页具有以下特点：

- **布局**：左侧固定导航栏，右侧内容展示区
- **动画**：点击左侧按钮，右侧内容以"树根蔓延"动画展开
- **配色**：复古大地色系（主色#8B6B4C，辅色#D4B59E，米白底#F8F5F0）
- **效果**：玻璃拟态卡片，简洁现代字体

## 依赖安装

```bash
# Word文档生成需要
pip install python-docx

# PPT生成需要
pip install python-pptx
```

## 文件结构

```
skill/
├── SKILL.md                 # 技能定义文件
├── README.md                # 使用说明
├── references/              # 参考资料
│   ├── ai_terminology.md    # AI术语词典
│   └── output_template.md   # 输出模板
└── scripts/                 # 脚本工具
    ├── clean_transcript.py  # 主清洗脚本
    ├── generate_html.py     # HTML生成脚本
    ├── generate_docx.py     # Word生成脚本
    └── generate_ppt.py      # PPT生成脚本
```

## 常见问题

**Q: 逐字稿是什么格式？**
A: 支持文本格式，最好包含发言人标记，如"主持人："、"嘉宾："等。

**Q: 如何提高识别准确率？**
A: 确保发言人标记清晰，如"主持人："、"嘉宾："、"分享者："等。

**Q: 支持哪些语言？**
A: 目前主要支持中文，但术语词典包含英文AI术语的修正。

**Q: 如何自定义术语词典？**
A: 编辑 `references/ai_terminology.md` 文件，添加需要修正的词条。

## 许可

MIT License
