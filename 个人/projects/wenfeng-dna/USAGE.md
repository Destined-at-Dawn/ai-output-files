# 文风DNA技能使用指南

## 快速开始

### 1. 安装依赖
```bash
cd wenfeng-dna
npm install
npm run build
```

### 2. 基础使用

#### 分析一段小红书文案
```bash
node dist/index.js analyze -t "我试过这个方法，效果真的太惊艳了！油皮姐妹闭眼入，绝对不踩雷。" --domain FG
```

输出包含：
- 完整的7层DNA编码
- 话语模式识别
- 算法推荐
- 矛盾点预警

#### 生成符合特定文风的文案
```bash
# 先分析一段文本获取DNA
node dist/index.js analyze -t "你的文案" --domain SK --json > dna.json

# 从JSON中提取DNA编码字符串
# 然后使用该编码生成新文案
node dist/index.js generate -d "PH1811..." -t "新话题" --domain SK -l 300
```

## 典型应用场景

### 场景1：小红书爆款文案仿写
```
目标: 仿写"油皮亲妈"风格的护肤文案

步骤:
1. 找一篇爆款小红书护肤文案
2. 分析其DNA编码
3. 使用相同的DNA编码生成类似风格的新文案
4. 替换关键词和话题

命令示例:
node dist/index.js analyze -t "爆款文案原文" --domain SK --json > template.json
# 提取DNA编码
node dist/index.js generate -d "提取的DNA" -t "你的产品" --domain SK -l 500 -o output.txt
```

### 场景2：文风对比 - 判断是否同一位作者
```
node dist/index.js compare author1.txt author2.txt
```

输出会显示：
- 各维度相似度百分比
- 整体相似度
- 主要差异点
- 风格特征对比

### 场景3：定位自己的文风
```
node dist/index.js analyze -t "你的文章内容" --domain PH
```

报告会告诉你：
- 你的哲学立场（唯物/唯心、实用/理想）
- 你的认识论倾向（经验主义/理性主义）
- 你的意识形态特征（权力意识、情感浓度等）
- 你的修辞习惯
- 推荐最适合你的生成算法

## API调用示例

### 在Node.js中使用

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
} from './wenfeng-dna';

// 1. 分析文本
const result = encodeText("哲学真的很难，但是真的值得学。");
console.log("DNA编码:", serializeDNA(result.dna));
console.log("置信度:", result.confidence);

// 2. 查看详细报告
console.log(result.report);

// 3. 生成文本
const generated = generateFromDNA(result.dna, {
  targetLength: 200,
  topic: "存在主义",
  algorithm: "AL02",  // 见证式算法
  vocabularyBank: getDefaultVocabularyManager().getBank('PH')
});
console.log(generated.content);

// 4. 对比两段文本
const comparison = compareTexts(text1, text2);
console.log(`相似度: ${comparison.overallSimilarity * 100}%`);
```

### 在Python中调用（通过子进程）

```python
import subprocess
import json

# 分析
result = subprocess.run(
  ['node', 'wenfeng-dna/dist/index.js', 'analyze', '-t', text, '--domain', 'SK', '--json'],
  capture_output=True, text=True
)
data = json.loads(result.stdout)

# 提取DNA
dna = data['dna']
# 构建DNA字符串...
```

## DNA编码速查

### 完整编码结构
```
PH1811EP111ID9555559RHNLCGVT1SY18031EP000100000DN98808SK8RD559151
││││ │  │ │       │       │        │           │           │
││││ │  │ │       │       │        │           │           └─ 六维雷达 (7位)
││││ │  │ │       │       │        │           └─ 领域编码 (11位)
││││ │  │ │       │       │        └─ 句法层 (16位)
││││ │  │ │       │       └─ 修辞层 (8位)
││││ │  │ │       └─ 意识形态 (7位)
││││ │  │ └─ 认识论 (3位)
││││ │  └─ 本体论(1-6)
│││└─ 平均句长(2位)
└─ PH前缀
```

### 常用组合速查

| 风格 | PH | EP | ID情感 | RH论证 | 适用场景 |
|------|----|----|--------|--------|----------|
| 小红书种草 | 18-24,1,1 | 111 | 情感7-9 | NLC/NGV | 美妆、穿搭、好物分享 |
| 知乎深度 | 25-35,2,1 | 221 | 情感4-6 | LLA | 专业分析、深度解读 |
| 公众号鸡汤 | 15-20,3,3 | 113 | 情感7-9 | NNG | 情感、成长、励志 |
| 学术论文 | 35+,4,1 | 222 | 情感1-3 | LLL | 学术、理论、严谨 |

## 特殊规则应用

### 修改生成文本的行为
```bash
# 使用规则配置（通过配置文件或环境变量）
# RULE09: 使用极端评价词
# RULE10: 使用"但是！"转折

# 高情感文案（适合种草）
RULES='{"RULE09":"extreme","RULE10":"但是！"}' node dist/index.js generate ...

# 理性文案（适合评测）
RULES='{"RULE09":"moderate","RULE10":"然而"}' node dist/index.js generate ...
```

## 故障排除

### DNA编码解析失败
- 检查编码长度是否正确
- 检查数字是否在允许范围内
- 检查领域码是否2字符

### 生成文本质量不高
- 确保传入正确的领域词汇库 (`--domain SK`)
- 增加目标字数 (`-l 500`)
- 尝试不同算法 (`--algorithm AL02` 见证式)

### 置信度过低
- 文本长度至少500字
- 使用领域词汇库提高准确性

## 进阶用法

### 创建自定义词汇库
```json
{
  "domainCode": "MY",
  "domainName": "我的领域",
  "coreConcepts": ["概念1", "概念2"],
  "figures": ["人物1", "人物2"],
  "methods": ["方法1", "方法2"],
  "problems": ["问题1", "问题2"],
  "effects": ["效果1", "效果2"],
  "attributes": ["属性1", "属性2"],
  "technicalTerms": ["术语1", "术语2"],
  "colloquialisms": ["口语1", "口语2"]
}
```

### 批量处理
```bash
# 批量分析文件夹中的所有txt文件
for f in *.txt; do
  node dist/index.js analyze -t "$(cat $f)" --domain SK --json > "output/${f%.txt}.json"
done
```

## 技术支持

- 完整文档: README.md
- 编码手册: 文风DNA编解码手册 v3.0
- 问题反馈: 在项目仓库提交Issue

---

**提示**: 首次使用建议先用短文本测试分析功能，熟悉DNA编码的含义后再进行生成操作。
