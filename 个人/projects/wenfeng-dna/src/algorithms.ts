/**
 * 文风DNA算法库
 * 定义5大核心生成算法
 */

import { GenerationAlgorithm } from './types';

export { GenerationAlgorithm };
export const ALGORITHMS: GenerationAlgorithm[] = [
  {
    id: 'AL01',
    name: 'FAP算法（Fear-Answer-Prompt）',
    steps: [
      '制造焦虑：描述问题，引起关注，占80%篇幅',
      '展示解决方案：提供答案，占15%',
      '给出行动指令：促使行动，占5%'
    ],
    weights: [8, 1.5, 0.5],
    description: '恐惧-答案-提示三阶段结构，适合营销文案'
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
    description: '个人见证四段式，建立可信度'
  },
  {
    id: 'AL03',
    name: '对比式算法',
    steps: [
      '列举选项：A vs B',
      '逐项对比：从多个维度对比',
      '给出结论：推荐XX'
    ],
    weights: [2, 6, 2],
    description: '对比-分析-推荐，适合评测类内容'
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
    description: '情境-冲突-问题-答案，金字塔原理经典结构'
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
    description: '目标-步骤-注意-预期，适合教程类内容'
  }
];

/**
 * 根据DNA特征推荐算法
 */
export function recommendAlgorithm(dna: import('./types').WenfengDNA): string {
  const { ID, RH, EP } = dna;

  // 高行动导向 → AL05（教程式）
  if (ID.action >= 8) return 'AL05';

  // 使用对比论证 → AL03（对比式）
  if (RH.argument.includes('C')) return 'AL03';

  // 经验主义知识来源 → AL02（见证式）
  if (EP.knowledgeSource === 1) return 'AL02';

  // 恐惧型论证（包含"问题""风险"等）→ AL01（FAP）
  if (RH.argument.includes('U') && ID.emotion >= 7) return 'AL01';

  // 默认AL04（SCQA）
  return 'AL04';
}
