/**
 * 文风DNA分析器
 * 比较不同文本的文风差异
 */

import {
  WenfengDNA,
  AnalysisResult,
  ComparisonResult,
  VocabularyBank,
  ONTOLOGY_TYPES
} from './types';
import { WenfengEncoder } from './encoder';

export class WenfengAnalyzer {
  private dna1: WenfengDNA;
  private dna2: WenfengDNA;
  private result1: AnalysisResult;
  private result2: AnalysisResult;

  constructor(text1: string, text2: string) {
    const encoder1 = new WenfengEncoder(text1);
    const encoder2 = new WenfengEncoder(text2);
    this.result1 = encoder1.encode();
    this.result2 = encoder2.encode();
    this.dna1 = this.result1.dna;
    this.dna2 = this.result2.dna;
  }

  /**
   * 对比两个DNA编码
   */
  public compare(): ComparisonResult {
    const similarities = this.calculateSimilarities();
    const differences = this.calculateDifferences();
    const overallSimilarity = this.calculateOverallSimilarity(similarities);

    return {
      dna1: this.dna1,
      dna2: this.dna2,
      similarities,
      differences,
      overallSimilarity
    };
  }

  /**
   * 计算相似度
   */
  private calculateSimilarities(): Array<{dimension: string, score: number}> {
    const dimensions = [
      { name: 'PH', score: this.comparePhilosophy() },
      { name: 'EP', score: this.compareEpistemology() },
      { name: 'ID', score: this.compareIdeology() },
      { name: 'RH', score: this.compareRhetoric() },
      { name: 'SY', score: this.compareSyntax() },
      { name: 'RD', score: this.compareRadar() }
    ];

    return dimensions.map(d => ({
      dimension: d.name,
      score: Math.round(d.score * 100) / 100
    }));
  }

  /**
   * 计算哲学层相似度
   */
  private comparePhilosophy(): number {
    const { PH: p1 } = this.dna1;
    const { PH: p2 } = this.dna2;

    const lenDiff = 1 - Math.abs(p1.avgSentenceLength - p2.avgSentenceLength) / 50;
    const ontoMatch = p1.ontologyType === p2.ontologyType ? 1 : 0;
    const timeMatch = p1.timeView === p2.timeView ? 1 : 0;

    return (lenDiff * 0.3 + ontoMatch * 0.35 + timeMatch * 0.35);
  }

  /**
   * 计算认识论相似度
   */
  private compareEpistemology(): number {
    const { EP: e1 } = this.dna1;
    const { EP: e2 } = this.dna2;

    const sourceMatch = e1.knowledgeSource === e2.knowledgeSource ? 1 : 0;
    const verifyMatch = e1.verificationMethod === e2.verificationMethod ? 1 : 0;
    const truthMatch = e1.truthView === e2.truthView ? 1 : 0;

    return (sourceMatch + verifyMatch + truthMatch) / 3;
  }

  /**
   * 计算意识形态相似度
   */
  private compareIdeology(): number {
    const { ID: i1 } = this.dna1;
    const { ID: i2 } = this.dna2;

    const dimensions = ['power', 'elite', 'knowledge', 'technology', 'action', 'class', 'emotion'];
    let totalDiff = 0;

    for (const dim of dimensions) {
      const v1 = i1[dim as keyof typeof i1] as number;
      const v2 = i2[dim as keyof typeof i2] as number;
      totalDiff += 1 - Math.abs(v1 - v2) / 9;
    }

    return totalDiff / 7;
  }

  /**
   * 计算修辞层相似度
   */
  private compareRhetoric(): number {
    const { RH: r1 } = this.dna1;
    const { RH: r2 } = this.dna2;

    // 论证相似度：相同字符比例
    const argMatch = this.stringSimilarity(r1.argument, r2.argument);
    // 修辞相似度
    const figMatch = this.stringSimilarity(r1.figure, r2.figure);
    // 节奏匹配
    const rhythmMatch = r1.rhythm === r2.rhythm ? 1 : 0;

    return (argMatch * 0.4 + figMatch * 0.4 + rhythmMatch * 0.2);
  }

  /**
   * 计算句法相似度
   */
  private compareSyntax(): number {
    const { SY: s1 } = this.dna1;
    const { SY: s2 } = this.dna2;

    const lenDiff = 1 - Math.abs(s1.avgSentenceLength - s2.avgSentenceLength) / 50;
    const compDiff = 1 - Math.abs(s1.complexity - s2.complexity) / 80;
    const varMatch = s1.variation === s2.variation ? 1 : 0;
    const punctMatch = s1.punctuation === s2.punctuation ? 1 : 0;

    const distDiff =
      1 - (Math.abs(s1.shortRatio - s2.shortRatio) +
           Math.abs(s1.mediumRatio - s2.mediumRatio) +
           Math.abs(s1.longRatio - s2.longRatio)) / 300;

    return (lenDiff + compDiff + varMatch + punctMatch + distDiff) / 5;
  }

  /**
   * 计算雷达相似度
   */
  private compareRadar(): number {
    const { RD: r1 } = this.dna1;
    const { RD: r2 } = this.dna2;

    const dimensions = ['reality', 'power', 'emotion', 'logic', 'concrete', 'action'];
    let totalDiff = 0;

    for (const dim of dimensions) {
      const v1 = r1[dim as keyof typeof r1] as number;
      const v2 = r2[dim as keyof typeof r2] as number;
      totalDiff += 1 - Math.abs(v1 - v2) / 9;
    }

    return totalDiff / 6;
  }

  /**
   * 计算差异
   */
  private calculateDifferences(): Array<{dimension: string, value1: any, value2: any}> {
    const differences: Array<{dimension: string, value1: any, value2: any}> = [];

    // 哲学层
    if (this.dna1.PH.ontologyType !== this.dna2.PH.ontologyType) {
      differences.push({
        dimension: 'PH本体论',
        value1: ONTOLOGY_TYPES[this.dna1.PH.ontologyType],
        value2: ONTOLOGY_TYPES[this.dna2.PH.ontologyType]
      });
    }

    // 意识形态
    const idDims = ['power', 'elite', 'knowledge', 'technology', 'action', 'class', 'emotion'];
    for (const dim of idDims) {
      const v1 = this.dna1.ID[dim as keyof typeof this.dna1.ID] as number;
      const v2 = this.dna2.ID[dim as keyof typeof this.dna2.ID] as number;
      if (Math.abs(v1 - v2) >= 3) {
        differences.push({
          dimension: `ID${dim.toUpperCase()}`,
          value1: v1,
          value2: v2
        });
      }
    }

    // 修辞
    if (this.dna1.RH.argument !== this.dna2.RH.argument) {
      differences.push({
        dimension: 'RH论证方式',
        value1: this.dna1.RH.argument,
        value2: this.dna2.RH.argument
      });
    }

    return differences;
  }

  /**
   * 计算整体相似度
   */
  private calculateOverallSimilarity(similarities: Array<{dimension: string, score: number}>): number {
    const total = similarities.reduce((sum, s) => sum + s.score, 0);
    return Math.round((total / similarities.length) * 100) / 100;
  }

  /**
   * 字符串相似度（Jaccard）
   */
  private stringSimilarity(s1: string, s2: string): number {
    const set1 = new Set(s1.split(''));
    const set2 = new Set(s2.split(''));
    const intersection = new Set([...set1].filter(x => set2.has(x)));
    const union = new Set([...set1, ...set2]);

    return intersection.size / union.size;
  }

  /**
   * 生成对比报告
   */
  public generateComparisonReport(): string {
    const comparison = this.compare();
    const { dna1, dna2, similarities, differences, overallSimilarity } = comparison;

    const lines: string[] = [
      '=== 文风DNA对比报告 ===',
      '',
      `【文本1编码】PH${dna1.PH.avgSentenceLength}${dna1.PH.ontologyType}${dna1.PH.timeView}`,
      `               ID${this.encodeID(dna1.ID)}`,
      `               RH${dna1.RH.argument}${dna1.RH.figure}${dna1.RH.rhythm}`,
      '',
      `【文本2编码】PH${dna2.PH.avgSentenceLength}${dna2.PH.ontologyType}${dna2.PH.timeView}`,
      `               ID${this.encodeID(dna2.ID)}`,
      `               RH${dna2.RH.argument}${dna2.RH.figure}${dna2.RH.rhythm}`,
      '',
      '【维度相似度】',
      ...similarities.map(s => `  ${s.dimension}: ${Math.round(s.score * 100)}%`),
      '',
      `【整体相似度】${Math.round(overallSimilarity * 100)}%`,
      overallSimilarity > 0.7 ? '  → 文风高度相似' :
      overallSimilarity > 0.4 ? '  → 文风中等相似' :
      '  → 文风差异显著',
      '',
      '【主要差异】',
      ...differences.map(d => `  ${d.dimension}: ${d.value1} vs ${d.value2}`),
      '',
      '【风格特征对比】',
      this.compareFeatures()
    ];

    return lines.join('\n');
  }

  /**
   * 特征对比
   */
  private compareFeatures(): string {
    const features: string[] = [];

    // 句长对比
    const len1 = this.dna1.PH.avgSentenceLength;
    const len2 = this.dna2.PH.avgSentenceLength;
    features.push(
      len1 > len2 ? '  文本1句子更长，更沉稳' : '  文本2句子更长，更沉稳'
    );

    // 情感浓度对比
    if (this.dna1.ID.emotion > this.dna2.ID.emotion + 2) {
      features.push('  文本1情感更浓烈');
    } else if (this.dna2.ID.emotion > this.dna1.ID.emotion + 2) {
      features.push('  文本2情感更浓烈');
    }

    // 行动导向对比
    if (this.dna1.ID.action > this.dna2.ID.action + 2) {
      features.push('  文本1更强调行动');
    } else if (this.dna2.ID.action > this.dna1.ID.action + 2) {
      features.push('  文本2更强调行动');
    }

    return features.join('\n');
  }

  private encodeID(id: import('./types').IdeologyCode): string {
    return `${id.power}${id.elite}${id.knowledge}${id.technology}${id.action}${id.class}${id.emotion}`;
  }
}

/**
 * 便捷函数：对比两段文本
 */
export function compareTexts(text1: string, text2: string): ComparisonResult {
  const analyzer = new WenfengAnalyzer(text1, text2);
  return analyzer.compare();
}

/**
 * 便捷函数：生成对比报告
 */
export function generateComparisonReport(text1: string, text2: string): string {
  const analyzer = new WenfengAnalyzer(text1, text2);
  return analyzer.generateComparisonReport();
}
