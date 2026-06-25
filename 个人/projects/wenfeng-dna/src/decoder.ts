/**
 * 文风DNA解码器
 * 根据DNA编码生成符合指定文风的文本
 */

import {
  WenfengDNA,
  DiscoursePattern,
  VocabularyBank,
  GenerationConfig,
  GenerationResult,
  ONTOLOGY_TYPES,
  ARGUMENT_TYPES,
  FIGURE_TYPES,
  RHYTHM_TYPES
} from './types';
import { GenerationAlgorithm } from './algorithms';
import { SpecialRulesEngine, RuleContext } from './special-rules-engine';
import { ContradictionHandler, BalanceResult } from './contradiction-handler';

export class WenfengDecoder {
  private dna: WenfengDNA;
  private config: GenerationConfig;
  private vocabularyBank?: VocabularyBank;
  private algorithms: GenerationAlgorithm[];
  private rulesEngine: SpecialRulesEngine;
  private contradictionHandler: ContradictionHandler;

  constructor(dna: WenfengDNA, config: GenerationConfig) {
    this.dna = dna;
    this.config = config;
    this.vocabularyBank = config.vocabularyBank;
    this.algorithms = this.loadAlgorithms();
    this.rulesEngine = new SpecialRulesEngine();
    this.contradictionHandler = new ContradictionHandler();

    // 应用特殊规则到DNA
    this.applyRulesToDNA();
  }

  /**
   * 应用特殊规则到DNA
   * 根据v3.0手册的特殊规则层调整DNA参数
   */
  private applyRulesToDNA(): void {
    const ruleOverrides = this.config.rules;
    if (!ruleOverrides) return;

    // RULE09: 评价词极端程度
    if (ruleOverrides.RULE09) {
      const emotionLevel = ruleOverrides.RULE09 === 'extreme' ? 8 : 3;
      this.dna.ID.emotion = emotionLevel;
    }

    // RULE05: 感叹号密度
    if (ruleOverrides.RULE05) {
      // 影响情感维度和修辞层
      const density = ruleOverrides.RULE05;
      if (density > 5) {
        this.dna.ID.emotion = Math.min(9, this.dna.ID.emotion + 1);
      }
    }

    // RULE10: 转折词选择
    if (ruleOverrides.RULE10 === '但是！') {
      this.dna.RH.figure = this.dna.RH.figure.replace('T', 'V'); // 用极端化替代反讽
    }
  }

  /**
   * 根据DNA生成文本
   */
  public generate(): GenerationResult {
    const algorithm = this.selectAlgorithm();
    const patterns = this.selectPatterns();
    const content = this.generateContent(algorithm, patterns);

    return {
      content,
      appliedDNA: this.dna,
      usedPatterns: patterns.map(p => p.id),
      usedVocabulary: this.collectUsedVocabulary(),
      metrics: this.calculateMetrics(content)
    };
  }

  /**
   * 选择生成算法
   */
  private selectAlgorithm(): GenerationAlgorithm {
    const { algorithm } = this.config;

    const matched = this.algorithms.find(a => a.id === algorithm);
    if (matched) return matched;

    // 根据DNA特征自动选择算法
    if (this.dna.ID.action >= 7 && this.dna.RD.action >= 7) {
      return this.algorithms.find(a => a.id === 'AL05')!; // 教程式
    }
    if (this.dna.RH.argument.includes('C')) {
      return this.algorithms.find(a => a.id === 'AL03')!; // 对比式
    }
    if (this.dna.EP.knowledgeSource === 1) {
      return this.algorithms.find(a => a.id === 'AL02')!; // 见证式
    }
    return this.algorithms.find(a => a.id === 'AL04')!; // SCQA默认
  }

  /**
   * 选择话语模式
   */
  private selectPatterns(): DiscoursePattern[] {
    const patterns: DiscoursePattern[] = [
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

    // 根据意识形态选择模式
    if (this.dna.ID.action >= 8) {
      // 行动导向强，使用更多PT05（但是！转折）
      return [patterns.find(p => p.id === 'PT05')!, patterns.find(p => p.id === 'PT01')!];
    }
    if (this.dna.RH.argument[0] === 'N') {
      // 叙事论证，使用PT02、PT04
      return [patterns.find(p => p.id === 'PT02')!, patterns.find(p => p.id === 'PT04')!];
    }
    if (this.dna.RH.argument[0] === 'C') {
      // 对比论证，使用PT09
      return [patterns.find(p => p.id === 'PT09')!];
    }

    return patterns.slice(0, 3);
  }

  /**
   * 生成内容
   */
  private generateContent(algorithm: GenerationAlgorithm, patterns: DiscoursePattern[]): string {
    const { topic } = this.config;
    const targetLength = this.config.targetLength || 500;
    const sentences: string[] = [];

    const weights = algorithm.weights;
    const totalWeight = weights.reduce((a: number, b: number) => a + b, 0);
    const stepsCount = algorithm.steps.length;

    // 检测并平衡矛盾点
    this.balanceContradictions();

    // 根据算法权重分配步骤
    for (let i = 0; i < stepsCount; i++) {
      const stepSentences = Math.round((weights[i] / totalWeight) * (targetLength / 20));
      const step = algorithm.steps[i];

      for (let j = 0; j < stepSentences; j++) {
        const sentence = this.generateSentence(step, patterns, i, j);
        sentences.push(sentence);
      }
    }

    // 补充到目标长度
    while (sentences.length < targetLength / 20) {
      sentences.push(this.generateSentence('补充', patterns, 0, sentences.length));
    }

    // 应用特殊规则到最终内容
    const finalContent = sentences.join('');
    const refinedContent = this.applySpecialRulesToContent(finalContent);

    return refinedContent;
  }

  /**
   * 平衡矛盾点
   * 根据v3.0手册的矛盾点层处理逻辑
   */
  private balanceContradictions(): void {
    const detections = this.contradictionHandler.detectContradictions(
      this.config.topic || '',
      this.dna
    );

    if (detections.length > 0) {
      // 根据检测结果调整DNA参数
      for (const detection of detections) {
        const strategy = this.getBalanceStrategy(detection.contradiction.id);
        if (strategy !== 'balanced') {
          const balanceResult: BalanceResult = this.contradictionHandler.balanceContradiction(
            detection.contradiction,
            this.dna,
            strategy
          );

          // 应用调整
          for (const adjustment of balanceResult.adjustments) {
            this.applyAdjustment(adjustment);
          }
        }
      }
    }
  }

  /**
   * 获取平衡策略
   */
  private getBalanceStrategy(contradictionId: string): 'left' | 'right' | 'balanced' {
    const recommendations = this.contradictionHandler.recommendBalanceStrategy(
      this.dna,
      this.config.topic ? '通用' : undefined
    );

    const rec = recommendations.find(r => r.contradictionId === contradictionId);
    return rec ? rec.strategy : 'balanced';
  }

  /**
   * 应用调整
   */
  private applyAdjustment(adjustment: {aspect: string; adjusted: number}): void {
    switch (adjustment.aspect) {
      case '权力维度':
        this.dna.ID.power = adjustment.adjusted;
        break;
      case '情感性':
        this.dna.RD.emotion = adjustment.adjusted;
        break;
      case '逻辑性':
        this.dna.RD.logic = adjustment.adjusted;
        break;
      case '词汇专业度':
        this.dna.DN.vocabularyLevel = adjustment.adjusted;
        break;
      case '口语占比':
        this.dna.DN.colloquialRatio = adjustment.adjusted;
        break;
    }
  }

  /**
   * 应用特殊规则到内容
   */
  private applySpecialRulesToContent(content: string): string {
    const sentences = this.splitIntoParagraphs(content);
    const refinedSentences: string[] = [];

    for (let i = 0; i < sentences.length; i++) {
      const sentence = sentences[i];
      const position: 'start' | 'middle' | 'end' =
        i === 0 ? 'start' : i === sentences.length - 1 ? 'end' : 'middle';

      const context: RuleContext = {
        dna: this.dna,
        text: sentence,
        paragraphIndex: i,
        sentenceIndex: 0,
        position,
        vocabularyBank: this.vocabularyBank
      };

      const results = this.rulesEngine.applyRules(context);
      let refined = sentence;

      // 应用规则修改
      for (const result of results) {
        for (const mod of result.modifications) {
          if (mod.type === 'insert') {
            if (mod.position === 0) {
              refined = mod.modified + refined;
            } else {
              refined = refined + mod.modified;
            }
          } else if (mod.type === 'suggest') {
            // 记录建议但不直接应用（用于报告）
          }
        }
      }

      refinedSentences.push(refined);
    }

    return refinedSentences.join('\n');
  }

  /**
   * 分割成段落
   */
  private splitIntoParagraphs(text: string): string[] {
    return text.split(/\n\n+/).filter(p => p.trim().length > 0);
  }

  /**
   * 生成单个句子
   */
  private generateSentence(
    step: string,
    patterns: DiscoursePattern[],
    stepIndex: number,
    sentenceIndex: number
  ): string {
    const pattern = patterns[stepIndex % patterns.length];
    const variables = this.fillVariables(pattern.variables, step);

    let sentence = pattern.template;
    for (const variable of variables) {
      sentence = sentence.replace(`{${variable}}`, variable);
    }

    // 根据句法特征调整句子
    sentence = this.adjustSyntax(sentence);

    // 根据修辞特征添加修辞
    sentence = this.applyRhetoric(sentence);

    return sentence + (this.dna.RH.rhythm === 1 ? '' : '，');
  }

  /**
   * 填充变量
   */
  private fillVariables(variables: string[], step: string): string[] {
    const filled: string[] = [];

    for (const variable of variables) {
      const value = this.getVariableValue(variable, step);
      filled.push(value);
    }

    return filled;
  }

  /**
   * 获取变量值
   */
  private getVariableValue(variable: string, step: string): string {
    const bank = this.vocabularyBank;

    switch (variable) {
      case '现象':
        return bank?.problems?.[0] || '很多问题';
      case '结论':
        return bank?.effects?.[0] || '这就是本质';
      case '动词':
        return ['试过', '用过', '做过', '研究过'][Math.floor(Math.random() * 4)];
      case '对象':
        return bank?.methods?.[0] || '这个方法';
      case '评价':
        return this.getEvaluationWord();
      case '条件':
        return bank?.problems?.[0] || '如果你遇到XX问题';
      case '结果':
        return bank?.effects?.[0] || '这个方法就能帮你';
      case '时长':
        return ['三年', '五年', '十年', '很久'][Math.floor(Math.random() * 4)];
      case '细节':
        return '每次都有新收获';
      case '观点':
        return bank?.coreConcepts?.[0] || '这个理念';
      case '转折':
        return '但真正有效的是另一套方法';
      case '理由':
        return '因为它直击根本';
      case '特点':
        return bank?.attributes?.[0] || '独特';
      case 'A':
        return '传统方法';
      case 'B':
        return '新方法';
      default:
        return variable;
    }
  }

  /**
   * 获取评价词
   */
  private getEvaluationWord(): string {
    if (this.dna.ID.emotion >= 7) {
      return ['惊艳', '震撼', '超级棒', '太强了'][Math.floor(Math.random() * 4)];
    }
    if (this.dna.ID.emotion <= 3) {
      return ['有效', '实用', '可行', '不错'][Math.floor(Math.random() * 4)];
    }
    return ['很好', '有用', '值得', '推荐'][Math.floor(Math.random() * 4)];
  }

  /**
   * 根据句法调整句子
   */
  private adjustSyntax(sentence: string): string {
    // 根据句长特征调整
    const targetLength = this.dna.SY.avgSentenceLength;

    if (sentence.length > targetLength * 1.5) {
      // 分割句子
      return sentence.substring(0, targetLength) + '。';
    }
    if (sentence.length < targetLength * 0.5) {
      // 扩展句子
      return sentence + '，这是非常重要的发现。';
    }

    return sentence;
  }

  /**
   * 应用修辞手法
   */
  private applyRhetoric(sentence: string): string {
    const { argument, figure, rhythm } = this.dna.RH;

    // 应用修辞手法
    if (figure.includes('V')) {
      // 极端化
      sentence = sentence.replace(/好/g, '超级好').replace(/强/g, '超强');
    }
    if (figure.includes('R') && Math.random() > 0.7) {
      // 重复
      const lastWord = sentence.slice(-5);
      sentence = sentence + '，' + lastWord + '真的很重要。';
    }
    if (figure.includes('G')) {
      // 极简格言
      if (sentence.length < 10) {
        sentence = '【' + sentence + '】';
      }
    }

    return sentence;
  }

  /**
   * 收集使用的词汇
   */
  private collectUsedVocabulary(): string[] {
    if (!this.vocabularyBank) return [];

    const used: string[] = [];
    const allVocab = [
      ...(this.vocabularyBank.coreConcepts || []),
      ...(this.vocabularyBank.methods || []),
      ...(this.vocabularyBank.attributes || [])
    ];

    return allVocab.slice(0, 20);
  }

  /**
   * 计算文本指标
   */
  private calculateMetrics(content: string): GenerationResult['metrics'] {
    const sentences = content.split(/[。！？.!?]/).filter(s => s.trim().length > 0);
    const words = content.toLowerCase().split(/\s+/).filter(w => w.length > 0);
    const avgLen = sentences.length > 0
      ? sentences.reduce((sum, s) => sum + s.length, 0) / sentences.length
      : 0;

    const bank = this.vocabularyBank;
    const technicalTerms = bank ? bank.technicalTerms?.length || 0 : 0;

    // 简单的情感词计数
    const emotionalWords = ['惊艳', '震撼', '超级', '太棒了', '爱', '恨', '痛苦', '快乐'];
    const emotionalCount = emotionalWords.filter(w => content.includes(w)).length;

    return {
      wordCount: content.length,
      sentenceCount: sentences.length,
      avgSentenceLength: Math.round(avgLen),
      uniqueWords: new Set(words).size,
      technicalTermCount: technicalTerms,
      emotionalWordCount: emotionalCount
    };
  }

  /**
   * 加载算法库
   */
  private loadAlgorithms(): GenerationAlgorithm[] {
    return [
      {
        id: 'AL01',
        name: 'FAP算法（Fear-Answer-Prompt）',
        steps: [
          '制造焦虑：描述问题，引起关注',
          '展示解决方案：提供答案',
          '给出行动指令：促使行动'
        ],
        weights: [8, 1.5, 0.5],
        description: '制造焦虑→提供答案→行动指令'
      },
      {
        id: 'AL02',
        name: '见证式算法',
        steps: [
          '个人经历：我遇到XX问题',
          '尝试过程：我试过XX方法',
          '效果展示：结果是XX',
          '推荐建议：你也可以试试'
        ],
        weights: [2, 3, 3, 2],
        description: '亲身经历→尝试→效果→推荐'
      },
      {
        id: 'AL03',
        name: '对比式算法',
        steps: [
          '列举选项：A vs B',
          '逐项对比：维度1、2、3',
          '给出结论：推荐XX'
        ],
        weights: [2, 6, 2],
        description: '对比选项→详细对比→推荐'
      },
      {
        id: 'AL04',
        name: 'SCQA算法',
        steps: [
          '描述情境（Situation）',
          '提出矛盾（Complication）',
          '引发问题（Question）',
          '给出答案（Answer）'
        ],
        weights: [2, 2, 2, 4],
        description: '情境→矛盾→问题→答案'
      },
      {
        id: 'AL05',
        name: '教程式算法',
        steps: [
          '说明目标：要达到XX效果',
          '列举步骤：第一步、第二步...',
          '注意事项：避免XX错误',
          '效果预期：坚持XX见效'
        ],
        weights: [1, 6, 2, 1],
        description: '目标→步骤→注意→预期'
      }
    ];
  }
}

/**
 * 便捷函数：根据DNA生成文本
 */
export function generateFromDNA(
  dna: WenfengDNA,
  config: GenerationConfig
): GenerationResult {
  const decoder = new WenfengDecoder(dna, config);
  return decoder.generate();
}
