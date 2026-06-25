#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逐字稿清洗与道法术器拆解脚本（专业版 + 科学理论识别）
功能：
1. 识别发言人并分段
2. 修正AI术语和商业用语
3. 过滤语气词和冗余表达
4. 识别科学理论（心理学、经济学、脑科学等）
5. 生成专业道法术器结构化输出
"""

import re
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class SpeakerSegment:
    """发言人段落"""
    speaker: str
    content: str
    timestamp: str = ""

@dataclass
class TheoryMatch:
    """理论匹配结果"""
    theory_name: str
    theory_english: str
    matched_text: str
    theory_desc: str

@dataclass
class CleanedTranscript:
    """清洗后的逐字稿"""
    title: str
    speakers: List[str]
    segments: List[SpeakerSegment]
    topics: List[str]
    summary: str
    key_insights: List[str]
    golden_quotes: List[str]
    speaker_info: str = ""
    event_name: str = ""
    date: str = ""
    theories: List[TheoryMatch] = None  # 识别到的科学理论

    def __post_init__(self):
        if self.theories is None:
            self.theories = []


class TranscriptCleaner:
    """逐字稿清洗器（专业版 + 科学理论识别）"""

    # AI术语词典（常见错误 -> 正确写法）
    # 注意：短词（<=2字符的英文）使用 WORD_BOUNDARY_TERMS 单独处理，避免误替换
    AI_TERMS = {
        # 模型与技术
        'chatgpt': 'ChatGPT',
        'gpt-4o': 'GPT-4o',
        'gpt-4': 'GPT-4',
        'gpt-3.5': 'GPT-3.5',
        'gpt-3': 'GPT-3',
        'gpt4o': 'GPT-4o',
        'gpt4': 'GPT-4',
        'gpt3': 'GPT-3',
        'claude': 'Claude',
        'claude opus': 'Claude Opus',
        'claude sonnet': 'Claude Sonnet',
        'claude haiku': 'Claude Haiku',
        'gemini': 'Gemini',
        'gemini pro': 'Gemini Pro',
        'llama': 'Llama',
        'llama3': 'Llama 3',
        'qwen': 'Qwen',
        'glm-4': 'GLM-4',
        'glm4': 'GLM-4',
        'grok': 'Grok',
        'sora': 'Sora',
        'openai o1': 'OpenAI o1',
        'openai o3': 'OpenAI o3',
        'token': 'Token',
        'prompt': 'Prompt',
        'embedding': 'Embedding',
        'fine-tuning': 'Fine-tuning',
        'finetuning': 'Fine-tuning',
        'stable diffusion': 'Stable Diffusion',
        'langchain': 'LangChain',
        'langgraph': 'LangGraph',
        'huggingface': 'Hugging Face',
        'openai': 'OpenAI',
        'anthropic': 'Anthropic',
        'midjourney': 'Midjourney',
        'coze': 'Coze',
        'dify': 'Dify',
        'fastgpt': 'FastGPT',
        'maxkb': 'MaxKB',
        'deepseek': 'DeepSeek',
        'kimi': 'Kimi',
        'copilot': 'Copilot',
        'codex': 'Codex',
        'cursor': 'Cursor',
        'windsurf': 'Windsurf',
        'lovable': 'Lovable',
        'replit': 'Replit',
        'bolt.new': 'Bolt.new',
        'vercel v0': 'Vercel v0',
        'claude code': 'Claude Code',

        # 技术概念（长词优先）
        'context engineering': 'Context Engineering',
        'vibe coding': 'Vibe Coding',
        'aigc': 'AIGC',
        'agent': 'Agent',

        # 商业用语
        'saas': 'SaaS',
        'paas': 'PaaS',
        'iaas': 'IaaS',
        'b2b': 'B2B',
        'b2c': 'B2C',
        'c2c': 'C2C',
        'arpu': 'ARPU',

        # 平台产品
        'twitter': 'Twitter/X',
        'github': 'GitHub',
        'youtube': 'YouTube',
        'facebook': 'Facebook',
        'instagram': 'Instagram',
        'tiktok': 'TikTok',
        'bilibili': 'Bilibili',
        'xiaohongshu': '小红书',

        # 语音识别错误
        '沙北镇': '沙盒',
        '沙北': '沙盒',
        '蜂群': '封装',
        '窗作者': '创作者',
        '窗作期': '创作期',
        '油稿': 'YouTube',
        '油吐': 'YouTube',
        '油兔': 'YouTube',
        '油土鳖': 'YouTube',
        '电频': '视频',
        '房量': '流量',
        '房板': '仿版',
        '公钱': '播放',
        '动站': '爆款',
        '高低cp': '高客单价',
        'c单': 'C端',
        '生材': '生财',
        '生台': '生财',
    }

    # 短词术语需要词边界匹配，避免误替换中文拼音或嵌入词
    # 格式: {pattern: replacement} — pattern 用 \b 包裹
    WORD_BOUNDARY_TERMS = {
        r'\bai\b': 'AI',
        r'\bllm\b': 'LLM',
        r'\bagi\b': 'AGI',
        r'\brag\b': 'RAG',
        r'\bapi\b': 'API',
        r'\bnlp\b': 'NLP',
        r'\bcv\b': 'CV',
        r'\bgpt\b': 'GPT',
        r'\bmcp\b': 'MCP',
        r'\bsd\b': 'SD',
        r'\bmvp\b': 'MVP',
        r'\bpmf\b': 'PMF',
        r'\broi\b': 'ROI',
        r'\bcac\b': 'CAC',
        r'\bltv\b': 'LTV',
        r'\bdau\b': 'DAU',
        r'\bmau\b': 'MAU',
        r'\bugc\b': 'UGC',
        r'\bpgc\b': 'PGC',
        r'\bogc\b': 'OGC',
        r'\bkoc\b': 'KOC',
        r'\bkol\b': 'KOL',
        r'\bprd\b': 'PRD',
        r'\bmrd\b': 'MRD',
        r'\bbrd\b': 'BRD',
        r'\bui\b': 'UI',
        r'\bux\b': 'UX',
        r'\bseo\b': 'SEO',
        r'\bsem\b': 'SEM',
        r'\bgeo\b': 'GEO',
        r'\bcps\b': 'CPS',
        r'\bcpm\b': 'CPM',
        r'\bcpc\b': 'CPC',
        r'\bcpa\b': 'CPA',
        r'\bipo\b': 'IPO',
        r'\bads\b': 'Ads',
    }

    # 语气词和冗余表达（分级处理）
    # 强语气词：总是删除
    STRONG_FILLERS = [
        '对吧？', '是吧？', '哦', '嗯', '呃',
        '好吧？', '好吧。', '好吧',
        '对不对', '是不是', '可以吗',
    ]
    # 弱语气词：只在句首或独立出现时删除
    WEAK_FILLERS = [
        '那个', '这个', '就是', '然后', '所以',
        '我觉得', '我认为', '我觉得就', '我觉得很',
        '我问一下', '我问大家', '能不能', '可不可以',
        '大家能不能', '大家可不可以', '大家看一下',
    ]
    # 纯语气词（单字，只独立出现时删除）
    SINGLE_FILLERS = ['啊']

    # 科学理论识别词典
    SCIENCE_THEORIES = {
        # 心理学
        '荷塘效应': {
            'english': 'Lotus Effect',
            'desc': '指数增长的滞后性：荷叶每天翻倍，第30天铺满，第29天才50%',
            'keywords': ['荷塘', '荷叶', '翻倍', '铺满', '第29天', '第30天', '滞后', '指数增长', '最后几天']
        },
        '羊群效应': {
            'english': 'Herd Behavior',
            'desc': '个体盲目跟随群体，缺乏独立判断',
            'keywords': ['羊群', '从众', '跟随', '别人都在做', '不敢做第一个', '大家都觉得']
        },
        '集体沉默': {
            'english': 'Group Silence',
            'desc': '群体决策中，有不同意见的人选择沉默，导致群体极化',
            'keywords': ['沉默', '没人说', '不敢说', '群体极化', '虚假共识', '不同意见']
        },
        '幸存者偏差': {
            'english': 'Survivorship Bias',
            'desc': '只看到成功者，忽略失败者，导致错误认知',
            'keywords': ['幸存者', '成功者', '失败者', '被忽略', '错误归因', '只看成功']
        },
        '锚定效应': {
            'english': 'Anchoring Effect',
            'desc': '第一印象或初始信息对后续判断产生强烈影响',
            'keywords': ['锚定', '第一印象', '初始', '难以调整', '先入为主']
        },
        '确认偏误': {
            'english': 'Confirmation Bias',
            'desc': '倾向于寻找支持自己已有观点的信息',
            'keywords': ['确认', '偏误', '只听想听的', '选择性', '回声室', '强化已有']
        },
        '沉没成本谬误': {
            'english': 'Sunk Cost Fallacy',
            'desc': '因为已经投入而继续错误决策',
            'keywords': ['沉没成本', '已经投入', '不能放弃', '不想浪费', '难以放弃']
        },
        '达克效应': {
            'english': 'Dunning-Kruger Effect',
            'desc': '能力低的人高估自己，能力高的人低估自己',
            'keywords': ['达克', '无知者无畏', '专家谨慎', '认知盲区', '不知道自己不知道']
        },
        '损失厌恶': {
            'english': 'Loss Aversion',
            'desc': '失去的痛苦大于获得的快乐',
            'keywords': ['损失厌恶', '害怕失去', '亏损', '痛苦', '保守']
        },
        '峰终定律': {
            'english': 'Peak-End Rule',
            'desc': '对体验的记忆主要取决于高峰和结束时的感受',
            'keywords': ['峰终', '高峰', '结尾', '记忆', '印象']
        },
        '稀缺原理': {
            'english': 'Scarcity Principle',
            'desc': '稀缺的东西更有价值',
            'keywords': ['稀缺', '有限', '限时', '限量', '紧迫感', '不多']
        },
        '社会认同': {
            'english': 'Social Proof',
            'desc': '看到别人做，自己也会做',
            'keywords': ['社会认同', '别人做', '从众', '跟随', '大家都在']
        },
        '权威偏误': {
            'english': 'Authority Bias',
            'desc': '过度信任权威人物的判断',
            'keywords': ['权威', '专家', '盲从', '质疑不足', '相信权威']
        },
        '旁观者效应': {
            'english': 'Bystander Effect',
            'desc': '旁观者越多，个体越不会出手帮助',
            'keywords': ['旁观者', '人越多', '不作为', '等待别人', '责任分散']
        },
        '登门槛效应': {
            'english': 'Foot-in-the-Door',
            'desc': '先提出小要求，再提出大要求，更容易被接受',
            'keywords': ['登门槛', '渐进式', '小要求', '一步一步', '先答应小的']
        },
        '互惠原理': {
            'english': 'Reciprocity',
            'desc': '给别人东西，他们会回报',
            'keywords': ['互惠', '回报', '人情', '交换', '你给我']
        },
        '承诺一致性': {
            'english': 'Commitment & Consistency',
            'desc': '公开承诺后会保持一致',
            'keywords': ['承诺', '一致性', '公开', '保持一致', '自我监控']
        },
        '心流状态': {
            'english': 'Flow',
            'desc': '完全沉浸于活动中的心理状态',
            'keywords': ['心流', '完全沉浸', '忘记时间', '专注', '进入状态', '最佳体验']
        },
        '延迟满足': {
            'english': 'Delayed Gratification',
            'desc': '放弃即时满足，追求长期更大的回报',
            'keywords': ['延迟满足', '即时满足', '长期', '自控', '忍耐']
        },
        '自我效能感': {
            'english': 'Self-Efficacy',
            'desc': '对自己完成任务能力的信念',
            'keywords': ['自我效能', '能力信念', '信心', '相信自己']
        },
        '成长型思维': {
            'english': 'Growth Mindset',
            'desc': '能力可以通过努力发展，而非固定',
            'keywords': ['成长型', '能力发展', '努力', '学习', '可改变']
        },
        '固定型思维': {
            'english': 'Fixed Mindset',
            'desc': '能力是固定的，无法改变',
            'keywords': ['固定型', '能力固定', '天赋', '害怕失败']
        },
        '元认知': {
            'english': 'Metacognition',
            'desc': '对自己认知过程的认识和调控',
            'keywords': ['元认知', '思考思考', '自我监控', '认知调节']
        },
        '认知失调': {
            'english': 'Cognitive Dissonance',
            'desc': '行为与信念冲突时的心理不适',
            'keywords': ['认知失调', '冲突', '不适', '不一致']
        },
        '破窗理论': {
            'english': 'Broken Windows Theory',
            'desc': '小问题不解决会导致大问题',
            'keywords': ['破窗', '小问题', '大问题', '环境效应', '蔓延']
        },

        # 经济学/金融
        '帕累托法则': {
            'english': 'Pareto Principle',
            'desc': '80%的结果来自20%的原因',
            'keywords': ['帕累托', '80/20', '二八', '关键少数', '不平等分布']
        },
        '机会成本': {
            'english': 'Opportunity Cost',
            'desc': '选择一个选项时放弃的其他选项的价值',
            'keywords': ['机会成本', '放弃', '选择的代价', '其他选项']
        },
        '边际效用递减': {
            'english': 'Diminishing Marginal Utility',
            'desc': '每增加一单位消费，效用递减',
            'keywords': ['边际效用', '递减', '越多越不满足', '第一个最香']
        },
        '复利效应': {
            'english': 'Compound Interest',
            'desc': '利息产生利息的指数增长',
            'keywords': ['复利', '时间', '指数增长', '积累', '滚雪球']
        },
        '规模经济': {
            'english': 'Economies of Scale',
            'desc': '产量增加，单位成本下降',
            'keywords': ['规模经济', '大规模', '成本下降', '效率']
        },
        '网络效应': {
            'english': 'Network Effect',
            'desc': '用户越多，产品价值越高',
            'keywords': ['网络效应', '用户越多', '价值越高', '赢家通吃', '越大越强']
        },
        '长尾理论': {
            'english': 'Long Tail',
            'desc': '少量冷门产品合计可超越热门产品',
            'keywords': ['长尾', '冷门', '个性化', '小众']
        },

        # 管理学/商业
        '飞轮效应': {
            'english': 'Flywheel Effect',
            'desc': '持续努力逐渐加速，最终形成动力循环',
            'keywords': ['飞轮', '持续', '加速', '循环', '越来越好']
        },
        '第一性原理': {
            'english': 'First Principles',
            'desc': '从最基本的事实出发，而非类比推理',
            'keywords': ['第一性原理', '基本事实', '本质', '去类比', '是什么就是什么']
        },
        '逆向思维': {
            'english': 'Inversion',
            'desc': '从反面思考问题',
            'keywords': ['逆向', '反向', '倒推', '避免错误']
        },
        '最小可行产品': {
            'english': 'MVP',
            'desc': '用最小成本验证市场',
            'keywords': ['MVP', '最小可行', '验证', '快速迭代', '不要完美']
        },
        '精益创业': {
            'english': 'Lean Startup',
            'desc': '快速验证、快速迭代、降低浪费',
            'keywords': ['精益', '快速验证', '迭代', '降低浪费']
        },
        '蓝海战略': {
            'english': 'Blue Ocean Strategy',
            'desc': '开创无人竞争的新市场',
            'keywords': ['蓝海', '无竞争', '新市场', '价值创新', '避开竞争']
        },
        '产品市场契合': {
            'english': 'PMF',
            'desc': '产品与市场需求的匹配程度',
            'keywords': ['PMF', '产品市场契合', '匹配', '需求', '定位']
        },

        # 脑科学/认知
        '系统1 vs 系统2': {
            'english': 'System 1 vs System 2',
            'desc': '系统1快速直觉，系统2缓慢理性',
            'keywords': ['系统1', '系统2', '快速', '缓慢', '直觉', '理性', '双系统']
        },
        '认知负荷': {
            'english': 'Cognitive Load',
            'desc': '工作记忆容量有限，过度负荷影响学习',
            'keywords': ['认知负荷', '工作记忆', '容量', '信息过载']
        },

        # 社会学/群体行为
        '邓巴数': {
            'english': "Dunbar's Number",
            'desc': '人类能维持的稳定社交关系约为150人',
            'keywords': ['邓巴数', '150人', '社交关系', '认知限制']
        },
        '弱连接理论': {
            'english': 'Weak Ties',
            'desc': '弱连接比强连接更能带来新信息',
            'keywords': ['弱连接', '新信息', '新机会', '强关系同质化']
        },

        # 策略/博弈
        '囚徒困境': {
            'english': "Prisoner's Dilemma",
            'desc': '个人理性导致集体非理性',
            'keywords': ['囚徒困境', '合作', '背叛', '困境', '理性']
        },
        '纳什均衡': {
            'english': 'Nash Equilibrium',
            'desc': '没有人有动力改变策略的状态',
            'keywords': ['纳什均衡', '稳定', '策略', '均衡']
        },
        '零和博弈': {
            'english': 'Zero-Sum Game',
            'desc': '一方收益等于另一方损失',
            'keywords': ['零和', '输赢', '竞争', '一方收益']
        },
        '正和博弈': {
            'english': 'Positive-Sum Game',
            'desc': '双方都能获益',
            'keywords': ['正和', '双赢', '合作', '增值']
        },
        '先发优势': {
            'english': 'First Mover Advantage',
            'desc': '先进入市场的优势',
            'keywords': ['先发', '优势', '占据心智', '第一个']
        },

        # 其他经典理论
        '奥卡姆剃刀': {
            'english': "Occam's Razor",
            'desc': '简单的解释往往更好',
            'keywords': ['奥卡姆剃刀', '简单', '不要复杂化', '剃刀', '经济']
        },
        '彼得原理': {
            'english': 'Peter Principle',
            'desc': '人会被提升到他不胜任的位置',
            'keywords': ['彼得原理', '提升', '不胜任', '组织', '能力边界']
        },
        '墨菲定律': {
            'english': "Murphy's Law",
            'desc': '凡事可能出错，就一定会出错',
            'keywords': ['墨菲定律', '出错', '悲观', '准备充分']
        },
        '帕金森定律': {
            'english': "Parkinson's Law",
            'desc': '工作会自动膨胀，占满所有可用时间',
            'keywords': ['帕金森', '工作膨胀', '占满时间', '官僚', '效率']
        },
        '蝴蝶效应': {
            'english': 'Butterfly Effect',
            'desc': '初始条件的微小变化导致巨大差异',
            'keywords': ['蝴蝶效应', '微小变化', '巨大差异', '初始条件', '敏感']
        },
        '黑天鹅事件': {
            'english': 'Black Swan',
            'desc': '极端罕见但有重大影响的事件',
            'keywords': ['黑天鹅', '罕见', '重大影响', '不可预测', '极端']
        },
        '灰犀牛事件': {
            'english': 'Grey Rhino',
            'desc': '明显存在但被忽视的威胁',
            'keywords': ['灰犀牛', '明显', '忽视', '高风险', '可以预防']
        },
    }

    # 主要发言人标识（用于金句、洞察、道层提取）
    MAIN_SPEAKERS = ['嘉宾', '分享者', '演讲者', '讲者', '老师']
    # 非主要发言人（排除）
    EXCLUDED_SPEAKERS = ['听众', '观众', '系统音', '系统', '主持人']

    def _is_main_speaker(self, speaker: str) -> bool:
        """判断是否为主要发言人"""
        for main in self.MAIN_SPEAKERS:
            if main in speaker:
                return True
        for excluded in self.EXCLUDED_SPEAKERS:
            if excluded in speaker:
                return False
        # 未知发言人，如果只有一个发言人则视为主要发言人
        return True

    def _get_main_speaker_text(self, segments: List[SpeakerSegment]) -> str:
        """提取所有主要发言人的文本"""
        return ' '.join([s.content for s in segments if self._is_main_speaker(s.speaker)])
    SPEAKER_PATTERNS = [
        r'^(.*?)[：:](.+)$',  # 发言人：内容
        r'^(.*?)[\s]*[\n\r](.+)$',  # 发言人\n内容
    ]

    def __init__(self):
        self.compiled_patterns = []
        for pattern in self.SPEAKER_PATTERNS:
            self.compiled_patterns.append(re.compile(pattern, re.MULTILINE | re.DOTALL))

    def identify_speakers(self, text: str) -> List[SpeakerSegment]:
        """识别发言人并分段"""
        segments = []
        lines = text.strip().split('\n')

        current_speaker = "分享者"
        current_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 检查是否是发言人标记
            speaker_found = False

            # 检查常见发言人标记
            speaker_markers = ['系统音：', '主持人：', '嘉宾：', '分享者：', '演讲者：']
            for marker in speaker_markers:
                if line.startswith(marker):
                    # 保存之前的段落
                    if current_content:
                        segments.append(SpeakerSegment(
                            speaker=current_speaker,
                            content=' '.join(current_content)
                        ))

                    # 开始新段落
                    current_speaker = marker.replace('：', '')
                    remaining = line[len(marker):].strip()
                    if remaining:
                        current_content = [remaining]
                    else:
                        current_content = []
                    speaker_found = True
                    break

            if not speaker_found:
                # 尝试正则匹配
                for pattern in self.compiled_patterns:
                    match = pattern.match(line)
                    if match:
                        # 保存之前的段落
                        if current_content:
                            segments.append(SpeakerSegment(
                                speaker=current_speaker,
                                content=' '.join(current_content)
                            ))

                        # 开始新段落
                        current_speaker = match.group(1).strip()
                        current_content = [match.group(2).strip()]
                        speaker_found = True
                        break

            if not speaker_found:
                current_content.append(line)

        # 保存最后一个段落
        if current_content:
            segments.append(SpeakerSegment(
                speaker=current_speaker,
                content=' '.join(current_content)
            ))

        return segments

    def correct_terms(self, text: str) -> str:
        """修正AI术语和商业用语"""
        corrected = text

        # 1. 先处理长词（按长度降序排序，避免短词替换影响长词）
        sorted_terms = sorted(self.AI_TERMS.items(), key=lambda x: len(x[0]), reverse=True)

        for wrong, correct in sorted_terms:
            pattern = re.compile(re.escape(wrong), re.IGNORECASE)
            corrected = pattern.sub(correct, corrected)

        # 2. 再处理短词（使用词边界匹配，避免误替换中文拼音）
        for pattern_str, correct in self.WORD_BOUNDARY_TERMS.items():
            pattern = re.compile(pattern_str, re.IGNORECASE)
            corrected = pattern.sub(correct, corrected)

        return corrected

    def remove_fillers(self, text: str) -> str:
        """去除语气词和冗余表达（分级处理）"""
        cleaned = text

        # 1. 强语气词：直接删除
        for filler in self.STRONG_FILLERS:
            pattern = r'\s*' + re.escape(filler) + r'[\s，。！？]*'
            cleaned = re.sub(pattern, ' ', cleaned)

        # 2. 弱语气词：只在句首或紧跟标点后删除
        for filler in self.WEAK_FILLERS:
            # 句首
            pattern = r'^' + re.escape(filler) + r'[\s，、]*'
            cleaned = re.sub(pattern, '', cleaned)
            # 标点后
            pattern = r'([。！？，])\s*' + re.escape(filler) + r'[\s，、]*'
            cleaned = re.sub(pattern, r'\1', cleaned)

        # 3. 单字语气词：只独立出现时删除（前后有标点或空格）
        for filler in self.SINGLE_FILLERS:
            pattern = r'(?<=[。！？，\s])' + re.escape(filler) + r'(?=[。！？，\s])'
            cleaned = re.sub(pattern, '', cleaned)

        # 清理多余空格
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()

        # 去除重复的标点
        cleaned = re.sub(r'[。，！？]{2,}', '。', cleaned)

        return cleaned

    def merge_same_speaker(self, segments: List[SpeakerSegment]) -> List[SpeakerSegment]:
        """合并同一发言人的连续段落"""
        if not segments:
            return []

        merged = [segments[0]]

        for segment in segments[1:]:
            if segment.speaker == merged[-1].speaker:
                merged[-1].content += ' ' + segment.content
            else:
                merged.append(segment)

        return merged

    def extract_topics(self, segments: List[SpeakerSegment]) -> List[str]:
        """提取会议主题"""
        all_text = ' '.join([s.content for s in segments])

        # 关键词提取
        topic_keywords = [
            'AI', '人工智能', '大模型', 'Agent', '自动化',
            '方法论', '框架', '策略', '执行', '工具', '工作流',
            '产品', '运营', '增长', '变现', '流量',
            '道', '法', '术', '器', '复盘', '总结',
            '编程', '代码', '开发', '创业', '副业',
            '短视频', '内容', '矩阵', '出海',
        ]

        topics = []
        for keyword in topic_keywords:
            if keyword in all_text:
                topics.append(keyword)

        return list(set(topics))[:8]

    def extract_golden_quotes(self, segments: List[SpeakerSegment]) -> List[str]:
        """提取金句（只从主要发言人）"""
        quotes = []
        main_speaker_text = self._get_main_speaker_text(segments)

        if not main_speaker_text:
            return []

        # 寻找包含特定关键词的句子
        quote_patterns = [
            r'[^。！？]*(?:不是.*?而是)[^。！？]*[。！？]',
            r'[^。！？]*(?:本质上|本质是|本质不是)[^。！？]*[。！？]',
            r'[^。！？]*(?:核心是|核心在于)[^。！？]*[。！？]',
            r'[^。！？]*(?:关键是|关键在于)[^。！？]*[。！？]',
            r'[^。！？]*(?:终局是|终局在于)[^。！？]*[。！？]',
            r'[^。！？]*(?:底层逻辑|底层是)[^。！？]*[。！？]',
            r'[^。！？]*(?:真正的)[^。！？]*[。！？]',
        ]

        for pattern in quote_patterns:
            matches = re.findall(pattern, main_speaker_text)
            # 过滤掉太短（<10字）或太长（>80字）的句子
            for m in matches:
                m = m.strip()
                if 10 <= len(m) <= 80 and m not in quotes:
                    quotes.append(m)
                    if len(quotes) >= 15:
                        break
            if len(quotes) >= 15:
                break

        return quotes

    def extract_key_insights(self, segments: List[SpeakerSegment]) -> List[str]:
        """提取核心洞察（只从主要发言人）"""
        insights = []
        main_speaker_text = self._get_main_speaker_text(segments)

        if not main_speaker_text:
            return []

        # 寻找包含核心观点的句子
        insight_patterns = [
            r'[^。！？]*(?:核心是|核心在于)[^。！？]*[。！？]',
            r'[^。！？]*(?:本质是|本质不是)[^。！？]*[。！？]',
            r'[^。！？]*(?:关键是|关键在于)[^。！？]*[。！？]',
            r'[^。！？]*(?:底层逻辑)[^。！？]*[。！？]',
            r'[^。！？]*(?:最大的变化|最重要的)[^。！？]*[。！？]',
            r'[^。！？]*(?:不是.*?而是)[^。！？]*[。！？]',
        ]

        for pattern in insight_patterns:
            matches = re.findall(pattern, main_speaker_text)
            for m in matches:
                m = m.strip()
                # 排除问句
                if m.endswith('？') or m.endswith('?'):
                    continue
                if 10 <= len(m) <= 100 and m not in insights:
                    insights.append(m)
                    break

        return insights[:5]

    def identify_theories(self, text: str) -> List[TheoryMatch]:
        """识别文本中的科学理论"""
        theories = []

        for theory_name, theory_info in self.SCIENCE_THEORIES.items():
            # 检查是否包含关键词
            matched_keywords = []
            for keyword in theory_info['keywords']:
                if keyword in text:
                    matched_keywords.append(keyword)

            # 如果匹配到2个以上关键词，认为匹配成功
            if len(matched_keywords) >= 2:
                # 找到匹配的文本片段（去重）
                matched_sentences = set()
                for keyword in matched_keywords:
                    # 找到包含关键词的句子
                    pattern = rf'[^。！？]*{re.escape(keyword)}[^。！？]*[。！？]'
                    matches = re.findall(pattern, text)
                    for match in matches:
                        matched_sentences.add(match.strip())

                matched_text = ' '.join(sorted(matched_sentences)[:3])  # 最多取3个不同的句子

                theories.append(TheoryMatch(
                    theory_name=theory_name,
                    theory_english=theory_info['english'],
                    matched_text=matched_text.strip(),
                    theory_desc=theory_info['desc']
                ))

        return theories

    def clean(self, text: str, title: str = "会议纪要",
              speaker_info: str = "",
              event_name: str = "",
              date: str = "") -> CleanedTranscript:
        """主清洗函数"""
        # 1. 识别发言人
        segments = self.identify_speakers(text)

        # 2. 合并同一发言人的连续段落
        segments = self.merge_same_speaker(segments)

        # 3. 修正术语并去除语气词
        cleaned_segments = []
        for segment in segments:
            content = segment.content
            content = self.correct_terms(content)
            content = self.remove_fillers(content)

            if content.strip():  # 只保留非空内容
                cleaned_segments.append(SpeakerSegment(
                    speaker=segment.speaker,
                    content=content
                ))

        # 4. 提取主题
        topics = self.extract_topics(cleaned_segments)

        # 5. 提取发言人列表
        speakers = list(set([s.speaker for s in cleaned_segments]))

        # 6. 生成摘要
        summary_text = ' '.join([s.content for s in cleaned_segments[:3]])
        summary = summary_text[:300] + '...' if len(summary_text) > 300 else summary_text

        # 7. 提取金句和洞察
        golden_quotes = self.extract_golden_quotes(cleaned_segments)
        key_insights = self.extract_key_insights(cleaned_segments)

        # 8. 识别科学理论
        all_text = ' '.join([s.content for s in cleaned_segments])
        theories = self.identify_theories(all_text)

        return CleanedTranscript(
            title=title,
            speakers=speakers,
            segments=cleaned_segments,
            topics=topics,
            summary=summary,
            key_insights=key_insights,
            golden_quotes=golden_quotes,
            speaker_info=speaker_info,
            event_name=event_name,
            date=date,
            theories=theories
        )

    def to_daofashuqi(self, cleaned: CleanedTranscript) -> str:
        """生成专业道法术器结构化输出"""
        lines = []

        # 头部信息
        lines.append(f"# {cleaned.title}")
        lines.append("")

        if cleaned.event_name or cleaned.date or cleaned.speaker_info:
            lines.append("> 来源：" + (cleaned.event_name if cleaned.event_name else "现场录音转写"))
            if cleaned.date:
                lines.append(f"> 日期：{cleaned.date}")
            if cleaned.speaker_info:
                lines.append(f"> **身份**：{cleaned.speaker_info}")
            lines.append("")
            lines.append("---")
            lines.append("")

        # 科学理论识别（新增）
        if cleaned.theories:
            lines.append("## 🔬 识别到的科学理论")
            lines.append("")
            for theory in cleaned.theories:
                lines.append(f"### {theory.theory_name}（{theory.theory_english}）")
                lines.append("")
                lines.append(f"**核心内容**：{theory.theory_desc}")
                lines.append("")
                lines.append(f"**匹配文本**：{theory.matched_text}")
                lines.append("")
            lines.append("---")
            lines.append("")

        # 第一部分：值不值得学/做（四维打分）
        lines.append("## 第一部分：值不值得学/做（四维打分）")
        lines.append("")
        lines.append("| 维度      | 短期(1-5) | 长期(1-5) | 说明                                                                                            |")
        lines.append("| ---------- | --------- | --------- | --------------------------------------------------------------------------------------------- |")

        # 根据内容估算四维打分
        all_text = ' '.join([s.content for s in cleaned.segments])

        # 钱维度 — 根据变现相关关键词密度评分
        money_keywords_strong = ['变现', '赚钱', '月入', '年入', '收入', '利润', '营收', 'ROI']
        money_keywords_weak = ['商业', '收益', '付费', '客户', '订单', '销售', '价格', '成本']
        money_strong = sum(1 for k in money_keywords_strong if k in all_text)
        money_weak = sum(1 for k in money_keywords_weak if k in all_text)
        money_short = min(5, 2 + money_strong + (1 if money_weak >= 2 else 0))
        money_long = min(5, money_short + (1 if any(k in all_text for k in ['复利', '长期', '被动收入', '规模']) else 0))
        money_desc = "未提及具体变现路径"
        if money_strong >= 2:
            money_desc = "内容涉及具体变现方法和收入数据"
        elif money_strong >= 1:
            money_desc = "提及变现方向，但缺少具体数据支撑"
        elif money_weak >= 2:
            money_desc = "间接涉及商业相关内容，变现潜力待验证"
        lines.append(f"| **钱**     | {money_short}       | {money_long}       | {money_desc} |")

        # 关系维度 — 根据社交/人脉关键词评分
        relation_keywords = ['人脉', '社群', '圈子', '合作', '链接', '社交', '伙伴', '团队', '交流', '社区']
        relation_count = sum(1 for k in relation_keywords if k in all_text)
        relation_short = min(5, 1 + relation_count)
        relation_long = min(5, relation_short + (1 if any(k in all_text for k in ['长期', '深度', '信任']) else 0))
        if relation_count >= 3:
            relation_desc = "内容强调社群/人脉建设，链接机会丰富"
        elif relation_count >= 1:
            relation_desc = "有一定社交链接价值，但非核心主题"
        else:
            relation_desc = "内容主要聚焦个人能力提升，人脉链接较弱"
        lines.append(f"| **关系**   | {relation_short}    | {relation_long}    | {relation_desc} |")

        # 技能维度 — 根据可操作性评分
        skill_keywords_strong = ['方法', '步骤', '操作', '实操', '教程', '技巧', '工具']
        skill_keywords_weak = ['学习', '能力', '技能', '知识', '框架', '思维', '认知']
        skill_strong = sum(1 for k in skill_keywords_strong if k in all_text)
        skill_weak = sum(1 for k in skill_keywords_weak if k in all_text)
        skill_short = min(5, 2 + skill_strong + (1 if skill_weak >= 3 else 0))
        skill_long = min(5, skill_short + (1 if any(k in all_text for k in ['底层', '通用', '可迁移']) else 0))
        if skill_strong >= 3:
            skill_desc = "提供具体可执行的技能和方法论，实操性强"
        elif skill_strong >= 1:
            skill_desc = "包含方法论框架，需结合实践落地"
        else:
            skill_desc = "偏认知层面，技能获取需自行转化"
        lines.append(f"| **技能**   | {skill_short}       | {skill_long}       | {skill_desc} |")

        # 影响力维度 — 根据个人品牌/传播相关词评分
        influence_keywords = ['IP', '品牌', '影响力', '粉丝', '流量', '传播', '内容', '平台', '曝光', '作品']
        influence_count = sum(1 for k in influence_keywords if k in all_text)
        influence_short = min(5, 1 + influence_count)
        influence_long = min(5, influence_short + (1 if any(k in all_text for k in ['积累', '长期', '复利', '壁垒']) else 0))
        if influence_count >= 3:
            influence_desc = "内容直接涉及个人IP/品牌建设，影响力天花板高"
        elif influence_count >= 1:
            influence_desc = "有一定影响力积累价值，需结合个人实践转化"
        else:
            influence_desc = "内容偏内功修炼，影响力需额外经营"
        lines.append(f"| **影响力** | {influence_short}  | {influence_long}  | {influence_desc} |")

        # 综合判断
        total = money_short + relation_short + skill_short + influence_short
        if total >= 16:
            verdict = "强烈值得学/做"
        elif total >= 12:
            verdict = "值得学/做"
        elif total >= 8:
            verdict = "谨慎考虑"
        else:
            verdict = "不值得学"

        lines.append("")
        lines.append(f"**综合判断：{verdict}**")
        lines.append("")

        # 生成基于内容的判断说明
        strengths = []
        if skill_short >= 4:
            strengths.append("方法论清晰、可操作性强")
        if money_short >= 4:
            strengths.append("变现路径明确")
        if influence_short >= 4:
            strengths.append("有助于个人IP建设")
        if relation_short >= 3:
            strengths.append("社交链接价值较高")
        if strengths:
            strengths_text = "、".join(strengths)
            lines.append(f"核心优势：{strengths_text}。适合想要在该领域深耕的人，建议结合个人实际情况选择性应用。")
        else:
            lines.append("内容有一定信息增量，建议结合个人实际情况判断投入产出比。")
        lines.append("")

        # 第二部分：能学到什么（道法术器拆解）
        lines.append("---")
        lines.append("")
        lines.append("## 第二部分：能学到什么（道法术器拆解）")
        lines.append("")

        # 道（底层认知）— 只从主要发言人提取
        lines.append("### 道（刻进骨子里）")
        lines.append("")

        # 只从主要发言人的文本提取
        main_text = self._get_main_speaker_text(cleaned.segments)

        dao_patterns = [
            r'[^。！？]*(?:本质|底层|根本)[^。！？]*[。！？]',
            r'[^。！？]*(?:不是.*?而是)[^。！？]*[。！？]',
            r'[^。！？]*(?:最大的变化|最重要的)[^。！？]*[。！？]',
            r'[^。！？]*(?:真正的)[^。！？]*[。！？]',
        ]

        dao_quotes = []
        for pattern in dao_patterns:
            matches = re.findall(pattern, main_text)
            for m in matches:
                m = m.strip()
                # 排除问句和太短/太长的句子
                if m.endswith('？') or m.endswith('?'):
                    continue
                if 10 <= len(m) <= 100 and m not in dao_quotes:
                    dao_quotes.append(m)

        for i, quote in enumerate(dao_quotes[:3], 1):
            lines.append(f"**核心认知{i}**")
            lines.append("")
            lines.append(f"> \"{quote}\"")
            lines.append("")

        # 法（方法论框架）— 提取高层框架/模型/原则，从主要发言人
        lines.append("### 法（很少变的方法论）")
        lines.append("")

        # 法：框架性描述（级别体系、原则、模型）
        fa_patterns = [
            r'[^。！？]*(?:L[1-6]是|Level [1-6]|第[一二三四五六七八九十]级|分为\d+[个层级])[^。！？]*[。！？]',
            r'[^。！？]*(?:\d+原则|\d+法则|\d+模型|\d+维|\d+层)[^。！？]*[。！？]',
            r'[^。！？]*(?:框架是|方法论是|公式是|模型是)[^。！？]*[。！？]',
            r'[^。！？]*(?:可以分为|分成|归纳为)[^。！？]*[。！？]',
        ]
        fa_used = set()  # 跟踪已用于"法"的内容，避免在"术"重复
        fa_items = []
        for pattern in fa_patterns:
            matches = re.findall(pattern, main_text)
            for m in matches:
                m = m.strip()
                if 10 <= len(m) <= 150 and m not in fa_used:
                    fa_items.append(m)
                    fa_used.add(m)

        if fa_items:
            for i, item in enumerate(fa_items[:3], 1):
                lines.append(f"**方法论{i}**")
                lines.append("")
                lines.append(item)
                lines.append("")
                lines.append("→ 这是一个可迁移的框架，适用于类似场景")
                lines.append("")
        else:
            lines.append("**核心方法论**")
            lines.append("")
            lines.append("- 根据内容提炼的方法论框架")
            lines.append("- 这是一个可迁移的框架，适用于类似场景")
            lines.append("")

        # 术（具体策略）— 提取具体操作步骤，排除已在"法"出现的内容
        lines.append("### 术（具体策略）")
        lines.append("")

        shu_patterns = [
            r'[^。！？]*(?:第[一二三四五六七八九十]步[，：、])[^。！？]*[。！？]',
            r'[^。！？]*(?:首先|其次|然后|最后)[，：、][^。！？]*[。！？]',
            r'[^。！？]*(?:具体操作|具体做法|怎么做|怎么用)[^。！？]*[。！？]',
        ]
        shu_items = []
        for pattern in shu_patterns:
            matches = re.findall(pattern, main_text)
            for m in matches:
                m = m.strip()
                # 跳过已在"法"中出现的内容
                if m in fa_used:
                    continue
                if 10 <= len(m) <= 150 and m not in shu_items:
                    shu_items.append(m)

        for i, action in enumerate(shu_items[:5], 1):
            lines.append(f"**【策略{i}】**")
            lines.append("")
            lines.append(action)
            lines.append("")

        if not shu_items:
            lines.append("**具体执行**")
            lines.append("")
            lines.append("- 根据内容提炼的可执行步骤")
            lines.append("")

        # 器（工具与资源）— 提取工具并从上下文推断用途
        lines.append("### 器（工具与资源）")
        lines.append("")

        lines.append("| 工具 | 用途 |")
        lines.append("|------|------|")

        # 提取提到的工具，并从上下文获取用途描述
        tool_keywords = {
            'Cursor': 'AI代码编辑器',
            'Codex': 'OpenAI代码生成模型',
            'ChatGPT': 'AI对话与内容生成',
            'Claude': 'Anthropic AI助手',
            'Claude Code': 'AI编程CLI工具',
            'Windsurf': 'AI辅助IDE',
            'Bolt.new': '全栈AI应用生成器',
            'Lovable': 'AI前端原型工具',
            'Midjourney': 'AI图像生成',
            'Stable Diffusion': 'AI图像生成（开源）',
            'Coze': 'AI Bot搭建平台',
            'Dify': 'LLM应用开发平台',
            'FastGPT': '知识库问答平台',
            'LangChain': 'LLM应用开发框架',
            'LangGraph': 'AI Agent编排框架',
            'Python': '编程语言',
            'JavaScript': '编程语言',
            'Notion': '知识管理与协作',
            'Figma': 'UI设计工具',
        }
        found_tools = []
        for tool_name, default_desc in tool_keywords.items():
            if tool_name in all_text:
                found_tools.append((tool_name, default_desc))

        for tool_name, desc in found_tools:
            lines.append(f"| **{tool_name}** | {desc} |")

        lines.append("")

        # 第三部分：我的收获与行动
        lines.append("---")
        lines.append("")
        lines.append("## 第三部分：我的收获与行动")
        lines.append("")

        lines.append("### 优先记住")
        lines.append("")
        for i, insight in enumerate(cleaned.key_insights[:3], 1):
            lines.append(f"{i}. {insight}")
        lines.append("")

        lines.append("### 今天就能做的三件事")
        lines.append("")

        # 从内容提取可执行行动，而非硬编码
        action_candidates = []
        action_extract_patterns = [
            r'[^。！？]*(?:可以[去做试]|建议|应该|马上|立刻|赶紧)[^。！？]*[。！？]',
            r'[^。！？]*(?:第一步|先做|先去|先把)[^。！？]*[。！？]',
        ]
        for pattern in action_extract_patterns:
            matches = re.findall(pattern, main_text)
            for m in matches:
                m = m.strip()
                if 8 <= len(m) <= 60 and m not in action_candidates:
                    action_candidates.append(m)

        if len(action_candidates) >= 3:
            for i, act in enumerate(action_candidates[:3], 1):
                lines.append(f"- [ ] **行动{i}**：{act}")
        elif action_candidates:
            for i, act in enumerate(action_candidates, 1):
                lines.append(f"- [ ] **行动{i}**：{act}")
            # 补充通用行动到3条
            generic_actions = ["整理本次分享的核心认知 - 今天完成", "选择1个方法论在实际场景中试用 - 本周内"]
            for act in generic_actions[:3 - len(action_candidates)]:
                lines.append(f"- [ ] {act}")
        else:
            # 无法提取时，基于内容主题生成
            if cleaned.topics:
                lines.append(f"- [ ] **深入研究**：围绕「{cleaned.topics[0]}」搜集更多案例 - 今天完成")
                lines.append(f"- [ ] **实践验证**：选择1个方法论在实际工作中试用 - 本周内")
                lines.append(f"- [ ] **复盘总结**：记录实践结果并迭代 - 下周完成")
            else:
                lines.append("- [ ] **整理核心观点** - 今天完成")
                lines.append("- [ ] **选择1个方法论试用** - 本周内")
                lines.append("- [ ] **复盘实践结果** - 下周完成")
        lines.append("")

        lines.append("### 关联你已有的")
        lines.append("")
        lines.append("- 将本文内容与你现有的知识体系连接")
        lines.append("- 思考如何将方法论应用到你的实际工作中")
        lines.append("")

        # 金句摘录
        if cleaned.golden_quotes:
            lines.append("---")
            lines.append("")
            lines.append("## 金句摘录")
            lines.append("")
            for quote in cleaned.golden_quotes:
                lines.append(f"> \"{quote}\"")
                lines.append("")

        return '\n'.join(lines)

    def to_simple_markdown(self, cleaned: CleanedTranscript) -> str:
        """转换为简单Markdown格式"""
        lines = []

        lines.append(f"# {cleaned.title}")
        lines.append("")

        # 摘要
        lines.append("## 摘要")
        lines.append(cleaned.summary)
        lines.append("")

        # 发言人
        if len(cleaned.speakers) > 1:
            lines.append("## 发言人")
            for speaker in cleaned.speakers:
                lines.append(f"- {speaker}")
            lines.append("")

        # 主题
        if cleaned.topics:
            lines.append("## 主题")
            for topic in cleaned.topics:
                lines.append(f"- {topic}")
            lines.append("")

        # 详细内容
        lines.append("## 详细内容")
        lines.append("")

        current_speaker = None
        for segment in cleaned.segments:
            if segment.speaker != current_speaker:
                lines.append(f"### {segment.speaker}")
                current_speaker = segment.speaker
            lines.append(segment.content)
            lines.append("")

        # 金句
        if cleaned.golden_quotes:
            lines.append("## 金句摘录")
            lines.append("")
            for quote in cleaned.golden_quotes:
                lines.append(f"> \"{quote}\"")
                lines.append("")

        return '\n'.join(lines)


def main():
    """命令行入口"""
    import sys
    import io

    # 修复Windows控制台编码问题
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    if len(sys.argv) < 2:
        print("用法: python clean_transcript.py <逐字稿文件路径> [标题] [选项]")
        print("选项:")
        print("  --daofashuqi  使用道法术器格式输出（推荐）")
        print("  --simple      使用简单格式输出（默认）")
        print("")
        print("示例:")
        print("  python clean_transcript.py transcript.txt '会议主题'")
        print("  python clean_transcript.py transcript.txt '分享主题' --daofashuqi")
        sys.exit(1)

    file_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "会议纪要"
    use_daofashuqi = '--daofashuqi' in sys.argv

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        cleaner = TranscriptCleaner()
        cleaned = cleaner.clean(text, title)

        if use_daofashuqi:
            markdown = cleaner.to_daofashuqi(cleaned)
        else:
            markdown = cleaner.to_simple_markdown(cleaned)

        # 输出结果
        output_path = file_path.replace('.txt', '_cleaned.md').replace('.md', '_cleaned.md')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"✅ 清洗完成！输出文件: {output_path}")
        print(f"📊 发言人: {', '.join(cleaned.speakers)}")
        print(f"🏷️ 主题: {', '.join(cleaned.topics)}")
        print(f"💡 核心洞察: {len(cleaned.key_insights)} 条")
        print(f"⭐ 金句: {len(cleaned.golden_quotes)} 条")
        print(f"🔬 科学理论: {len(cleaned.theories)} 个")

        if cleaned.theories:
            print(f"\n📚 识别到的理论: {', '.join([t.theory_name for t in cleaned.theories])}")

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
