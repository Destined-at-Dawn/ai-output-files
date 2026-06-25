/**
 * 文风DNA编解码系统 v3.0
 * 基于"文风DNA编解码手册"的完整实现
 *
 * @author Claude Code
 * @license MIT
 */

// ============ 类型导出 ============
export * from './types';

// ============ 核心类导出 ============
export { WenfengEncoder } from './encoder';
export { WenfengDecoder } from './decoder';
export { WenfengAnalyzer } from './analyzer';

// ============ 辅助模块导出 ============
export { VocabularyBankManager, getDefaultVocabularyManager } from './vocabulary-bank-manager';
export { SpecialRulesEngine, createRulesEngine } from './special-rules-engine';
export { ContradictionHandler, createContradictionHandler } from './contradiction-handler';

// ============ 算法导出 ============
export { ALGORITHMS, recommendAlgorithm } from './algorithms';

// ============ 便捷函数导出 ============
export { encodeText, serializeDNA } from './encoder';
export { generateFromDNA } from './decoder';
export { compareTexts, generateComparisonReport } from './analyzer';
export { parseDNAString, serializeDNA as dnaToString } from './dna-utils';

// ============ CLI入口 ============
import { Command } from 'commander';
import chalk from 'chalk';
import * as fs from 'fs';
import {
  WenfengEncoder
} from './encoder';
import {
  WenfengDNA,
  GenerationConfig,
  VocabularyBank,
  PRESET_VOCABULARY_BANKS
} from './types';
import { getDefaultVocabularyManager } from './vocabulary-bank-manager';
import { generateFromDNA } from './decoder';
import { generateComparisonReport } from './analyzer';
import { parseDNAString } from './dna-utils';

// CLI主程序
const program = new Command();

program
  .name('wenfeng-dna')
  .description('文风DNA编解码系统 v3.0 - 分析和生成文本风格编码')
  .version('3.0.0');

/**
 * 命令1: analyze - 分析文本文风
 */
program
  .command('analyze')
  .description('分析文本的文风DNA编码')
  .argument('[file]', '文本文件路径')
  .option('-t, --text <text>', '直接输入文本')
  .option('-d, --domain <code>', '指定领域代码')
  .option('-o, --output <file>', '输出报告到文件')
  .option('-j, --json', '输出JSON格式')
  .action(async (file: string | undefined, options: any) => {
    try {
      let text: string;

      if (options.text) {
        text = options.text;
      } else if (file && fs.existsSync(file)) {
        text = fs.readFileSync(file, 'utf-8');
      } else if (file) {
        console.error(chalk.red('错误: 文件不存在'));
        process.exit(1);
      } else {
        console.error(chalk.red('错误: 必须提供文本文件或使用 -t 参数'));
        process.exit(1);
      }

      const manager = getDefaultVocabularyManager();
      let vocabularyBank: VocabularyBank | undefined;

      if (options.domain) {
        vocabularyBank = manager.getBank(options.domain);
      }

      console.log(chalk.blue('🔍 正在分析文风DNA...'));
      const encoder = new WenfengEncoder(text, vocabularyBank);
      const result = encoder.encode();

      if (options.json) {
        const output = JSON.stringify(result, null, 2);
        if (options.output) {
          fs.writeFileSync(options.output, output);
          console.log(chalk.green(`✅ JSON报告已保存: ${options.output}`));
        } else {
          console.log(output);
        }
      } else {
        const report = result.report;
        if (options.output) {
          fs.writeFileSync(options.output, report);
          console.log(chalk.green(`✅ 报告已保存: ${options.output}`));
        } else {
          console.log(report);
          showRecommendations(result);
        }
      }

    } catch (error: any) {
      console.error(chalk.red('分析失败:'), error.message);
      process.exit(1);
    }
  });

/**
 * 命令2: generate - 根据DNA生成文本
 */
program
  .command('generate')
  .description('根据DNA编码生成文本')
  .option('-d, --dna <dna>', 'DNA编码字符串')
  .option('-t, --topic <topic>', '生成主题')
  .option('-l, --length <number>', '目标字数', '500')
  .option('-a, --algorithm <id>', '生成算法 (AL01-AL05)', 'AL04')
  .option('--domain <code>', '使用预设词汇库')
  .option('-o, --output <file>', '输出到文件')
  .action(async (options: any) => {
    try {
      if (!options.dna) {
        console.error(chalk.red('错误: 必须使用 -d 参数指定DNA编码'));
        process.exit(1);
      }
      const dna = parseDNAString(options.dna);
      if (!dna) {
        console.error(chalk.red('错误: DNA编码格式不正确'));
        process.exit(1);
      }

      let vocabularyBank: VocabularyBank | undefined;
      if (options.domain && PRESET_VOCABULARY_BANKS[options.domain]) {
        vocabularyBank = PRESET_VOCABULARY_BANKS[options.domain];
      }

      const config: GenerationConfig = {
        dna,
        targetLength: parseInt(options.length),
        topic: options.topic,
        algorithm: options.algorithm,
        vocabularyBank
      };

      console.log(chalk.blue('✨ 正在生成文本...'));
      const result = generateFromDNA(dna, config);

      if (options.output) {
        fs.writeFileSync(options.output, result.content);
        console.log(chalk.green(`✅ 已保存: ${options.output}`));
      } else {
        console.log(chalk.bold('\n=== 生成的文本 ===\n'));
        console.log(result.content);
        console.log(chalk.bold('\n=== 指标 ==='));
        console.log(`字数: ${result.metrics.wordCount}, 句子: ${result.metrics.sentenceCount}`);
        console.log(`平均句长: ${result.metrics.avgSentenceLength}字`);
      }

    } catch (error: any) {
      console.error(chalk.red('生成失败:'), error.message);
      process.exit(1);
    }
  });

/**
 * 命令3: compare - 对比两段文本
 */
program
  .command('compare')
  .description('对比两段文本的文风')
  .argument('<file1>', '第一段文本')
  .argument('<file2>', '第二段文本')
  .option('-o, --output <file>', '输出报告到文件')
  .action((file1: string, file2: string, options: any) => {
    try {
      if (!file1 || !file2) {
        console.error(chalk.red('错误: 必须提供两个文件'));
        process.exit(1);
      }
      if (!fs.existsSync(file1) || !fs.existsSync(file2)) {
        console.error(chalk.red('错误: 文件不存在'));
        process.exit(1);
      }

      const text1 = fs.readFileSync(file1, 'utf-8');
      const text2 = fs.readFileSync(file2, 'utf-8');

      console.log(chalk.blue('🔍 正在对比...'));
      const report = generateComparisonReport(text1, text2);

      if (options.output) {
        fs.writeFileSync(options.output, report);
        console.log(chalk.green(`✅ 报告已保存: ${options.output}`));
      } else {
        console.log(report);
      }

    } catch (error: any) {
      console.error(chalk.red('对比失败:'), error.message);
      process.exit(1);
    }
  });

/**
 * 命令4: list-vocab - 列出词汇库
 */
program
  .command('list-vocab')
  .description('列出可用的预设词汇库')
  .action(() => {
    console.log(chalk.bold('\n=== 预设词汇库 ===\n'));
    for (const bank of Object.values(PRESET_VOCABULARY_BANKS)) {
      console.log(chalk.cyan(`[${bank.domainCode}] ${bank.domainName} (${bank.domainNameZh})`));
    }
    console.log('\n使用 --domain 参数指定词汇库');
  });

/**
 * 辅助函数: 显示推荐
 */
function showRecommendations(result: any): void {
  const { dna } = result;

  console.log(chalk.bold('\n=== 推荐 ==='));

  // 算法推荐
  if (dna.ID.action >= 8) {
    console.log(chalk.green('  算法: AL05 教程式 (行动导向强)'));
  } else if (dna.RH.argument.includes('C')) {
    console.log(chalk.green('  算法: AL03 对比式 (使用对比论证)'));
  } else if (dna.EP.knowledgeSource === 1) {
    console.log(chalk.green('  算法: AL02 见证式 (经验主义)'));
  } else {
    console.log(chalk.green('  算法: AL04 SCQA (默认)'));
  }

  // 矛盾点提示
  if (dna.ID.power >= 7 && dna.ID.emotion >= 7) {
    console.log(chalk.yellow('  ⚠️ 检测到权威-平等矛盾倾向'));
  }
}

// 仅当直接执行文件时运行CLI
if (require.main === module) {
  program.parse();
}
