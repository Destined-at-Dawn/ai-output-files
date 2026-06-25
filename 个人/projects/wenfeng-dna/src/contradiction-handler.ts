/**
 * 矛盾点处理器
 * 实现v3.0手册中的矛盾点检测与平衡
 */

import { Contradiction, PRESET_CONTRADICTIONS, WenfengDNA } from './types';

export interface ContradictionDetection {
  contradiction: Contradiction;
  detected: boolean;
  severity: 'low' | 'medium' | 'high';
  evidence: string[];
  suggestions: string[];
}

export interface BalanceResult {
  contradictionId: string;
  originalBalance: number; // -1到1，负偏左，正偏右
  appliedBalance: number;
  adjustments: Array<{
    aspect: string;
    original: number;
    adjusted: number;
    reason: string;
  }>;
}

export class ContradictionHandler {
  private contradictions: Map<string, Contradiction>;

  constructor() {
    this.contradictions = new Map();
    // 加载预设矛盾点
    for (const cd of PRESET_CONTRADICTIONS) {
      this.contradictions.set(cd.id, cd);
    }
  }

  /**
   * 检测文本中的矛盾点
   */
  public detectContradictions(text: string, dna: WenfengDNA): ContradictionDetection[] {
    const results: ContradictionDetection[] = [];

    for (const cd of this.contradictions.values()) {
      const detection = this.detectSingleContradiction(cd, text, dna);
      if (detection.detected) {
        results.push(detection);
      }
    }

    return results;
  }

  /**
   * 检测单个矛盾点
   */
  private detectSingleContradiction(
    cd: Contradiction,
    text: string,
    dna: WenfengDNA
  ): ContradictionDetection {
    const evidence: string[] = [];
    let severity: 'low' | 'medium' | 'high' = 'low';
    let detected = false;

    switch (cd.id) {
      case 'CD01': // 权威 vs 平等
        detected = this.detectAuthorityVsEquality(text, dna, evidence, severity);
        break;

      case 'CD02': // 理性 vs 感性
        detected = this.detectRationalVsEmotional(text, dna, evidence, severity);
        break;

      case 'CD03': // 批判 vs 建设
        detected = this.detectCriticalVsConstructive(text, evidence);
        break;

      case 'CD04': // 普世 vs 个性
        detected = this.detectUniversalVsIndividual(text, evidence);
        break;

      case 'CD05': // 专业 vs 通俗
        detected = this.detectProfessionalVsPopular(text, dna, evidence);
        break;
    }

    // 根据证据数量调整严重程度
    if (evidence.length >= 3) severity = 'high';
    else if (evidence.length >= 2) severity = 'medium';

    return {
      contradiction: cd,
      detected,
      severity,
      evidence,
      suggestions: this.generateSuggestions(cd, severity)
    };
  }

  // ============ 矛盾点检测方法 ============

  private detectAuthorityVsEquality(
    text: string,
    dna: WenfengDNA,
    evidence: string[],
    severity: 'low' | 'medium' | 'high'
  ): boolean {
    const authorityPatterns = ['必须', '应该', '一定', '绝对', '权威', '专家说', '研究表明'];
    const equalityPatterns = ['你可以', '你可以试试', '我觉得', '我认为', '个人经验', '你也可以'];

    const hasAuthority = authorityPatterns.some(p => text.includes(p));
    const hasEquality = equalityPatterns.some(p => text.includes(p));

    if (hasAuthority && hasEquality) {
      evidence.push('同时存在权威表述和平等表述');
      severity = 'medium';
      return true;
    }

    // 检查ID维度是否处于矛盾状态
    if (dna.ID.power >= 7 && dna.ID.emotion >= 7) {
      evidence.push('高权力+高情感维度易产生权威-平等矛盾');
      return true;
    }

    return false;
  }

  private detectRationalVsEmotional(
    text: string,
    dna: WenfengDNA,
    evidence: string[],
    severity: 'low' | 'medium' | 'high'
  ): boolean {
    const rationalPatterns = ['因为', '所以', '因此', '数据', '研究', '实验', '证明', '统计'];
    const emotionalPatterns = ['!!!', '太棒了', '惊艳', '震撼', '感动', '爱', '恨'];

    const hasRational = rationalPatterns.some(p => text.includes(p));
    const hasEmotional = emotionalPatterns.some(p => text.includes(p));

    if (hasRational && hasEmotional) {
      evidence.push('同时存在理性论证和情感表达');
      if (hasRational && hasEmotional && text.includes('但是')) {
        severity = 'high';
        evidence.push('使用转折词连接理性与感性');
      }
      return true;
    }

    return false;
  }

  private detectCriticalVsConstructive(text: string, evidence: string[]): boolean {
    const criticalPatterns = ['问题', '弊端', '缺陷', '隐患', '错误', '不应该', '都是错的'];
    const constructivePatterns = ['应该', '建议', '可以', '解决方案', '方法', '步骤'];

    const hasCritical = criticalPatterns.some(p => text.includes(p));
    const hasConstructive = constructivePatterns.some(p => text.includes(p));

    if (hasCritical && hasConstructive) {
      evidence.push('同时包含批判性表述和建设性建议');
      return true;
    }

    return false;
  }

  private detectUniversalVsIndividual(text: string, evidence: string[]): boolean {
    const universalPatterns = ['所有人', '每个人都', '普遍', '一定', '总是', '所有人都会'];
    const individualPatterns = ['因人而异', '看情况', '如果你', '具体', '有些人', '可能'];

    const hasUniversal = universalPatterns.some(p => text.includes(p));
    const hasIndividual = individualPatterns.some(p => text.includes(p));

    if (hasUniversal && hasIndividual) {
      evidence.push('同时给出普世建议和个性化提示');
      return true;
    }

    return false;
  }

  private detectProfessionalVsPopular(
    text: string,
    dna: WenfengDNA,
    evidence: string[]
  ): boolean {
    // 检测是否有专业术语后面紧跟解释
    const technicalTermPatterns = [
      /([A-Za-z\u4e00-\u9fa5]{2,6})（([A-Za-z\u4e00-\u9fa5]{2,10})）/g, // 术语（解释）
      /([A-Za-z\u4e00-\u9fa5]{2,6})，([^，]{2,10})，/g // 术语，解释，
    ];

    let hasTermWithExplanation = false;
    for (const pattern of technicalTermPatterns) {
      const matches = text.match(pattern);
      if (matches && matches.length > 0) {
        hasTermWithExplanation = true;
        evidence.push(`术语"${matches[0].match(/^([A-Za-z\u4e00-\u9fa5]{2,6})/)?.[0]}"有解释`);
      }
    }

    // 检查DN编码是否显示专业-通俗平衡
    if (dna.DN.vocabularyLevel >= 7 && dna.DN.colloquialRatio >= 6) {
      evidence.push('词汇专业度高但口语占比也高，存在专业-通俗张力');
      return true;
    }

    return hasTermWithExplanation;
  }

  /**
   * 生成建议
   */
  private generateSuggestions(cd: Contradiction, severity: 'low' | 'medium' | 'high'): string[] {
    const baseSuggestions = [cd.resolution];

    if (severity === 'high') {
      baseSuggestions.push('建议调整文本结构，明确主次关系');
      baseSuggestions.push('考虑将矛盾点分开到不同段落');
    }

    return baseSuggestions;
  }

  /**
   * 平衡矛盾点
   * 根据resolution调整DNA维度值
   */
  public balanceContradiction(
    cd: Contradiction,
    currentDNA: WenfengDNA,
    strategy: 'left' | 'right' | 'balanced'
  ): BalanceResult {
    const originalBalance = this.calculateContradictionBalance(cd, currentDNA);
    let targetBalance = 0;
    let appliedBalance = originalBalance;

    const adjustments: BalanceResult['adjustments'] = [];

    switch (cd.id) {
      case 'CD01': // 权威 vs 平等
        if (strategy === 'left') { // 偏权威
          targetBalance = 0.7;
          adjustments.push({
            aspect: '权力维度',
            original: currentDNA.ID.power,
            adjusted: Math.min(9, currentDNA.ID.power + 1),
            reason: '增强权威感'
          });
        } else if (strategy === 'right') { // 偏平等
          targetBalance = -0.7;
          adjustments.push({
            aspect: '权力维度',
            original: currentDNA.ID.power,
            adjusted: Math.max(1, currentDNA.ID.power - 1),
            reason: '增强平等感'
          });
        }
        break;

      case 'CD02': // 理性 vs 感性
        if (strategy === 'left') { // 偏理性
          targetBalance = 0.7;
          adjustments.push({
            aspect: '逻辑性',
            original: currentDNA.RD.logic,
            adjusted: Math.min(9, currentDNA.RD.logic + 1),
            reason: '增强逻辑性'
          });
          adjustments.push({
            aspect: '情感性',
            original: currentDNA.RD.emotion,
            adjusted: Math.max(1, currentDNA.RD.emotion - 1),
            reason: '降低情感强度'
          });
        } else if (strategy === 'right') { // 偏感性
          targetBalance = -0.7;
          adjustments.push({
            aspect: '情感性',
            original: currentDNA.RD.emotion,
            adjusted: Math.min(9, currentDNA.RD.emotion + 1),
            reason: '增强情感表达'
          });
        }
        break;

      case 'CD05': // 专业 vs 通俗
        if (strategy === 'left') { // 偏专业
          targetBalance = 0.7;
          adjustments.push({
            aspect: '词汇专业度',
            original: currentDNA.DN.vocabularyLevel,
            adjusted: Math.min(9, currentDNA.DN.vocabularyLevel + 1),
            reason: '提升专业度'
          });
          adjustments.push({
            aspect: '口语占比',
            original: currentDNA.DN.colloquialRatio,
            adjusted: Math.max(1, currentDNA.DN.colloquialRatio - 1),
            reason: '降低口语化'
          });
        } else if (strategy === 'right') { // 偏通俗
          targetBalance = -0.7;
          adjustments.push({
            aspect: '词汇专业度',
            original: currentDNA.DN.vocabularyLevel,
            adjusted: Math.max(1, currentDNA.DN.vocabularyLevel - 1),
            reason: '降低专业度'
          });
          adjustments.push({
            aspect: '口语占比',
            original: currentDNA.DN.colloquialRatio,
            adjusted: Math.min(9, currentDNA.DN.colloquialRatio + 1),
            reason: '增加口语化'
          });
        }
        break;
    }

    // 计算调整后的平衡值
    appliedBalance = originalBalance + (targetBalance - originalBalance) * 0.5;

    return {
      contradictionId: cd.id,
      originalBalance,
      appliedBalance,
      adjustments
    };
  }

  /**
   * 计算矛盾点当前平衡状态
   * 返回-1到1，负值表示偏右（第二个维度），正值表示偏左（第一个维度）
   */
  private calculateContradictionBalance(cd: Contradiction, dna: WenfengDNA): number {
    switch (cd.id) {
      case 'CD01': // 权威 vs 平等 (power高=偏权威)
        return (dna.ID.power - 5) / 4; // -1到1

      case 'CD02': // 理性 vs 感性 (logic高=偏理性)
        return (dna.RD.logic - dna.RD.emotion) / 8;

      case 'CD05': // 专业 vs 通俗 (vocabularyLevel高=偏专业)
        return (dna.DN.vocabularyLevel - dna.DN.colloquialRatio) / 8;

      default:
        return 0;
    }
  }

  /**
   * 生成矛盾点分析报告
   */
  public generateContradictionReport(detections: ContradictionDetection[]): string {
    if (detections.length === 0) {
      return '未检测到明显的矛盾点，文风一致性良好。';
    }

    const lines: string[] = [
      '=== 矛盾点检测报告 ===',
      '',
      `检测到${detections.length}个矛盾点:`,
      ''
    ];

    for (const detection of detections) {
      lines.push(`【${detection.contradiction.id}】${detection.contradiction.name}`);
      lines.push(`  严重程度: ${detection.severity === 'high' ? '高' : detection.severity === 'medium' ? '中' : '低'}`);
      lines.push(`  表现:`);
      for (const ev of detection.evidence) {
        lines.push(`    • ${ev}`);
      }
      lines.push(`  处理建议: ${detection.contradiction.resolution}`);
      if (detection.suggestions.length > 1) {
        lines.push(`  额外建议:`);
        for (const sug of detection.suggestions.slice(1)) {
          lines.push(`    • ${sug}`);
        }
      }
      lines.push('');
    }

    return lines.join('\n');
  }

  /**
   * 添加自定义矛盾点
   */
  public addCustomContradiction(contradiction: Contradiction): void {
    this.contradictions.set(contradiction.id, contradiction);
  }

  /**
   * 获取所有矛盾点
   */
  public getAllContradictions(): Contradiction[] {
    return Array.from(this.contradictions.values());
  }

  /**
   * 根据DNA推荐矛盾点平衡策略
   */
  public recommendBalanceStrategy(
    dna: WenfengDNA,
    targetAudience?: string
): Array<{contradictionId: string, strategy: 'left' | 'right' | 'balanced', reason: string}> {
    const recommendations: Array<{contradictionId: string, strategy: 'left' | 'right' | 'balanced', reason: string}> = [];

    for (const cd of this.contradictions.values()) {
      let strategy: 'left' | 'right' | 'balanced' = 'balanced';
      let reason = '';

      switch (cd.id) {
        case 'CD01': // 权威 vs 平等
          if (targetAudience === '新手' || targetAudience === '初学者') {
            strategy = 'right'; // 偏平等
            reason = '面向新手需要更平等的对话感';
          } else if (targetAudience === '专家' || targetAudience === '同行') {
            strategy = 'left'; // 偏权威
            reason = '面向专家需要建立专业权威';
          }
          break;

        case 'CD02': // 理性 vs 感性
          if (dna.ID.emotion >= 7) {
            strategy = 'right'; // 偏感性
            reason = '高情感维度适合感性表达';
          } else {
            strategy = 'left'; // 偏理性
            reason = '低情感维度适合理性表达';
          }
          break;

        case 'CD05': // 专业 vs 通俗
          if (dna.DN.domainCode === 'ED' || dna.DN.domainCode === 'PH') {
            strategy = 'right'; // 偏通俗
            reason = '教育/哲学领域需要降低专业门槛';
          } else if (dna.DN.domainCode === 'SK') {
            strategy = 'left'; // 偏专业
            reason = '护肤领域需要建立专业信任';
          }
          break;
      }

      recommendations.push({
        contradictionId: cd.id,
        strategy,
        reason
      });
    }

    return recommendations;
  }
}

/**
 * 便捷函数
 */
export function createContradictionHandler(): ContradictionHandler {
  return new ContradictionHandler();
}
