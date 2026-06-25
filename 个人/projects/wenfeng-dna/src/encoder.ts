/**
 * 文风DNA编码器
 * 分析文本并提取文风DNA编码
 */

import {
  WenfengDNA,
  PhilosophyCode,
  EpistemologyCode,
  IdeologyCode,
  RhetoricCode,
  SyntaxCode,
  DomainCode,
  RadarCode,
  AnalysisResult,
  DiscoursePattern,
  VocabularyBank,
  ONTOLOGY_TYPES,
  TIME_VIEWS,
  KNOWLEDGE_SOURCES,
  VERIFICATION_METHODS,
  TRUTH_VIEWS,
  ARGUMENT_TYPES,
  FIGURE_TYPES,
  RHYTHM_TYPES
} from './types';

export class WenfengEncoder {
  private text: string;
  private sentences: string[];
  private words: string[];
  private vocabularyBank?: VocabularyBank;

  constructor(text: string, vocabularyBank?: VocabularyBank) {
    this.text = text;
    this.sentences = this.splitSentences(text);
    this.words = this.tokenize(text);
    this.vocabularyBank = vocabularyBank;
  }

  /**
   * 完整编码分析
   */
  public encode(): AnalysisResult {
    const dna: WenfengDNA = {
      PH: this.encodePhilosophy(),
      EP: this.encodeEpistemology(),
      ID: this.encodeIdeology(),
      RH: this.encodeRhetoric(),
      SY: this.encodeSyntax(),
      DN: this.encodeDomain(),
      RD: this.encodeRadar()
    };

    const patterns = this.identifyPatterns();
    const vocabularyUsage = this.analyzeVocabularyUsage();

    return {
      dna,
      patterns,
      vocabularyUsage,
      confidence: this.calculateConfidence(),
      report: this.generateReport(dna, patterns)
    };
  }

  /**
   * 编码PH - 哲学层
   */
  private encodePhilosophy(): PhilosophyCode {
    const avgLen = this.calculateAvgSentenceLength();
    const ontology = this.detectOntologyType();
    const timeView = this.detectTimeView();

    return {
      avgSentenceLength: Math.round(avgLen),
      ontologyType: ontology,
      timeView: timeView
    };
  }

  /**
   * 编码EP - 认识论层
   */
  private encodeEpistemology(): EpistemologyCode {
    const knowledgeSource = this.detectKnowledgeSource();
    const verification = this.detectVerificationMethod();
    const truthView = this.detectTruthView();

    return {
      knowledgeSource,
      verificationMethod: verification,
      truthView
    };
  }

  /**
   * 编码ID - 意识形态层
   */
  private encodeIdeology(): IdeologyCode {
    // 基于文本特征推断7个维度
    const text = this.text.toLowerCase();

    // 权力维度：权威词汇 vs 平等词汇
    const authorityWords = ['专家说', '权威', '必须', '应该', '一定要', '绝对', '必须', '权威'];
    const egalitarianWords = ['你可以', '你可以试试', '我觉得', '我认为', '个人经验'];
    const authorityCount = this.countWords(text, authorityWords);
    const egalitarianCount = this.countWords(text, egalitarianWords);
    const power = this.normalizeScore(authorityCount, egalitarianCount, 1, 9);

    // 精英倾向：专业术语 vs 通俗表达
    const elitistWords = ['精英', '阶层', '上层', '高级', '专业'];
    const commonWords = ['大家', '普通人', '所有人', '每个人'];
    const elite = this.normalizeScore(
      this.countWords(text, elitistWords),
      this.countWords(text, commonWords),
      1, 9
    );

    // 知识态度：垄断词汇 vs 共享词汇
    const monopolyWords = ['独家', '内部', '秘传', '不传之秘'];
    const shareWords = ['分享', '公开', '大家', '共同'];
    const knowledge = this.normalizeScore(
      this.countWords(text, monopolyWords),
      this.countWords(text, shareWords),
      1, 9
    );

    // 技术态度：乐观 vs 批判
    const optimisticWords = ['进步', '发展', '优势', '革命性', '突破'];
    const criticalWords = ['风险', '问题', '缺陷', '隐患', '弊端'];
    const technology = this.normalizeScore(
      this.countWords(text, optimisticWords),
      this.countWords(text, criticalWords),
      1, 9
    );

    // 行动导向：行动词汇 vs 理论词汇
    const actionWords = ['做', '行动', '实践', '试试', '开始', '执行'];
    const theoryWords = ['理论', '思考', '分析', '理解', '研究'];
    const action = this.normalizeScore(
      this.countWords(text, actionWords),
      this.countWords(text, theoryWords),
      1, 9
    );

    // 阶层意识：强调阶层 vs 淡化阶层
    const classWords = ['阶层', '阶级', '上层', '底层', '中产', '富人', '穷人'];
    const noClassWords = ['人人', '平等', '每个人', '所有'];
    const classConsciousness = this.normalizeScore(
      this.countWords(text, classWords),
      this.countWords(text, noClassWords),
      1, 9
    );

    // 情感浓度：情感词汇频率
    const emotionalWords = ['!', '!!!', '太棒了', '惊艳', '震撼', '感动', '爱', '恨', '超级', '极其', '惊人'];
    const calmWords = ['客观', '理性', '冷静', '中立', '平衡'];
    const emotion = this.normalizeScore(
      this.countWords(text, emotionalWords),
      this.countWords(text, calmWords),
      1, 9
    );

    return { power, elite, knowledge, technology, action, class: classConsciousness, emotion };
  }

  /**
   * 编码RH - 修辞层
   */
  private encodeRhetoric(): RhetoricCode {
    const argument = this.detectArgumentPattern();
    const figure = this.detectFigurePattern();
    const rhythm = this.detectRhythmType();

    return { argument, figure, rhythm };
  }

  /**
   * 编码SY - 句法层
   */
  private encodeSyntax(): SyntaxCode {
    const sentences = this.sentences;
    const lengths = sentences.map(s => s.length);

    const avgLen = lengths.reduce((a, b) => a + b, 0) / lengths.length;
    const complexity = this.calculateComplexity();
    const variation = this.calculateVariation();

    const punctuation = this.detectPunctuationStyle();
    const { short, medium, long } = this.calculateSentenceDistribution();

    return {
      avgSentenceLength: Math.round(avgLen),
      complexity,
      variation,
      punctuation,
      shortRatio: short,
      mediumRatio: medium,
      longRatio: long
    };
  }

  /**
   * 编码DN - 领域编码
   */
  private encodeDomain(): DomainCode {
    const text = this.text.toLowerCase();

    // 词汇专业度：基于长词、复杂词的频率
    const longWords = this.words.filter(w => w.length >= 4);
    const vocabLevel = Math.min(9, Math.max(1, Math.round((longWords.length / this.words.length) * 15)));

    // 技术术语占比
    let termCount = 0;
    if (this.vocabularyBank?.technicalTerms) {
      for (const term of this.vocabularyBank.technicalTerms) {
        if (text.includes(term.toLowerCase())) {
          termCount++;
        }
      }
    }
    const termRatio = this.vocabularyBank?.technicalTerms
      ? Math.min(9, Math.round((termCount / this.vocabularyBank.technicalTerms.length) * 10))
      : 5;

    // 口语占比
    const colloquialPatterns = ['的', '了', '呢', '吧', '啊', '嘛', '啦', '呗', '呗', '哈哈', '呵呵', '嘻嘻'];
    const colloquialCount = this.countWords(text, colloquialPatterns);
    const colloquialRatio = Math.min(9, Math.round((colloquialCount / this.words.length) * 20));

    // 文言占比
    const classicalPatterns = ['之', '乎', '者', '也', '焉', '哉', '矣', '耳', '哉', '欤'];
    const classicalCount = this.countWords(text, classicalPatterns);
    const classicalRatio = Math.min(9, Math.round((classicalCount / this.words.length) * 50));

    // 领域识别
    let domainCode = 'GN'; // 默认通用
    let depth = 5;

    if (this.vocabularyBank) {
      domainCode = this.vocabularyBank.domainCode;
      // 深度评估：基于核心概念使用频率
      const coreConceptCount = this.vocabularyBank.coreConcepts?.filter(c =>
        text.includes(c.toLowerCase())
      ).length || 0;
      depth = Math.min(9, Math.round((coreConceptCount / 10) * 5) + 3);
    } else {
      // 没有词汇库，尝试基于关键词识别领域
      domainCode = this.guessDomainCode(text);
      depth = this.estimateDepth(text);
    }

    return {
      vocabularyLevel: vocabLevel,
      termRatio,
      colloquialRatio,
      classicalRatio,
      domainCode,
      depth
    };
  }

  /**
   * 猜测领域代码（基于关键词）
   */
  private guessDomainCode(text: string): string {
    const domainKeywords: Record<string, string[]> = {
      'SK': ['皮肤', '保湿', '美白', '抗衰', '精华', '面霜', '眼霜', '毛孔', '皱纹'],
      'PH': ['存在', '本质', '真理', '自由', '意识', '理性', '现象', '本体'],
      'FG': ['独立', '自信', '边界', '成长', '觉醒', '女性', '自我', '关系'],
      'ED': ['学习', '思维', '能力', '认知', '理解', '迁移', '元认知', '素养']
    };

    const scores: Record<string, number> = {};

    for (const [code, keywords] of Object.entries(domainKeywords)) {
      scores[code] = keywords.filter(k => text.includes(k)).length;
    }

    const maxEntry = Object.entries(scores).sort((a, b) => b[1] - a[1])[0];
    return maxEntry && maxEntry[1] > 0 ? maxEntry[0] : 'GN';
  }

  /**
   * 估计内容深度
   */
  private estimateDepth(text: string): number {
    // 深度指标：
    // 1. 专业术语数量
    // 2. 长句比例
    // 3. 抽象词汇数量
    // 4. 理论性词汇

    const depthIndicators = [
      '理论', '概念', '体系', '框架', '机制', '原理', '本质',
      '深层', '根本', '核心', '系统', '结构', '逻辑'
    ];

    const indicatorCount = depthIndicators.filter(d => text.includes(d)).length;
    return Math.min(9, Math.round((indicatorCount / 5) * 3) + 3);
  }

  /**
   * 编码RD - 六维雷达
   */
  private encodeRadar(): RadarCode {
    const text = this.text;

    // 真实性：事实词汇 vs 主观词汇
    const factWords = ['数据', '研究', '实验', '证明', '统计', '事实'];
    const subjectiveWords = ['我觉得', '我认为', '感觉', '相信', '猜测'];
    const reality = this.normalizeScore(
      this.countWords(text, factWords),
      this.countWords(text, subjectiveWords),
      1, 9
    );

    // 权力性：命令式 vs 建议式
    const imperativeWords = ['必须', '应该', '一定要', '禁止', '不得'];
    const suggestiveWords = ['可以', '也许', '可能', '建议', '推荐'];
    const power = this.normalizeScore(
      this.countWords(text, imperativeWords),
      this.countWords(text, suggestiveWords),
      1, 9
    );

    // 情感性：情感词汇频率
    const emotionalWords = ['感动', '震撼', '惊艳', '太棒了', '爱', '恨', '痛苦', '快乐'];
    const neutralWords = ['客观', '中立', '平衡', '理性'];
    const emotion = this.normalizeScore(
      this.countWords(text, emotionalWords),
      this.countWords(text, neutralWords),
      1, 9
    );

    // 逻辑性：逻辑连接词
    const logicWords = ['因为', '所以', '因此', '但是', '然而', '如果', '那么', '首先', '其次', '最后'];
    const logic = Math.min(9, Math.max(1, this.countWords(text, logicWords) * 2));

    // 具体性：具体名词 vs 抽象词
    const concreteWords = ['具体', '例如', '比如', '实际', '实例', '案例'];
    const abstractWords = ['抽象', '理论', '概念', '理念', '原则'];
    const concrete = this.normalizeScore(
      this.countWords(text, concreteWords),
      this.countWords(text, abstractWords),
      1, 9
    );

    // 行动性：动词密度，特别是行动动词
    const actionVerbs = ['做', '行动', '开始', '执行', '实施', '实践', '尝试', '创造', '建立'];
    const action = Math.min(9, Math.max(1, (this.countWords(text, actionVerbs) / this.words.length) * 50));

    return { reality, power, emotion, logic, concrete, action };
  }

  // ============ 辅助方法 ============

  private splitSentences(text: string): string[] {
    return text
      .replace(/[。！？.!?；;]/g, '$&|')
      .split('|')
      .filter(s => s.trim().length > 0)
      .map(s => s.trim());
  }

  private tokenize(text: string): string[] {
    return text
      .toLowerCase()
      .replace(/[^\u4e00-\u9fa5a-z0-9\s]/g, ' ')
      .split(/\s+/)
      .filter(w => w.length > 0);
  }

  private calculateAvgSentenceLength(): number {
    if (this.sentences.length === 0) return 0;
    const total = this.sentences.reduce((sum, s) => sum + s.length, 0);
    return total / this.sentences.length;
  }

  private calculateComplexity(): number {
    // 基于从句数量、修饰语等计算复杂度
    const complexMarkers = ['，', '；', '、', '「', '」', '（', '）', '虽然', '但是', '然而', '因此'];
    const markerCount = this.countWords(this.text, complexMarkers);
    const baseComplexity = (this.words.length / Math.max(1, this.sentences.length)) / 3;
    return Math.min(99, Math.round(baseComplexity + markerCount * 2));
  }

  private calculateVariation(): 1 | 3 | 5 {
    const lengths = this.sentences.map(s => s.length);
    const avg = lengths.reduce((a, b) => a + b, 0) / lengths.length;
    const variance = lengths.reduce((sum, len) => sum + Math.pow(len - avg, 2), 0) / lengths.length;
    const stdDev = Math.sqrt(variance);

    if (stdDev < avg * 0.2) return 1;
    if (stdDev < avg * 0.5) return 3;
    return 5;
  }

  private calculateSentenceDistribution(): { short: number; medium: number; long: number } {
    const avg = this.calculateAvgSentenceLength();
    let short = 0, medium = 0, long = 0;

    for (const s of this.sentences) {
      if (s.length < avg * 0.5) short++;
      else if (s.length < avg * 1.5) medium++;
      else long++;
    }

    const total = this.sentences.length;
    return {
      short: Math.round((short / total) * 100),
      medium: Math.round((medium / total) * 100),
      long: Math.round((long / total) * 100)
    };
  }

  private detectOntologyType(): 1 | 2 | 3 | 4 | 5 | 6 {
    const text = this.text.toLowerCase();

    // 实用主义关键词
    const practical = ['效果', '实用', '有用', '具体', '实际', '结果', '验证', '测试'];
    // 理想主义关键词
    const idealist = ['理想', '完美', '崇高', '理念', '理论', '原则'];
    // 经验主义关键词
    const empirical = ['感觉', '体验', '经历', '感受', '亲测', '试用'];
    // 理论主义关键词
    const theoretical = ['理论', '逻辑', '推演', '证明', '推导', '概念'];
    // 相对主义关键词
    const relativist = ['因人而异', '看情况', '不同', '多种', '多样'];
    // 怀疑主义关键词
    const skeptical = ['怀疑', '质疑', '不确定', '可能', '也许', '不一定'];

    const scores: Record<number, number> = {
      1: this.countWords(text, practical),
      2: this.countWords(text, idealist),
      3: this.countWords(text, empirical),
      4: this.countWords(text, theoretical),
      5: this.countWords(text, relativist),
      6: this.countWords(text, skeptical)
    };

    return Number(Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0]) as 1 | 2 | 3 | 4 | 5 | 6;
  }

  private detectTimeView(): 1 | 2 | 3 | 4 | 5 {
    const text = this.text.toLowerCase();

    const linear = ['进步', '发展', '前进', '越来越', '成长', '进化', '提升'];
    const cyclic = ['循环', '重复', '轮回', '周期', '周而复始', '历史重演'];
    const present = ['当下', '现在', '立刻', '马上', '这一刻', '此时此刻'];
    const rupture = ['突变', '飞跃', '革命', '断裂', '颠覆', '跨越'];
    const parallel = ['同时', '并行', '多线', '多元', '多个方面'];

    const scores: Record<number, number> = {
      1: this.countWords(text, linear),
      2: this.countWords(text, cyclic),
      3: this.countWords(text, present),
      4: this.countWords(text, rupture),
      5: this.countWords(text, parallel)
    };

    return Number(Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0]) as 1 | 2 | 3 | 4 | 5;
  }

  private detectKnowledgeSource(): 1 | 2 | 3 | 4 | 5 {
    const text = this.text.toLowerCase();

    const experience = ['我试过', '我做过', '亲测', '体验', '经历', '用过'];
    const rational = ['逻辑', '推理', '推导', '证明', '演绎', '必然'];
    const authority = ['专家说', '权威', '研究表明', '数据显示', '根据'];
    const practice = ['实践中', '实践中发现', '边做边学', '实战'];
    const intuition = ['感觉', '直觉', '直觉告诉我', '我觉得', '预感'];

    const scores: Record<number, number> = {
      1: this.countWords(text, experience),
      2: this.countWords(text, rational),
      3: this.countWords(text, authority),
      4: this.countWords(text, practice),
      5: this.countWords(text, intuition)
    };

    return Number(Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0]) as 1 | 2 | 3 | 4 | 5;
  }

  private detectVerificationMethod(): 1 | 2 | 3 | 4 | 5 {
    const text = this.text.toLowerCase();

    const personal = ['我亲测', '我试过', '我的经历', '我验证'];
    const scientific = ['研究', '实验', '数据', '统计', '论文', '临床试验'];
    const social = ['大家说', '很多人都', '普遍', '公认', '用户反馈'];
    const authVerify = ['专家认证', '权威推荐', '官方认可'];
    const market = ['销量', '爆款', '热卖', '回购', '口碑'];

    const scores: Record<number, number> = {
      1: this.countWords(text, personal),
      2: this.countWords(text, scientific),
      3: this.countWords(text, social),
      4: this.countWords(text, authVerify),
      5: this.countWords(text, market)
    };

    return Number(Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0]) as 1 | 2 | 3 | 4 | 5;
  }

  private detectTruthView(): 1 | 2 | 3 | 4 {
    const text = this.text.toLowerCase();

    const absolute = ['一定', '绝对', '必然', '永远', '永远都是'];
    const relative = ['因人而异', '看情况', '不同人', '可能', '也许'];
    const pragmatic = ['有用', '有效', '实用', '解决问题', '达到目的'];
    const contextual = ['在这种情况下', '具体问题具体分析', '看语境'];

    const scores: Record<number, number> = {
      1: this.countWords(text, absolute),
      2: this.countWords(text, relative),
      3: this.countWords(text, pragmatic),
      4: this.countWords(text, contextual)
    };

    return Number(Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0]) as 1 | 2 | 3 | 4;
  }

  private detectArgumentPattern(): string {
    const text = this.text;
    const patterns: Record<string, number> = {
      'N': this.countNarrativeArguments(text),
      'L': this.countLogicalArguments(text),
      'C': this.countComparisons(text),
      'U': this.countElevations(text),
      'A': this.countAnalogies(text),
      'F': this.countAuthorities(text)
    };

    const sorted = Object.entries(patterns).sort((a, b) => b[1] - a[1]);
    const primary = sorted[0][0];
    const secondary = sorted[1][0];
    const tertiary = sorted[2][0];

    return primary + secondary + tertiary;
  }

  private countNarrativeArguments(text: string): number {
    const markers = ['故事', '经历', '案例', '曾经', '有一次', '我遇到', '我记得'];
    return this.countWords(text, markers);
  }

  private countLogicalArguments(text: string): number {
    const markers = ['因为', '所以', '因此', '既然', '既然', '如果', '那么'];
    return this.countWords(text, markers);
  }

  private countComparisons(text: string): number {
    const markers = ['相比', '相比之下', '不同于', 'vs', 'VS', '一个...另一个', '二者'];
    return this.countWords(text, markers);
  }

  private countElevations(text: string): number {
    const markers = ['最重要的是', '最关键的是', '归根结底', '本质上', '真正'];
    return this.countWords(text, markers);
  }

  private countAnalogies(text: string): number {
    const markers = ['就像', '好比', '如同', '仿佛', '相当于', '类似'];
    return this.countWords(text, markers);
  }

  private countAuthorities(text: string): number {
    const markers = ['专家说', '研究表明', '数据显示', '权威', '大师', '名人'];
    return this.countWords(text, markers);
  }

  private detectFigurePattern(): string {
    const text = this.text;

    const patterns: Record<string, number> = {
      'G': this.countGnomons(text),
      'V': this.countExtremes(text),
      'T': this.countIronies(text),
      'R': this.countRepetitions(text),
      'Q': this.countQuestions(text),
      'M': this.countMetaphors(text)
    };

    const sorted = Object.entries(patterns).sort((a, b) => b[1] - a[1]);
    return sorted[0][0] + sorted[1][0] + sorted[2][0];
  }

  private countGnomons(text: string): number {
    // 极简格言：简短有力的陈述句
    const shortPowerful = text.match(/[^。！？.!?]{2,8}[。！？.!?]/g) || [];
    return shortPowerful.filter(s => s.length <= 15).length;
  }

  private countExtremes(text: string): number {
    const markers = ['极其', '超级', '无比', '非常', '极其', '最', '太...了', '惊人'];
    return this.countWords(text, markers);
  }

  private countIronies(text: string): number {
    const markers = ['呵呵', '讽刺', '可笑', '真有意思', '所谓的', '所谓的'];
    return this.countWords(text, markers);
  }

  private countRepetitions(text: string): number {
    // 检测重复出现的词语
    const words = this.tokenize(text);
    const wordCounts: Record<string, number> = {};
    words.forEach(w => {
      if (w.length > 1) {
        wordCounts[w] = (wordCounts[w] || 0) + 1;
      }
    });
    let repeatCount = 0;
    for (const count of Object.values(wordCounts)) {
      if (count >= 3) repeatCount++;
    }
    return repeatCount;
  }

  private countQuestions(text: string): number {
    return (text.match(/[？?]/g) || []).length;
  }

  private countMetaphors(text: string): number {
    const markers = ['就像', '如同', '好似', '仿佛', '相当于', '隐喻', '象征'];
    return this.countWords(text, markers);
  }

  private detectRhythmType(): 1 | 3 | 5 | 9 {
    const lengths = this.sentences.map(s => s.length);
    const avg = lengths.reduce((a, b) => a + b, 0) / lengths.length;

    // 计算长度变化系数
    const variations = lengths.map(l => Math.abs(l - avg) / avg);
    const avgVariation = variations.reduce((a, b) => a + b, 0) / variations.length;

    if (avgVariation < 0.2) return 1;
    if (avgVariation < 0.4) return 3;
    if (avgVariation < 0.6) return 5;
    return 9;
  }

  private detectPunctuationStyle(): string {
    const text = this.text;
    const periodCount = (text.match(/[。.!]/g) || []).length;
    const commaCount = (text.match(/[，,]/g) || []).length;
    const exclamationCount = (text.match(/[!！]/g) || []).length;
    const questionCount = (text.match(/[?？]/g) || []).length;

    const max = Math.max(periodCount, commaCount, exclamationCount, questionCount);

    let style = '';
    if (periodCount === max) style += 'E';
    if (commaCount === max) style += 'P';
    if (exclamationCount === max) style += 'X';
    if (questionCount === max) style += 'Q';

    if (style.length === 0) {
      style = 'EP';
    } else if (style.length === 1) {
      style = style + style[0]; // duplicate to make 2 chars
    }
    return style.substring(0, 2);
  }

  private identifyPatterns(): Array<{pattern: DiscoursePattern, actualFrequency: number}> {
    const ptPatterns: DiscoursePattern[] = [
      {
        id: 'PT01',
        frequency: 40,
        template: '你看，{现象}，这不就是{结论}吗？',
        example: '你看，读了三遍还是不懂，这不就是晦涩吗？',
        variables: ['现象', '结论']
      },
      {
        id: 'PT02',
        frequency: 35,
        template: '我{动词}过，{对象}，{评价}。',
        example: '我试过，冥想，效果真的惊艳。',
        variables: ['动词', '对象', '评价']
      },
      {
        id: 'PT03',
        frequency: 30,
        template: '如果{条件}，那{结果}。',
        example: '如果你是内向者，那这个方法绝对适合你。',
        variables: ['条件', '结果']
      },
      {
        id: 'PT04',
        frequency: 25,
        template: '{对象}我{动词}了{时长}，{评价}，{细节}。',
        example: '这本书我读了三遍，收获巨大，每次都有新发现。',
        variables: ['对象', '动词', '时长', '评价', '细节']
      },
      {
        id: 'PT05',
        frequency: 20,
        template: '说实话，{观点}，但是！{转折}。',
        example: '说实话，哲学很难，但是！真的值得学。',
        variables: ['观点', '转折']
      },
      {
        id: 'PT06',
        frequency: 15,
        template: '{对象}真的{评价}，{理由}。',
        example: '这个理论真的深刻，解释了很多现象。',
        variables: ['对象', '评价', '理由']
      },
      {
        id: 'PT07',
        frequency: 15,
        template: '为什么{问题}？因为{原因}。',
        example: '为什么推荐存在主义？因为它直面人生困境。',
        variables: ['问题', '原因']
      },
      {
        id: 'PT08',
        frequency: 10,
        template: '{对象}的{特点}，{评价}。',
        example: '海德格尔的语言，晦涩但准确。',
        variables: ['对象', '特点', '评价']
      },
      {
        id: 'PT09',
        frequency: 10,
        template: '相比{A}，{B}更{特点}。',
        example: '相比笛卡尔，康德更系统。',
        variables: ['A', 'B', '特点']
      },
      {
        id: 'PT10',
        frequency: 5,
        template: '{观点}，这是我{时长}的{经验/思考}。',
        example: '现象学真的有用，这是我五年的思考。',
        variables: ['观点', '时长', '经验/思考']
      }
    ];

    // 简单统计每种模式的出现次数
    const results: Array<{pattern: DiscoursePattern, actualFrequency: number}> = [];

    for (const pattern of ptPatterns) {
      const estimated = this.estimatePatternFrequency(pattern);
      results.push({ pattern, actualFrequency: estimated });
    }

    return results.sort((a, b) => b.actualFrequency - a.actualFrequency).slice(0, 5);
  }

  private estimatePatternFrequency(pattern: DiscoursePattern): number {
    const { template } = pattern;
    let count = 0;

    // 检测模板中的固定部分
    if (template.includes('我') && template.includes('过')) {
      count += this.countWords(this.text, ['我试过', '我做过', '我体验过']);
    }
    if (template.includes('如果')) {
      count += this.countWords(this.text, ['如果', '假如', '要是']);
    }
    if (template.includes('因为')) {
      count += this.countWords(this.text, ['因为', '之所以']);
    }
    if (template.includes('相比')) {
      count += this.countWords(this.text, ['相比', '相比之下', '不同于']);
    }

    return Math.min(100, Math.round(count * 10));
  }

  private analyzeVocabularyUsage(): Record<string, number> {
    // 这里应该与词汇库对比，暂时返回空
    return {};
  }

  private calculateConfidence(): number {
    // 基于文本长度和分析的完整性计算置信度
    const baseConfidence = Math.min(1, this.words.length / 500);
    return Math.round(baseConfidence * 100) / 100;
  }

  private generateReport(dna: WenfengDNA, patterns: Array<{pattern: DiscoursePattern, actualFrequency: number}>): string {
    const lines: string[] = [
      '=== 文风DNA分析报告 ===',
      '',
      `【哲学层】PH${dna.PH.avgSentenceLength}${dna.PH.ontologyType}${dna.PH.timeView}`,
      `  平均句长: ${dna.PH.avgSentenceLength}字`,
      `  本体论: ${ONTOLOGY_TYPES[dna.PH.ontologyType]}`,
      `  时间观: ${TIME_VIEWS[dna.PH.timeView]}`,
      '',
      `【认识论】EP${this.encodeEPNumber(dna.EP)}`,
      `  知识来源: ${KNOWLEDGE_SOURCES[dna.EP.knowledgeSource]}`,
      `  验证方式: ${VERIFICATION_METHODS[dna.EP.verificationMethod]}`,
      `  真理观: ${TRUTH_VIEWS[dna.EP.truthView]}`,
      '',
      `【意识形态】ID${this.encodeIDNumber(dna.ID)}`,
      `  权力: ${dna.ID.power}/9, 精英: ${dna.ID.elite}/9, 知识: ${dna.ID.knowledge}/9`,
      `  技术: ${dna.ID.technology}/9, 行动: ${dna.ID.action}/9, 阶层: ${dna.ID.class}/9, 情感: ${dna.ID.emotion}/9`,
      '',
      `【修辞层】RH${dna.RH.argument}${dna.RH.figure}${dna.RH.rhythm}`,
      `  论证: ${ARGUMENT_TYPES[dna.RH.argument[0]]}+${ARGUMENT_TYPES[dna.RH.argument[1]]}+${ARGUMENT_TYPES[dna.RH.argument[2]]}`,
      `  修辞: ${FIGURE_TYPES[dna.RH.figure[0]]}+${FIGURE_TYPES[dna.RH.figure[1]]}+${FIGURE_TYPES[dna.RH.figure[2]]}`,
      `  节奏: ${RHYTHM_TYPES[dna.RH.rhythm]}`,
      '',
      `【句法层】SY${this.pad2(dna.SY.avgSentenceLength)}${this.pad2(dna.SY.complexity)}${dna.SY.variation}${dna.SY.punctuation}${this.pad3(dna.SY.shortRatio)}${this.pad3(dna.SY.mediumRatio)}${this.pad3(dna.SY.longRatio)}`,
      `  短句: ${dna.SY.shortRatio}%, 中句: ${dna.SY.mediumRatio}%, 长句: ${dna.SY.longRatio}%`,
      '',
      `【六维雷达】RD${dna.RD.reality}${dna.RD.power}${dna.RD.emotion}${dna.RD.logic}${dna.RD.concrete}${dna.RD.action}`,
      `  真实${dna.RD.reality} 权力${dna.RD.power} 情感${dna.RD.emotion} 逻辑${dna.RD.logic} 具体${dna.RD.concrete} 行动${dna.RD.action}`,
      '',
      `【主要话语模式】`,
      ...patterns.slice(0, 5).map(p => `  ${p.pattern.id}: ${p.actualFrequency}% - ${p.pattern.template}`),
      '',
      `置信度: ${Math.round(this.calculateConfidence() * 100)}%`
    ];

    return lines.join('\n');
  }

  private encodeEPNumber(ep: EpistemologyCode): string {
    return `${ep.knowledgeSource}${ep.verificationMethod}${ep.truthView}`;
  }

  private encodeIDNumber(id: IdeologyCode): string {
    return `${id.power}${id.elite}${id.knowledge}${id.technology}${id.action}${id.class}${id.emotion}`;
  }

  private pad2(n: number): string {
    return n.toString().padStart(2, '0');
  }

  private pad3(n: number): string {
    return n.toString().padStart(3, '0');
  }

  // ============ 工具方法 ============

  private countWords(text: string, words: string[]): number {
    let count = 0;
    for (const word of words) {
      const regex = new RegExp(word, 'gi');
      const matches = text.match(regex);
      if (matches) count += matches.length;
    }
    return count;
  }

  private normalizeScore(posCount: number, negCount: number, min: number, max: number): number {
    const total = posCount + negCount;
    if (total === 0) return Math.round((min + max) / 2);

    const ratio = posCount / total;
    return Math.round(min + ratio * (max - min));
  }
}

/**
 * 便捷函数：编码文本
 */
export function encodeText(text: string): AnalysisResult {
  const encoder = new WenfengEncoder(text);
  return encoder.encode();
}

/**
 * 将DNA对象序列化为编码字符串
 */
export function serializeDNA(dna: WenfengDNA): string {
  const { PH, EP, ID, RH, SY, DN, RD } = dna;

  const phPart = `PH${pad2(PH.avgSentenceLength)}${PH.ontologyType}${PH.timeView}`;
  const epPart = `EP${EP.knowledgeSource}${EP.verificationMethod}${EP.truthView}`;
  const idPart = `ID${ID.power}${ID.elite}${ID.knowledge}${ID.technology}${ID.action}${ID.class}${ID.emotion}`;
  const rhPart = `RH${RH.argument}${RH.figure}${RH.rhythm}`;
  const syPart = `SY${pad2(SY.avgSentenceLength)}${pad2(SY.complexity)}${SY.variation}${SY.punctuation}${pad3(SY.shortRatio)}${pad3(SY.mediumRatio)}${pad3(SY.longRatio)}`;
  const dnPart = `DN${pad2(DN.vocabularyLevel)}${pad2(DN.termRatio)}${pad2(DN.colloquialRatio)}${pad2(DN.classicalRatio)}${DN.domainCode}${DN.depth}`;
  const rdPart = `RD${RD.reality}${RD.power}${RD.emotion}${RD.logic}${RD.concrete}${RD.action}`;

  return phPart + epPart + idPart + rhPart + syPart + dnPart + rdPart;
}

function pad2(n: number): string {
  return n.toString().padStart(2, '0');
}

function pad3(n: number): string {
  return n.toString().padStart(3, '0');
}
