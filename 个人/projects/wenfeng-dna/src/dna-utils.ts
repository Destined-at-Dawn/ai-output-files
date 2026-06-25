/**
 * DNA编解码工具函数
 */

import { WenfengDNA } from './types';

/**
 * 解析DNA字符串为DNA对象
 */
export function parseDNAString(dnaStr: string): WenfengDNA | null {
  try {
    const dna: any = {};

    // 解析PH
    const phMatch = dnaStr.match(/PH(\d{2})([1-6])([1-5])/);
    if (phMatch) {
      dna.PH = {
        avgSentenceLength: parseInt(phMatch[1]),
        ontologyType: parseInt(phMatch[2]) as any,
        timeView: parseInt(phMatch[3]) as any
      };
    }

    // 解析EP
    const epMatch = dnaStr.match(/EP([1-5])([1-5])([1-4])/);
    if (epMatch) {
      dna.EP = {
        knowledgeSource: parseInt(epMatch[1]) as any,
        verificationMethod: parseInt(epMatch[2]) as any,
        truthView: parseInt(epMatch[3]) as any
      };
    }

    // 解析ID (7位数字)
    const idMatch = dnaStr.match(/ID(\d{7})/);
    if (idMatch) {
      const idNum = idMatch[1];
      dna.ID = {
        power: parseInt(idNum[0]),
        elite: parseInt(idNum[1]),
        knowledge: parseInt(idNum[2]),
        technology: parseInt(idNum[3]),
        action: parseInt(idNum[4]),
        class: parseInt(idNum[5]),
        emotion: parseInt(idNum[6])
      };
    }

    // 解析RH
    const rhMatch = dnaStr.match(/RH([A-Z]{3})([A-Z]{3})([1359])/);
    if (rhMatch) {
      dna.RH = {
        argument: rhMatch[1],
        figure: rhMatch[2],
        rhythm: parseInt(rhMatch[3]) as any
      };
    }

    // 解析SY
    const syMatch = dnaStr.match(/SY(\d{2})(\d{2})([135])([A-Z]{2})(\d{3})(\d{3})(\d{3})/);
    if (syMatch) {
      dna.SY = {
        avgSentenceLength: parseInt(syMatch[1]),
        complexity: parseInt(syMatch[2]),
        variation: parseInt(syMatch[3]) as any,
        punctuation: syMatch[4],
        shortRatio: parseInt(syMatch[5]),
        mediumRatio: parseInt(syMatch[6]),
        longRatio: parseInt(syMatch[7])
      };
    }

    // 解析DN - 格式: DN vv tt oo ww DD depth
    // vv: 词汇专业度(2位)
    // tt: 术语占比(2位)
    // oo: 口语占比(2位)
    // ww: 文言占比(2位)
    // DD: 领域码(2字符)
    // depth: 深度(1位)
    const dnMatch = dnaStr.match(/DN(\d{2})(\d{2})(\d{2})(\d{2})([A-Z0-9]{2})([1-9])/);
    if (dnMatch) {
      dna.DN = {
        vocabularyLevel: parseInt(dnMatch[1]),
        termRatio: parseInt(dnMatch[2]),
        colloquialRatio: parseInt(dnMatch[3]),
        classicalRatio: parseInt(dnMatch[4]),
        domainCode: dnMatch[5],
        depth: parseInt(dnMatch[6])
      };
    }

    // 解析RD
    const rdMatch = dnaStr.match(/RD([1-9])([1-9])([1-9])([1-9])([1-9])([1-9])/);
    if (rdMatch) {
      dna.RD = {
        reality: parseInt(rdMatch[1]),
        power: parseInt(rdMatch[2]),
        emotion: parseInt(rdMatch[3]),
        logic: parseInt(rdMatch[4]),
        concrete: parseInt(rdMatch[5]),
        action: parseInt(rdMatch[6])
      };
    }

    // 验证是否解析成功
    if (!dna.PH || !dna.EP || !dna.ID || !dna.RH || !dna.SY || !dna.DN || !dna.RD) {
      return null;
    }

    return dna as WenfengDNA;
  } catch {
    return null;
  }
}

/**
 * 将DNA对象序列化为字符串
 */
export function serializeDNA(dna: WenfengDNA): string {
  const { PH, EP, ID, RH, SY, DN, RD } = dna;

  const phPart = `PH${pad2(PH.avgSentenceLength)}${PH.ontologyType}${PH.timeView}`;
  const epPart = `EP${EP.knowledgeSource}${EP.verificationMethod}${EP.truthView}`;
  const idPart = `ID${ID.power}${ID.elite}${ID.knowledge}${ID.technology}${ID.action}${ID.class}${ID.emotion}`;
  const rhPart = `RH${RH.argument}${RH.figure}${RH.rhythm}`;
  const syPart = `SY${pad2(SY.avgSentenceLength)}${pad2(SY.complexity)}${SY.variation}${SY.punctuation}${pad3(SY.shortRatio)}${pad3(SY.mediumRatio)}${pad3(SY.longRatio)}`;
  const dnPart = `DN${DN.vocabularyLevel}${DN.termRatio}${DN.colloquialRatio}${DN.classicalRatio}${DN.domainCode}${DN.depth}`;
  const rdPart = `RD${RD.reality}${RD.power}${RD.emotion}${RD.logic}${RD.concrete}${RD.action}`;

  return phPart + epPart + idPart + rhPart + syPart + dnPart + rdPart;
}

function pad2(n: number): string {
  return n.toString().padStart(2, '0');
}

function pad3(n: number): string {
  return n.toString().padStart(3, '0');
}
