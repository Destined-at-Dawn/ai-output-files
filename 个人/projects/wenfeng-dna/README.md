# 文风DNA编解码系统 v3.0

基于《文风DNA编解码手册》v3.0的完整实现，提供文风分析、生成、对比的全套工具。

## 核心功能

### 1. 文风分析 (analyze)
分析文本的文风DNA编码，提取7层编码：
- **PH哲学层**: 平均句长 + 本体论 + 时间观
- **EP认识论**: 知识来源 + 验证方式 + 真理观
- **ID意识形态**: 权力/精英/知识/技术/行动/阶层/情感 7维度
- **RH修辞层**: 论证方式 + 修辞手法 + 节奏类型
- **SY句法层**: 句长 + 复杂度 + 变化度 + 标点 + 句长分布
- **DN领域层**: 专业度 + 术语占比 + 口语占比 + 文言占比 + 领域码 + 深度
- **RD六维雷达**: 真实/权力/情感/逻辑/具体/行动

### 2. 文本生成 (generate)
根据DNA编码生成符合指定文风的文本
- 支持5种生成算法 (AL01-AL05)
- 支持10种话语模式 (PT01-PT10)
- 支持自定义词汇库
- 自动处理特殊规则和矛盾点

### 3. 文风对比 (compare)
对比两段文本的文风差异
- 6维度相似度计算
- 识别主要差异点
- 生成详细对比报告

### 4. 词汇库管理
- 4个预设领域词汇库：护肤(SK)、哲学(PH)、女性成长(FG)、教育(ED)
- 支持自定义词汇库导入导出
- 自动领域检测

### 5. 特殊规则引擎
实现v3.0手册的10条特殊规则 (RULE01-RULE10)
- 句首设问控制
- 个人经历引用
- 行动指令添加
- 评价词极端程度控制
- 转折词选择等

### 6. 矛盾点处理
自动检测和处理5大矛盾点 (CD01-CD05)
- 权威 vs 平等
- 理性 vs 感性
- 批判 vs 建设
- 普世 vs 个性
- 专业 vs 通俗

## 安装

```bash
cd wenfeng-dna
npm install
npm run build
```

## CLI使用

### 分析文本

```bash
# 分析文件
node dist/index.js analyze input.txt -d SK -o report.txt

# 直接分析文本
node dist/index.js analyze -t "我试过很多方法，效果真的惊艳。" --domain SK

# JSON格式输出
node dist/index.js analyze -t "文本" -d PH --json > analysis.json
```

### 生成文本

```bash
# 使用DNA编码生成（需要完整的7部分编码）
node dist/index.js generate \
  -d "PH1811EP111ID9555559RHNLCGVT1SY18031EP000100000DN98808SK8RD559151" \
  -t "护肤心得" \
  --domain SK \
  -l 200 \
  -o output.txt
```

### 对比文本

```bash
node dist/index.js compare text1.txt text2.txt -o comparison.txt
```

### 词汇库管理

```bash
# 列出所有预设词汇库
node dist/index.js list-vocab

# 导出词汇库
node dist/index.js export-vocab SK -o skincare-vocab.json
```

### 自动检测领域

```bash
node dist/index.js detect-domain -t "文本内容" --top 3
```

## API使用

```typescript
import {
  WenfengEncoder,
  WenfengDecoder,
  WenfengAnalyzer,
  encodeText,
  generateFromDNA,
  compareTexts,
  serializeDNA,
  parseDNAString,
  getDefaultVocabularyManager
} from './dist/index';

// 分析文本
const result = encodeText("我试过很多方法，效果惊艳。");
console.log(result.dna);
console.log(result.report);

// 序列化DNA
const dnaStr = serializeDNA(result.dna);
console.log(dnaStr);

// 生成文本
const config = {
  dna: result.dna,
  targetLength: 200,
  topic: "护肤心得",
  algorithm: "AL02", // 见证式算法
  vocabularyBank: manager.getBank('SK')
};
const generated = generateFromDNA(result.dna, config);
console.log(generated.content);

// 对比文本
const comparison = compareTexts(text1, text2);
console.log(comparison.overallSimilarity);
```

## DNA编码格式

完整DNA编码包含7个部分，连续无分隔符：

```
PH[XX][Y][Z]EP[X][Y][Z]ID[A][B][C][D][E][F][G]RH[AAA][BBB][C]SY[XX][YY][Z][WW][AAA][BBB][CCC]DN[V][T][O][W][DD][D]RD[R][P][E][L][C][A]
```

示例：
```
PH1811EP111ID9555559RHNLCGVT1SY18031EP000100000DN98808SK8RD559151
```

各字段说明：
- **PH**: 平均句长(2位) + 本体论(1-6) + 时间观(1-5)
- **EP**: 知识来源(1-5) + 验证方式(1-5) + 真理观(1-4)
- **ID**: 权力(1-9) + 精英(1-9) + 知识(1-9) + 技术(1-9) + 行动(1-9) + 阶层(1-9) + 情感(1-9)
- **RH**: 论证方式(3字母) + 修辞手法(3字母) + 节奏(1/3/5/9)
- **SY**: 平均句长(2) + 复杂度(2) + 变化度(1/3/5) + 标点(2字母) + 短句%(3) + 中句%(3) + 长句%(3)
- **DN**: 词汇专业度(2) + 术语占比(2) + 口语占比(2) + 文言占比(2) + 领域码(2) + 深度(1-9)
- **RD**: 真实(1-9) + 权力(1-9) + 情感(1-9) + 逻辑(1-9) + 具体(1-9) + 行动(1-9)

## 预设词汇库

| 代码 | 领域 | 描述 |
|------|------|------|
| SK | 护肤 | 包含护肤核心概念、品牌、方法、问题、效果、特征、术语、俚语 |
| PH | 哲学 | 哲学概念、人物、方法、问题、效果、属性、术语、口语 |
| FG | 女性成长 | 女性成长相关词汇 |
| ED | 教育 | 教育学习领域词汇 |

## 特殊规则 (RULE01-RULE10)

- RULE01: 句首设问式频率控制
- RULE02: 每段必须包含"我XX过"
- RULE03: 结尾必须有行动指令
- RULE04: 每段至少1个核心概念词
- RULE05: 感叹号密度控制
- RULE06: 专业术语首次出现需解释
- RULE07: 人物/品牌名引用规范
- RULE08: 数字表达方式
- RULE09: 评价词极端程度控制
- RULE10: 转折词选择

## 矛盾点 (CD01-CD05)

- CD01: 权威 vs 平等
- CD02: 理性 vs 感性
- CD03: 批判 vs 建设
- CD04: 普世 vs 个性
- CD05: 专业 vs 通俗

## 生成算法 (AL01-AL05)

| 算法 | 名称 | 适用场景 | 权重分配 |
|------|------|----------|----------|
| AL01 | FAP算法 | 营销文案 | 8:1.5:0.5 |
| AL02 | 见证式算法 | 建立可信度 | 2:3:3:2 |
| AL03 | 对比式算法 | 评测对比 | 2:6:2 |
| AL04 | SCQA算法 | 通用结构 | 2:2:2:4 |
| AL05 | 教程式算法 | 教程类 | 1:6:2:1 |

## 话语模式 (PT01-PT10)

10种高频话语模板，带占比权重：
- PT01: "你看，{现象}，这不就是{结论}吗？" (40%)
- PT02: "我{动词}过，{对象}，{评价}。" (35%)
- PT03: "如果{条件}，那{结果}。" (30%)
- ...等

## 项目结构

```
wenfeng-dna/
├── src/
│   ├── types.ts              # 类型定义和常量
│   ├── encoder.ts            # 文风编码器
│   ├── decoder.ts            # 文本解码器
│   ├── analyzer.ts           # 对比分析器
│   ├── algorithms.ts         # 生成算法库
│   ├── vocabulary-bank-manager.ts  # 词汇库管理
│   ├── special-rules-engine.ts    # 特殊规则引擎
│   ├── contradiction-handler.ts   # 矛盾点处理器
│   ├── dna-utils.ts          # DNA编解码工具
│   ├── index.ts              # 主入口 (CLI + API导出)
│   └── wenfeng-dna-cli.ts    # 独立CLI (旧版)
├── data/
│   └── vocabulary-*.json     # 预设词汇库
├── dist/                     # 编译输出
├── package.json
├── tsconfig.json
└── README.md
```

## 开发

```bash
# 开发模式（监听文件变化）
npm run dev

# 编译
npm run build

# 测试
npm test

# 运行CLI
node dist/index.js [command] [options]
```

## 版本历史

### v3.0 (当前)
- 完整的7层编码系统
- 特殊规则引擎
- 矛盾点自动处理
- 预设词汇库
- CLI命令行工具
- 完整的API导出

### v2.0
- 5层编码系统
- 基本分析功能

### v1.0
- 初始版本
- 基础文风识别

## 技术栈

- TypeScript 5.0
- Node.js 18+
- Commander.js (CLI)
- Chalk (终端颜色)

## 参考

- 《文风DNA编解码手册》v3.0
- 文风分析算法设计
- 自然语言处理

---

**作者**: Claude Code
**许可**: MIT
**版本**: 3.0.0
