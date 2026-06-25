/**
 * 特殊规则引擎
 * 实现v3.0手册中的RULE01-RULE10
 */

import { SpecialRule, PRESET_SPECIAL_RULES } from './types';

export interface RuleContext {
  dna: any; // WenfengDNA
  text: string;
  paragraphIndex: number;
  sentenceIndex: number;
  position: 'start' | 'middle' | 'end';
  vocabularyBank?: any;
}

export interface RuleResult {
  ruleId: string;
  applied: boolean;
  modifications: Array<{
    type: 'insert' | 'replace' | 'delete' | 'suggest';
    position: number;
    original?: string;
    modified: string;
  }>;
}

export class SpecialRulesEngine {
  private rules: Map<string, SpecialRule>;
  private customRules: SpecialRule[] = [];

  constructor() {
    this.rules = new Map();
    // 加载预设规则
    for (const rule of PRESET_SPECIAL_RULES) {
      this.rules.set(rule.id, rule);
    }
  }

  /**
   * 添加自定义规则
   */
  public addCustomRule(rule: SpecialRule): void {
    this.customRules.push(rule);
    this.rules.set(rule.id, rule);
  }

  /**
   * 移除规则
   */
  public removeRule(ruleId: string): boolean {
    return this.rules.delete(ruleId);
  }

  /**
   * 获取规则
   */
  public getRule(ruleId: string): SpecialRule | undefined {
    return this.rules.get(ruleId);
  }

  /**
   * 列出所有规则
   */
  public listRules(): SpecialRule[] {
    return Array.from(this.rules.values());
  }

  /**
   * 应用规则到文本
   */
  public applyRules(
    context: RuleContext,
    ruleIds?: string[]
  ): RuleResult[] {
    const results: RuleResult[] = [];
    const targetRules = ruleIds
      ? ruleIds.map(id => this.rules.get(id)).filter(Boolean) as SpecialRule[]
      : this.listRules();

    for (const rule of targetRules) {
      const result = this.applyRule(rule, context);
      if (result.applied) {
        results.push(result);
      }
    }

    return results;
  }

  /**
   * 应用单个规则
   */
  private applyRule(rule: SpecialRule, context: RuleContext): RuleResult {
    const result: RuleResult = {
      ruleId: rule.id,
      applied: false,
      modifications: []
    };

    const { condition } = rule;
    const { dna, text, position, paragraphIndex } = context;

    // 根据条件判断是否应用规则
    let shouldApply = false;

    switch (condition) {
      case '句首':
        shouldApply = position === 'start' && this.shouldApplyStartRule(rule, dna);
        break;

      case '每段':
        shouldApply = paragraphIndex > 0 && this.shouldApplyParagraphRule(rule, dna, context);
        break;

      case '结尾':
        shouldApply = position === 'end' && this.shouldApplyEndRule(rule, dna);
        break;

      case '感叹号':
        shouldApply = this.shouldApplyExclamationRule(rule, text);
        break;

      case '专业术语':
        shouldApply = this.shouldApplyTermRule(rule, context);
        break;

      case '人物/品牌名':
        shouldApply = this.shouldApplyNameRule(rule, context);
        break;

      case '数字':
        shouldApply = this.shouldApplyNumberRule(rule, text);
        break;

      case '评价词':
        shouldApply = this.shouldApplyEvaluationRule(rule, dna);
        break;

      case '转折':
        shouldApply = this.shouldApplyTransitionRule(rule, dna);
        break;

      default:
        // 自定义条件
        shouldApply = this.evaluateCustomCondition(condition, context);
    }

    if (shouldApply) {
      result.applied = true;
      result.modifications = this.generateModifications(rule, context);
    }

    return result;
  }

  // ============ 规则条件判断方法 ============

  private shouldApplyStartRule(rule: SpecialRule, dna: any): boolean {
    // RULE01: 句首设问式频率控制
    // 基于RH.argument判断是否适合设问
    if (rule.id === 'RULE01') {
      // 叙事论证或设问修辞时更可能使用句首设问
      return dna.RH?.argument?.includes('N') || dna.RH?.figure?.includes('Q');
    }
    return Math.random() < 0.4;
  }

  private shouldApplyParagraphRule(rule: SpecialRule, dna: any, context: RuleContext): boolean {
    if (rule.id === 'RULE02') {
      // 检查段落是否已包含"我XX过"
      const hasSelfReference = context.text.includes('我') &&
        (context.text.includes('试过') || context.text.includes('过') || context.text.includes('了'));
      return !hasSelfReference;
    }
    if (rule.id === 'RULE04') {
      // 检查是否包含核心概念词
      const coreConcepts = context.vocabularyBank?.coreConcepts || [];
      return !coreConcepts.some((c: string) => context.text.includes(c));
    }
    return true;
  }

  private shouldApplyEndRule(rule: SpecialRule, dna: any): boolean {
    if (rule.id === 'RULE03') {
      // 检查是否已有行动指令
      const actionWords = ['试试', '建议', '可以', '应该', '不妨', '推荐'];
      return !actionWords.some(word => dna?.text?.includes(word));
    }
    return true;
  }

  private shouldApplyExclamationRule(rule: SpecialRule, text: string): boolean {
    // RULE05: 感叹号密度控制
    const exclamationCount = (text.match(/[!！]/g) || []).length;
    const wordCount = text.length;
    const density = (exclamationCount / wordCount) * 100;

    // 根据情感浓度调整
    const targetDensity = 3; // 默认3个/百字
    return density < targetDensity && Math.random() < 0.3;
  }

  private shouldApplyTermRule(rule: SpecialRule, context: RuleContext): boolean {
    // RULE06: 专业术语首次出现需解释
    // 这个主要用于生成时的判断，分析阶段主要用于标记
    return context.vocabularyBank?.technicalTerms?.some(
      (term: string) => context.text.includes(term)
    ) || false;
  }

  private shouldApplyNameRule(rule: SpecialRule, context: RuleContext): boolean {
    // RULE07: 人物品牌名首次全称
    const figures = context.vocabularyBank?.figures || [];
    return figures.some((f: string) => context.text.includes(f));
  }

  private shouldApplyNumberRule(rule: SpecialRule, text: string): boolean {
    // RULE08: 数字表达
    // 检测是否有模糊数字需要精确化
    const vagueNumbers = ['很多', '很少', '大量', '少数', '不少', '许多'];
    return vagueNumbers.some(v => text.includes(v));
  }

  private shouldApplyEvaluationRule(rule: SpecialRule, dna: any): boolean {
    // RULE09: 评价词极端程度控制
    const emotionLevel = dna?.ID?.emotion || 5;
    return emotionLevel >= 7 || emotionLevel <= 3;
  }

  private shouldApplyTransitionRule(rule: SpecialRule, dna: any): boolean {
    // RULE10: 转折词选择
    // 高情感用"但是！"，低情感用"然而"
    return true; // 这个规则总是需要考虑
  }

  private evaluateCustomCondition(condition: string, context: RuleContext): boolean {
    // 简单实现：随机应用，实际应该解析condition表达式
    return Math.random() < 0.5;
  }

  /**
   * 生成规则修改建议
   */
  private generateModifications(rule: SpecialRule, context: RuleContext): RuleResult['modifications'] {
    const modifications: RuleResult['modifications'] = [];

    const { behavior } = rule;
    const { text, position } = context;

    switch (rule.id) {
      case 'RULE02': // 每段必须包含"我XX过"
        if (!text.includes('我')) {
          modifications.push({
            type: 'insert',
            position: position === 'start' ? 0 : text.length,
            modified: '我试过，'
          });
        }
        break;

      case 'RULE03': // 结尾有行动指令
        if (!this.hasActionWord(text)) {
          const actionEndings = ['你可以试试。', '建议你尝试。', '不妨一试。'];
          modifications.push({
            type: 'insert',
            position: text.length,
            modified: ' ' + actionEndings[Math.floor(Math.random() * actionEndings.length)]
          });
        }
        break;

      case 'RULE05': // 感叹号密度
        const exclamationCount = (text.match(/[!！]/g) || []).length;
        if (exclamationCount === 0 && Math.random() < 0.3) {
          modifications.push({
            type: 'replace',
            position: text.length - 1,
            original: '。',
            modified: '！'
          });
        }
        break;

      case 'RULE09': // 评价词
        const evaluation = this.getEvaluationByEmotion(context.dna?.ID?.emotion);
        modifications.push({
          type: 'suggest',
          position: 0,
          modified: `建议使用评价词: ${evaluation}`
        });
        break;
    }

    return modifications;
  }

  private hasActionWord(text: string): boolean {
    const actionWords = ['试试', '建议', '可以', '应该', '不妨', '推荐', '行动', '开始'];
    return actionWords.some(word => text.includes(word));
  }

  private getEvaluationByEmotion(emotion: number): string {
    if (emotion >= 7) return ['惊艳', '震撼', '超级棒', '太强了'][Math.floor(Math.random() * 4)];
    if (emotion <= 3) return ['有效', '实用', '可行', '不错'][Math.floor(Math.random() * 4)];
    return ['很好', '有用', '值得', '推荐'][Math.floor(Math.random() * 4)];
  }

  /**
   * 生成规则报告
   */
  public generateRulesReport(rules?: string[]): string {
    const targetRules = rules
      ? rules.map(id => this.rules.get(id)).filter(Boolean) as SpecialRule[]
      : this.listRules();

    const lines: string[] = [
      '=== 特殊规则报告 ===',
      '',
      '【预设规则】'
    ];

    for (const rule of targetRules) {
      lines.push(`  ${rule.id}: ${rule.description}`);
      if (rule.example) {
        lines.push(`    示例: ${rule.example}`);
      }
      lines.push(`    条件: ${rule.condition} → 行为: ${rule.behavior}`);
      lines.push('');
    }

    lines.push(`共${targetRules.length}条规则`);
    return lines.join('\n');
  }

  /**
   * 验证规则配置
   */
  public validateRule(rule: Partial<SpecialRule>): Array<{field: string, message: string}> {
    const errors: Array<{field: string, message: string}> = [];

    if (!rule.id) {
      errors.push({ field: 'id', message: '规则ID不能为空' });
    }
    if (!rule.condition) {
      errors.push({ field: 'condition', message: '条件不能为空' });
    }
    if (!rule.behavior) {
      errors.push({ field: 'behavior', message: '行为不能为空' });
    }
    if (!rule.description) {
      errors.push({ field: 'description', message: '描述不能为空' });
    }

    return errors;
  }
}

/**
 * 便捷函数
 */
export function createRulesEngine(): SpecialRulesEngine {
  return new SpecialRulesEngine();
}
