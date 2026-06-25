/**
 * 词汇库管理器
 * 负责管理预设词汇库和自定义词汇库
 */

import {
  VocabularyBank,
  PresetVocabularyBank,
  PRESET_VOCABULARY_BANKS
} from './types';

export class VocabularyBankManager {
  private customBanks: Map<string, VocabularyBank> = new Map();
  private currentBank?: VocabularyBank;

  constructor() {}

  /**
   * 获取预设词汇库
   */
  public getPresetBank(domainCode: string): PresetVocabularyBank | undefined {
    return PRESET_VOCABULARY_BANKS[domainCode];
  }

  /**
   * 列出所有预设词汇库
   */
  public listPresetBanks(): Array<{code: string, name: string, nameZh: string}> {
    return Object.values(PRESET_VOCABULARY_BANKS).map(bank => ({
      code: bank.domainCode,
      name: bank.domainName,
      nameZh: bank.domainNameZh
    }));
  }

  /**
   * 注册自定义词汇库
   */
  public registerCustomBank(domainCode: string, bank: VocabularyBank): void {
    this.customBanks.set(domainCode, bank);
  }

  /**
   * 获取词汇库（先查自定义，再查预设）
   */
  public getBank(domainCode: string): VocabularyBank | undefined {
    // 先查自定义
    const custom = this.customBanks.get(domainCode);
    if (custom) return custom;

    // 再查预设
    return this.getPresetBank(domainCode);
  }

  /**
   * 设置当前使用的词汇库
   */
  public setCurrentBank(domainCode: string): boolean {
    const bank = this.getBank(domainCode);
    if (bank) {
      this.currentBank = bank;
      return true;
    }
    return false;
  }

  /**
   * 获取当前词汇库
   */
  public getCurrentBank(): VocabularyBank | undefined {
    return this.currentBank;
  }

  /**
   * 从文本自动识别可能的领域
   * 基于关键词匹配计算相似度
   */
  public detectDomain(text: string): Array<{domainCode: string, domainName: string, score: number}> {
    const results: Array<{domainCode: string, domainName: string, score: number}> = [];

    for (const bank of Object.values(PRESET_VOCABULARY_BANKS)) {
      const score = this.calculateDomainMatch(text, bank);
      if (score > 0.1) { // 只返回有一定匹配度的领域
        results.push({
          domainCode: bank.domainCode,
          domainName: bank.domainName,
          score
        });
      }
    }

    return results.sort((a, b) => b.score - a.score);
  }

  /**
   * 计算文本与词汇库的匹配度
   */
  private calculateDomainMatch(text: string, bank: VocabularyBank): number {
    const lowerText = text.toLowerCase();
    let matchCount = 0;
    let totalWords = 0;

    // 检查所有词汇类别
    const allVocab = [
      ...(bank.coreConcepts || []),
      ...(bank.methods || []),
      ...(bank.problems || []),
      ...(bank.technicalTerms || [])
    ];

    for (const word of allVocab) {
      totalWords++;
      if (lowerText.includes(word.toLowerCase())) {
        matchCount++;
      }
    }

    return matchCount / totalWords;
  }

  /**
   * 创建空白词汇库模板
   */
  public createEmptyBank(domainCode: string, domainName: string, domainNameZh?: string): VocabularyBank {
    return {
      domainCode,
      domainName,
      coreConcepts: [],
      figures: [],
      methods: [],
      problems: [],
      effects: [],
      attributes: [],
      technicalTerms: [],
      colloquialisms: []
    };
  }

  /**
   * 从JSON文件加载词汇库
   */
  public loadFromJSON(jsonStr: string): VocabularyBank | null {
    try {
      const data = JSON.parse(jsonStr);
      // 验证必要字段
      if (!data.domainCode || !data.domainName) {
        console.error('词汇库JSON缺少必要字段: domainCode, domainName');
        return null;
      }
      return data as VocabularyBank;
    } catch (e) {
      console.error('JSON解析失败:', e);
      return null;
    }
  }

  /**
   * 导出词汇库为JSON
   */
  public exportToJSON(bank: VocabularyBank): string {
    return JSON.stringify(bank, null, 2);
  }

  /**
   * 合并两个词汇库
   */
  public mergeBanks(base: VocabularyBank, addition: VocabularyBank): VocabularyBank {
    return {
      ...base,
      coreConcepts: [...new Set([...base.coreConcepts, ...addition.coreConcepts])],
      figures: [...new Set([...base.figures, ...addition.figures])],
      methods: [...new Set([...base.methods, ...addition.methods])],
      problems: [...new Set([...base.problems, ...addition.problems])],
      effects: [...new Set([...base.effects, ...addition.effects])],
      attributes: [...new Set([...base.attributes, ...addition.attributes])],
      technicalTerms: [...new Set([...base.technicalTerms, ...addition.technicalTerms])],
      colloquialisms: [...new Set([...base.colloquialisms, ...addition.colloquialisms])]
    };
  }

  /**
   * 验证词汇库完整性
   */
  public validateBank(bank: VocabularyBank): Array<{field: string, message: string}> {
    const errors: Array<{field: string, message: string}> = [];

    if (!bank.domainCode) {
      errors.push({ field: 'domainCode', message: '领域代码不能为空' });
    }
    if (!bank.domainName) {
      errors.push({ field: 'domainName', message: '领域名称不能为空' });
    }

    const arrays = [
      'coreConcepts', 'figures', 'methods', 'problems',
      'effects', 'attributes', 'technicalTerms', 'colloquialisms'
    ];

    for (const field of arrays) {
      const value = (bank as any)[field];
      if (!Array.isArray(value)) {
        errors.push({ field, message: '必须是数组类型' });
      }
    }

    return errors;
  }

  /**
   * 获取领域名称映射
   */
  public getDomainNameMap(): Record<string, string> {
    const map: Record<string, string> = {};
    for (const bank of Object.values(PRESET_VOCABULARY_BANKS)) {
      map[bank.domainCode] = bank.domainNameZh || bank.domainName;
    }
    for (const [code, bank] of this.customBanks) {
      map[code] = bank.domainName;
    }
    return map;
  }
}

/**
 * 便捷函数：获取默认管理器
 */
export function getDefaultVocabularyManager(): VocabularyBankManager {
  return new VocabularyBankManager();
}
