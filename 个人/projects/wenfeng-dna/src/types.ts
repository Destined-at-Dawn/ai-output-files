/**
 * 文风DNA类型定义
 * 基于v3.0编解码手册的完整类型系统
 */

// ============ 编码层类型 ============

/** 哲学层编码 PH[XX][Y][Z] */
export interface PhilosophyCode {
  /** 平均句长 10-99 */
  avgSentenceLength: number;
  /** 本体论类型 */
  ontologyType: 1 | 2 | 3 | 4 | 5 | 6;
  /** 时间观 */
  timeView: 1 | 2 | 3 | 4 | 5;
}

/** 认识论编码 EP[X][Y][Z] */
export interface EpistemologyCode {
  /** 知识来源 */
  knowledgeSource: 1 | 2 | 3 | 4 | 5;
  /** 验证方式 */
  verificationMethod: 1 | 2 | 3 | 4 | 5;
  /** 真理观 */
  truthView: 1 | 2 | 3 | 4;
}

/** 意识形态编码 ID[A][B][C][D][E][F][G] */
export interface IdeologyCode {
  power: number;        // 权力维度 1-9
  elite: number;        // 精英倾向 1-9
  knowledge: number;    // 知识态度 1-9
  technology: number;   // 技术态度 1-9
  action: number;       // 行动导向 1-9
  class: number;        // 阶层意识 1-9
  emotion: number;      // 情感浓度 1-9
}

/** 修辞层编码 RH[论证][修辞][节奏] */
export interface RhetoricCode {
  /** 论证方式，3字符字符串如'NNN' */
  argument: string;
  /** 修辞手法，3字符字符串如'GVR' */
  figure: string;
  /** 节奏类型 1|3|5|9 */
  rhythm: 1 | 3 | 5 | 9;
}

/** 句法层编码 SY[XX][YY][Z][WW][AAA][BBB][CCC] */
export interface SyntaxCode {
  avgSentenceLength: number;  // 平均句长 10-99
  complexity: number;         // 句式复杂度 10-99
  variation: 1 | 3 | 5;       // 句式变化度
  punctuation: string;        // 标点风格 2字符
  shortRatio: number;         // 短句占比 %
  mediumRatio: number;        // 中句占比 %
  longRatio: number;         // 长句占比 %
}

/** 领域编码 DN[V][T][O][W][领域码][深度] */
export interface DomainCode {
  vocabularyLevel: number;   // 词汇专业度 1-9
  termRatio: number;         // 技术术语占比 1-9
  colloquialRatio: number;   // 口语占比 1-9
  classicalRatio: number;    // 文言占比 1-9
  domainCode: string;        // 领域码 2字符
  depth: number;             // 深度 1-9
}

/** 六维雷达编码 RD[R][P][E][L][C][A] */
export interface RadarCode {
  reality: number;   // 真实性 1-9
  power: number;     // 权力性 1-9
  emotion: number;   // 情感性 1-9
  logic: number;     // 逻辑性 1-9
  concrete: number;  // 具体性 1-9
  action: number;    // 行动性 1-9
}

// ============ 完整DNA编码 ============

export interface WenfengDNA {
  PH: PhilosophyCode;
  EP: EpistemologyCode;
  ID: IdeologyCode;
  RH: RhetoricCode;
  SY: SyntaxCode;
  DN: DomainCode;
  RD: RadarCode;
}

// ============ 词汇库类型 ============

export interface VocabularyBank {
  domainCode: string;
  domainName: string;
  /** 核心概念词 */
  coreConcepts: string[];
  /** 人物/品牌/流派词 */
  figures: string[];
  /** 方法/工具/产品词 */
  methods: string[];
  /** 问题/现象词 */
  problems: string[];
  /** 效果/目标词 */
  effects: string[];
  /** 特征/属性词 */
  attributes: string[];
  /** 专业术语词 */
  technicalTerms: string[];
  /** 口语/俚语词 */
  colloquialisms: string[];
}

// ============ 话语模式类型 ============

export interface DiscoursePattern {
  id: string;
  frequency: number;       // 出现频率 %
  template: string;        // 模板 {变量}
  example: string;         // 示例
  variables: string[];     // 变量列表
  description?: string;    // 描述
}

// ============ 算法类型 ============

export interface GenerationAlgorithm {
  id: string;
  name: string;
  steps: string[];
  weights: number[];  // 各步骤权重
  description: string;
}

// ============ 特殊规则类型 ============

export interface SpecialRule {
  id: string;
  condition: string;
  behavior: string;
  description: string;
  example?: string;
}

// ============ 矛盾点类型 ============

export interface Contradiction {
  id: string;
  name: string;
  description: string;
  manifestations: string[];
  resolution: string;
  example?: string;
}

// ============ 分析结果类型 ============

export interface AnalysisResult {
  /** 提取的DNA编码 */
  dna: WenfengDNA;
  /** 识别的话语模式及其频率 */
  patterns: Array<{pattern: DiscoursePattern, actualFrequency: number}>;
  /** 使用的领域词汇统计 */
  vocabularyUsage: Record<string, number>;
  /** 置信度 0-1 */
  confidence: number;
  /** 详细分析报告 */
  report: string;
}

// ============ 生成配置类型 ============

export interface GenerationConfig {
  dna: Partial<WenfengDNA>;
  /** 目标字数 */
  targetLength?: number;
  /** 话题/内容 */
  topic?: string;
  /** 使用的算法 */
  algorithm?: string;
  /** 使用的词汇库 */
  vocabularyBank?: VocabularyBank;
  /** 特殊规则覆盖 */
  rules?: Record<string, any>;
}

// ============ 生成结果类型 ============

export interface GenerationResult {
  content: string;
  appliedDNA: WenfengDNA;
  usedPatterns: string[];
  usedVocabulary: string[];
  metrics: {
    wordCount: number;
    sentenceCount: number;
    avgSentenceLength: number;
    uniqueWords: number;
    technicalTermCount: number;
    emotionalWordCount: number;
  };
}

// ============ 比较结果类型 ============

export interface ComparisonResult {
  dna1: WenfengDNA;
  dna2: WenfengDNA;
  similarities: Array<{dimension: string, score: number}>;
  differences: Array<{dimension: string, value1: any, value2: any}>;
  overallSimilarity: number;
}

// ============ 常量定义 ============

export const ONTOLOGY_TYPES: Record<number, string> = {
  1: '唯物实用主义',
  2: '唯物理想主义',
  3: '唯心经验主义',
  4: '唯心理论主义',
  5: '相对主义',
  6: '怀疑主义'
};

export const TIME_VIEWS: Record<number, string> = {
  1: '线性进步',
  2: '循环重复',
  3: '碎片当下',
  4: '断裂跳跃',
  5: '多线并行'
};

export const KNOWLEDGE_SOURCES: Record<number, string> = {
  1: '经验主义',
  2: '理性主义',
  3: '权威主义',
  4: '实践主义',
  5: '直觉主义'
};

export const VERIFICATION_METHODS: Record<number, string> = {
  1: '个人验证',
  2: '科学验证',
  3: '群体验证',
  4: '权威验证',
  5: '市场验证'
};

export const TRUTH_VIEWS: Record<number, string> = {
  1: '绝对真理',
  2: '相对真理',
  3: '实用真理',
  4: '情境真理'
};

export const ARGUMENT_TYPES: Record<string, string> = {
  'N': '叙事论证',
  'L': '逻辑论证',
  'C': '对比论证',
  'U': '升华论证',
  'A': '类比论证',
  'F': '权威论证'
};

export const FIGURE_TYPES: Record<string, string> = {
  'G': '极简格言',
  'V': '极端化',
  'T': '反讽',
  'R': '重复',
  'Q': '设问',
  'M': '隐喻'
};

export const RHYTHM_TYPES: Record<number, string> = {
  1: '快节奏',
  3: '中等节奏',
  5: '慢节奏',
  9: '变速节奏'
};

export const PUNCTUATION_TYPES: Record<string, string> = {
  'EE': '句号为主',
  'EP': '句号+逗号',
  'EX': '句号+感叹',
  'EQ': '句号+问号',
  'PP': '逗号为主',
  'PX': '逗号+感叹',
  'PQ': '逗号+问号',
  'XX': '感叹号密集',
  'QQ': '问号密集'
};

// ============ 领域预设词汇库 ============

export interface PresetVocabularyBank extends VocabularyBank {
  domainNameZh: string;
  description?: string;
}

export const PRESET_VOCABULARY_BANKS: Record<string, PresetVocabularyBank> = {
  'SK': {
    domainCode: 'SK',
    domainName: '护肤',
    domainNameZh: '护肤美容',
    coreConcepts: ['皮肤', '保湿', '美白', '抗衰', '修复', '屏障', '角质层', '吸收', '渗透', '刺激'],
    figures: ['SK-II', '雅诗兰黛', '兰蔻', '资生堂', '欧莱雅', '倩碧', '科颜氏', '修丽可', '宝拉珍选', '理肤泉'],
    methods: ['神仙水', '小棕瓶', '小黑瓶', '红腰子', '精华', '面霜', '眼霜', '面膜', '洗面奶', '卸妆水'],
    problems: ['毛孔', '皱纹', '出油', '暗沉', '闭口', '痘痘', '黑头', '粉刺', '细纹', '松弛'],
    effects: ['美白', '保湿', '修复', '抗氧化', '紧致', '提亮', '淡斑', '去黄', '控油', '祛痘'],
    attributes: ['清爽', '油腻', '粘腻', '搓泥', '泛白', '假滑', '轻薄', '厚重', '水润', '丝滑'],
    technicalTerms: ['烟酰胺', '玻尿酸', '透明质酸', '神经酰胺', '视黄醇', 'A醇', '水杨酸', '果酸', '早C晚A', '建立耐受'],
    colloquialisms: ['真的好', '惊艳到我', '试试看', '油皮亲妈', '干皮救星', '平价替代', '贵妇精华', '学生党福音']
  },
  'PH': {
    domainCode: 'PH',
    domainName: '哲学',
    domainNameZh: '哲学思考',
    coreConcepts: ['存在', '本质', '真理', '自由', '意识', '理性', '经验', '先验', '现象', '本体'],
    figures: ['柏拉图', '亚里士多德', '笛卡尔', '康德', '黑格尔', '尼采', '海德格尔', '萨特', '维特根斯坦', '福柯'],
    methods: ['现象学还原', '辩证法', '解构', '谱系学', '语言分析', '先验演绎', '存在论分析', '反思', '批判', '诠释'],
    problems: ['存在焦虑', '虚无', '异化', '荒诞', '自我欺骗', '他者', '权力', '话语', '主体性', '时间性'],
    effects: ['澄明', '解放', '自由', '真实性', '本真', '超越', '觉醒', '批判意识', '反思能力', '智慧'],
    attributes: ['晦涩', '深刻', '抽象', '具体', '系统', '碎片', '激进', '保守', '批判', '建构'],
    technicalTerms: ['此在', '绽出', '去蔽', '能指', '所指', '差异', '延异', '僭越', '悬置', '还原', '意向性', '视域融合'],
    colloquialisms: ['真的难', '看不懂', '烧脑', '醍醐灌顶', '茅塞顿开', '颠覆三观', '刷新认知', '打开新世界']
  },
  'FG': {
    domainCode: 'FG',
    domainName: '女性成长',
    domainNameZh: '女性成长',
    coreConcepts: ['独立', '自信', '边界', '价值', '成长', '觉醒', '自我', '关系', '选择', '力量'],
    figures: ['西蒙·波伏娃', '贝蒂·弗里丹', '格洛丽亚·斯泰纳姆', '杨笠', '李银河', '上野千鹤子', '女性主义', '性别研究'],
    methods: ['自我觉察', '情绪管理', '边界设定', '沟通技巧', '财务独立', '职业规划', '心理咨询', '支持小组'],
    problems: ['PUA', '情感操控', '讨好型人格', '自我怀疑', '物化', '凝视', '规训', '焦虑', '内耗', '依赖'],
    effects: ['独立', '自洽', '清醒', '坚定', '自由', '掌控', '平衡', '幸福', '成就', '尊严'],
    attributes: ['清醒', '勇敢', '脆弱', '坚韧', '温柔', '锋利', '柔软', '有力', '真实', '复杂'],
    technicalTerms: ['性别刻板印象', '父权制', '结构性压迫', '交叉性', '身体自主权', '情感劳动', '隐形家务', '玻璃天花板'],
    colloquialisms: ['清醒点', '别傻了', '值得更好的', '爱自己', '活出自我', '不将就', '断舍离', '做自己', '姐妹们']
  },
  'ED': {
    domainCode: 'ED',
    domainName: '教育',
    domainNameZh: '教育学习',
    coreConcepts: ['学习', '思维', '能力', '素养', '认知', '理解', '迁移', '元认知', '动机', '兴趣'],
    figures: ['皮亚杰', '维果茨基', '布鲁纳', '杜威', '蒙台梭利', '建构主义', '行为主义', '认知主义', '人本主义'],
    methods: ['项目式学习', '探究式学习', '合作学习', '差异化教学', '脚手架', '思维导图', '费曼学习法', '刻意练习'],
    problems: ['厌学', '焦虑', '内卷', '应试', '机械记忆', '知识碎片化', '迁移困难', '动机缺失', '习得性无助'],
    effects: ['深度理解', '批判性思维', '创造力', '问题解决', '自主学习', '终身学习', '核心素养', '全面发展'],
    attributes: ['主动', '被动', '深度', '浅层', '机械', '理解', '灵活', '僵化', '有趣', '枯燥'],
    technicalTerms: ['最近发展区', '认知负荷', '图式', '先验知识', '元认知监控', '自我效能感', '内在动机', '外在动机'],
    colloquialisms: ['学不进去', '开窍了', '懂了', '会了', '卡住了', '突破了', '顿悟', '灵光一现', '恍然大悟']
  }
};

// ============ 预设特殊规则 ============

export const PRESET_SPECIAL_RULES: SpecialRule[] = [
  {
    id: 'RULE01',
    condition: '句首',
    behavior: '使用PT01设问式的频率',
    description: '句首设问式频率控制',
    example: '句首使用"你看，XX，这不就是XX吗？"的频率为40%'
  },
  {
    id: 'RULE02',
    condition: '每段',
    behavior: '必须包含"我XX过"或"我XX了"',
    description: '每段必须包含个人经历表述',
    example: '每段至少包含"我试过""我研究过""我发现了"等表达'
  },
  {
    id: 'RULE03',
    condition: '结尾',
    behavior: '必须有行动指令',
    description: '段落结尾必须有行动召唤',
    example: '结尾使用"你可以试试""建议你""不妨"等行动引导'
  },
  {
    id: 'RULE04',
    condition: '每段',
    behavior: '至少1个核心概念词',
    description: '每段必须使用领域核心概念',
    example: '在护肤领域，每段至少使用1个核心概念如"保湿""修复"等'
  },
  {
    id: 'RULE05',
    condition: '感叹号',
    behavior: '感叹号密度控制',
    description: '感叹号使用密度',
    example: '情感浓度高的领域感叹号密度可达5-10个/百字'
  },
  {
    id: 'RULE06',
    condition: '专业术语',
    behavior: '首次出现需解释',
    description: '专业术语首次出现是否需要解释',
    example: '首次出现"烟酰胺"时，紧接着用括号解释'
  },
  {
    id: 'RULE07',
    condition: '人物/品牌名',
    behavior: '首次全称，后续可简称',
    description: '人物品牌名称引用规范',
    example: '首次"海德格尔"，后续可用"他"'
  },
  {
    id: 'RULE08',
    condition: '数字',
    behavior: '避免直接说/精确到小数点',
    description: '数字表达方式',
    example: '不说"很多人"而说"超过70%的人"'
  },
  {
    id: 'RULE09',
    condition: '评价词',
    behavior: '根据情感浓度决定极端程度',
    description: '评价词极端程度控制',
    example: '情感>=7时使用"惊艳""震撼"，情感<=3时使用"有效""实用"'
  },
  {
    id: 'RULE10',
    condition: '转折',
    behavior: '使用"但是！"还是"然而"',
    description: '转折词选择',
    example: '高情感用"但是！"，低情感用"然而"'
  }
];

// ============ 预设矛盾点 ============

export const PRESET_CONTRADICTIONS: Contradiction[] = [
  {
    id: 'CD01',
    name: '权威 vs 平等',
    description: '既要建立专家权威，又要营造平等对话感',
    manifestations: [
      '使用"我XX过""我XX了"建立权威',
      '使用"你也可以""你可以试试"拉近距离'
    ],
    resolution: '前半段建立权威，后半段拉近距离',
    example: '"我研究哲学十年，深刻理解海德格尔的艰深。但对你来说，从存在主义入门可能更合适。"'
  },
  {
    id: 'CD02',
    name: '理性 vs 感性',
    description: '既要科学理性，又要感性煽动',
    manifestations: [
      '使用术语、数据、逻辑展示理性',
      '使用情感词、共鸣句、体验描述激发感性'
    ],
    resolution: '先讲理性（术语），再讲感性（感受）',
    example: '"烟酰胺的透皮吸收率是传统成分的3倍。但真正让我惊艳的是，皮肤那种透亮的感觉。"'
  },
  {
    id: 'CD03',
    name: '批判 vs 建设',
    description: '既要批判现状，又要给出方案',
    manifestations: [
      '指出问题、弊端、错误',
      '提供解决方案、方法、建议'
    ],
    resolution: '先批判大环境，再给出具体方案',
    example: '"绝大多数护肤品都是智商税。但如果你知道怎么选，其实只需要这三步。"'
  },
  {
    id: 'CD04',
    name: '普世 vs 个性',
    description: '既要给出普遍规律，又要强调因人而异',
    manifestations: [
      '陈述普遍适用的规律',
      '补充个性化建议和例外情况'
    ],
    resolution: '"一般来说XX，但如果你是XX，那就XX"',
    example: '"一般来说早C晚A有效。但如果你是敏感肌，那就先从低浓度开始。"'
  },
  {
    id: 'CD05',
    name: '专业 vs 通俗',
    description: '既要展示专业性，又要通俗易懂',
    manifestations: [
      '使用专业术语、英文原名、行业黑话',
      '用大白话、比喻、类比解释'
    ],
    resolution: '先用术语，立即用大白话解释',
    example: '"使用视黄醇（就是A醇）促胶原，简单说就是让皮肤重新变紧致。"'
  }
];
