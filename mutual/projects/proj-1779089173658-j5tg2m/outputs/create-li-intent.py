import os, json

intent_dir = r'C:\Users\13975\.newmax\skills\li-intent'
refs_dir = os.path.join(intent_dir, 'references')
os.makedirs(refs_dir, exist_ok=True)

# SKILL.md
skill_md = """---
name: li-intent
version: 1.0
description: "SOP-driven intent understanding - from keyword matching to intent-to-skill-chain execution"
---

# li-intent - SOP-Driven Intent Understanding Engine

## Theory Table

| ID | Theory | Source | Application |
|----|--------|--------|-------------|
| T1 | Recognition-Primed Decision | Klein 1998 | Experts match patterns not keywords |
| T2 | Schema Theory | Piaget | SOPs are schemas for familiar situations |
| T3 | Bounded Rationality | Simon 1957 | First matching intent is often good enough |
| T4 | Chunking | Miller 1956 | Intent = chunk of keywords + context + history |
| T5 | Metcalfe's Law | Network Theory | Each new SOP makes the network more valuable |
| T6 | Transfer of Learning | Cognitive Psychology | "This is like last time" = pattern transfer |
| T7 | Satisficing vs Maximizing | Schwartz 2004 | Match first good intent, don't exhaust all |
| T8 | Distributed Cognition | Hutchins 1995 | Intent lives in the system not just the message |
| T9 | Ecological Rationality | Gigerenzer | Simple rules in structured environments win |
| T10 | Semantic Memory | Tulving 1972 | Intent = semantic categorization of input |
| T11 | Script Theory | Schank 1977 | SOPs = automatic action sequences |
| T12 | Transfer Appropriate Processing | Morris 1977 | Match intent to best task format |

## Design Philosophy

1. **Intent is pattern not keyword** - "help read WeChat" and "analyze this link" are the same intent.
   DP1: Keyword-only matching misses 60% of intents.
2. **SOP is the intent implementation** - Each SOP maps one intent to a skill chain.
   DP2: Skills implement intent directly without SOP = no standardization.
3. **Historical experience is the first lookup** - Before routing table, check: done this before?
   DP3: Always route from scratch = waste 80% exploration time.
4. **Cross-workspace awareness** - SOP in workspace X is valid reference in workspace Y.
   DP4: SOPs are workspace-bound = 188 SOPs but only 37 per workspace see them.
5. **Three-layer: intent -> SOP -> skill chain** - Never jump from intent to skill directly.
   DP5: Skip SOP layer = no standardization, no feedback loop.
6. **Feedback refines intent mapping** - User correction = intent mismatch = update SOP.
   DP6: Feedback doesn't improve accuracy = repeat same mistakes.
7. **Skill chains not monoliths** - 3 skills in sequence > 1 skill doing everything.
   DP7: One skill per intent = bloated skills that do nothing well.
8. **Confidence-based execution** - High auto, medium announce, low ask.
   DP8: Same behavior regardless of confidence = waste or surprise.

## Pipeline

### Phase 0: Input Classification
1. Scan for structural signals: URL, code block, file path, question
2. Scan for domain signals: hardware, content, research, learning, skill
3. Scan for action signals: read, write, analyze, create, fix, search
4. Output: action + domain + structure + keywords

### Phase 1: Historical Experience Retrieval
1. Check memory/long-term.md - this intent logged before?
2. Check memory/{recent-dates}.md - recent similar tasks?
3. Check conversation context - earlier in this session?
4. Check skill-usage-log.md - skills used for similar intents?
5. Output: historical_intent + historical_skill_chain + outcome

### Phase 2: SOP Matching
1. If historical match with good outcome -> reuse that SOP
2. Otherwise scan workspace SOP index for IF/ELSE pattern match
3. SOP index: IF action=read AND structure=URL -> sop-content-analysis
4. Output: matched_sop + skill_chain + confidence

### Phase 3: Skill Chain Execution
1. Execute skills in SOP-defined order
2. Each skill receives output of previous as input
3. If skill fails -> check SOP fallback -> try alternative
4. If no SOP matches -> fall back to routing table keywords
5. Output: final_result + skills_used

### Phase 4: Feedback and Learning
1. Collect user feedback (explicit or implicit)
2. Positive -> strengthen intent-to-SOP mapping
3. Negative -> log mismatch -> update SOP routing
4. New pattern 3+ times -> promote to permanent SOP
5. Write to skill-usage-log.md

## Intent Pattern Library (Seed)

From 188 SOPs across 5 workspaces:

| Intent | Pattern | SOP | Skill Chain |
|--------|---------|-----|-------------|
| Read article | URL + read/analyze | Content analysis | li-analyze -> li-memory |
| Write content | write/create + platform | Content creation | li-analyze -> li-transcript |
| Research | search/research + topic | Research | li-research -> li-devil |
| Create skill | create + skill | Skill lifecycle | li-bestskill -> li-skillcreate |
| Debug code | error/bug + code | Debug | li-debug -> li-diagnose |
| Hardware | FPGA/Arduino/verilog | Hardware delivery | li-hardware -> li-debug |
| Learning | learn/understand | Learning | li-mindcoach -> li-analyze |
| Maintenance | sync/clean/organize | Maintenance | li-sync -> li-manage |
| Decision | should/choose/how | Decision | li-devil -> li-mindcoach |

## Case Studies

### Case 1: "Help me read this WeChat article"
**Input**: URL + "read" + "WeChat"
**Intent**: action=read, structure=URL, domain=content
**Historical**: memory shows baoyu-url-to-markdown + li-analyze used before
**SOP**: sop-content-analysis -> extract -> analyze (dao-fa-shu-qi) -> remember
**Result**: Structured analysis with cognitive science refs, auto-persisted.

### Case 2: "Write a Xiaohongshu post about FPGA"
**Input**: "write" + "FPGA" + "Xiaohongshu"
**Intent**: action=create, domain=hardware+content, platform=xiaohongshu
**SOP**: sop-content-creation -> audience analysis -> write -> format
**Chain**: li-hardware (domain) -> li-analyze (audience) -> li-transcript (format)
**Result**: Hardware content formatted for social media.

### Case 3: "This skill doesn't trigger correctly"
**Input**: "skill" + "trigger" + "not correct"
**Intent**: action=fix, domain=skill-system
**SOP**: sop-skill-lifecycle -> diagnose -> fix routing -> verify
**Chain**: li-diagnose (root cause) -> li-skillcreate Phase 3.5 (fix) -> li-sync (propagate)
**Result**: Routing issue found and fixed across all workspaces.

## Anti-patterns

| ID | Anti-pattern | Correct |
|----|-------------|---------|
| AP1 | Keyword-only matching | Combine action + structure + domain + history |
| AP2 | Design intent library from scratch | Mine 188 existing SOPs for patterns |
| AP3 | Same behavior for all confidence | Three-tier: auto/announce/ask |
| AP4 | One skill per intent | SOP = skill chain, not single skill |
| AP5 | Ignore historical experience | Always check memory and skill-usage-log first |
| AP6 | Workspace-bound SOPs | Cross-workspace SOP awareness |
| AP7 | Static intent library | Feedback-driven continuous update |

## Conditional Next Steps

| Condition | Action |
|-----------|--------|
| High confidence intent match | Auto-execute SOP skill chain |
| Medium confidence match | Announce intent then execute |
| No intent match found | Fall back to routing table keywords |
| Historical match different domain | Adapt SOP template, don't force original |
| User corrects intent | Log mismatch, update pattern library |
| New pattern 3+ times | Promote to permanent SOP |
| Skill chain fails mid-execution | Try SOP fallback, then inform user |

## Related Skills

- **li-analyze**: Content analysis - "read/analyze/see" routes here
- **li-research**: Research - "search/research/investigate" routes here
- **li-hardware**: Hardware - FPGA/Arduino/verilog routes here
- **li-debug**: Debugging - "error/bug/not working" routes here
- **li-mindcoach**: Learning - "learn/understand/explain" routes here
- **li-improve**: Evolution - "optimize/upgrade/improve" routes here
- **li-sync**: Maintenance - "sync/organize/clean" routes here

## References Index

| File | Purpose |
|------|---------|
| references/intent-patterns-full.md | Complete pattern library from 188 SOPs |
| references/case-studies.md | Detailed resolution cases |
| references/sop-integration-guide.md | How to connect SOPs to intent engine |

---
*li-intent: not more keywords, but understanding what the user actually wants.*
"""

with open(os.path.join(intent_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
    f.write(skill_md)

# _meta.json
meta = {
    "name": "li-intent",
    "version": "1.0",
    "author": "li-series",
    "description": "SOP-driven intent understanding engine",
    "category": "li-series/infrastructure",
    "created": "2026-06-10",
    "updated": "2026-06-10",
    "line_count": len(skill_md.splitlines()),
    "dependencies": ["li-manage", "li-memory", "li-sync"],
    "related_skills": ["li-analyze", "li-research", "li-hardware", "li-debug", "li-mindcoach", "li-improve"],
    "reference_files": 3,
    "golden_rules": 7
}
with open(os.path.join(intent_dir, '_meta.json'), 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

# eval.json
eval_data = {
    "eval_version": "1.0",
    "assertions": [
        {"check": "SKILL.md exists and >100 lines", "type": "file_exists_and_size"},
        {"check": "Has Phase 0-4 pipeline", "type": "pipeline_completeness"},
        {"check": "Has Theory Table T1-T12", "type": "theory_table"},
        {"check": "Has Design Philosophy with counterexamples", "type": "design_philosophy"},
        {"check": "Has Intent Pattern Library", "type": "content_coverage"},
        {"check": "Has Case Studies (3)", "type": "case_studies"},
        {"check": "Has Anti-patterns (7)", "type": "anti_patterns"},
        {"check": "Has Conditional Next Steps", "type": "next_steps"},
        {"check": "Has Related Skills", "type": "related_skills"},
        {"check": "Has references with content", "type": "references"},
        {"check": "Has golden_rules.md >500B", "type": "golden_rules"},
        {"check": "Has _meta.json", "type": "meta"}
    ]
}
with open(os.path.join(intent_dir, 'eval.json'), 'w', encoding='utf-8') as f:
    json.dump(eval_data, f, indent=2, ensure_ascii=False)

# golden_rules.md
gr = """# Golden Rules - li-intent

GR-001: Intent is pattern not keyword - "read WeChat" and "analyze link" are the same intent [high]
- Source: 2026-06-10 design decision
- Anti-pattern: AP1 keyword-only matching

GR-002: Check historical experience before routing - memory/ and skill-usage-log.md first [high]
- Source: Rewind.ai + 188 SOPs analysis
- Anti-pattern: AP5 ignore history

GR-003: SOPs are the intent implementation - never skip SOP layer [high]
- Source: 5 workspaces SOP index design
- Anti-pattern: AP4 one skill per intent

GR-004: Mine existing SOPs for patterns - don't design from scratch [high]
- Source: 2026-06-10 mistake designing intent-patterns.json ignoring 188 SOPs
- Anti-pattern: AP2 design from scratch

GR-005: Cross-workspace SOP awareness - SOP in X is valid reference in Y [medium]
- Source: li-sync cross-workspace design
- Anti-pattern: AP6 workspace-bound SOPs

GR-006: Feedback refines intent mapping - correction = mismatch = update [high]
- Source: li-improve feedback loop + SOP self-learning framework
- Anti-pattern: AP7 static library

GR-007: Three-tier confidence - auto(>=0.8) announce(0.5-0.8) ask(<0.5) [medium]
- Source: skill-auto-activation confidence threshold
- Anti-pattern: AP3 same behavior all confidence
"""
with open(os.path.join(intent_dir, 'golden_rules.md'), 'w', encoding='utf-8') as f:
    f.write(gr)

# references/intent-patterns-full.md
patterns = """# Intent Pattern Library - Full Reference

## Extraction Method
Patterns extracted from 188 SOPs across 5 workspaces (mutual, competition, creation, job-hunting, personal).

## Content Analysis Intent
IF message contains URL/link AND action=read/analyze
THEN skill_chain = [content-extractor, li-analyze, li-memory]
Confidence boosters: +0.1 if user shared before, +0.1 if topic matches profile

## Content Creation Intent
IF action=write/create AND domain=content
THEN skill_chain = [li-analyze(audience), li-transcript, li-mindcoach(tone)]
Platform: xiaohongshu=short-form, wechat=long-form, PPT=visual

## Research Intent
IF action=search/research AND depth=deep
THEN skill_chain = [li-research, li-devil, li-analyze]
Depth: quick=li-research only, deep=full chain

## Skill Lifecycle Intent
IF domain=skill AND action=create/fuse/optimize
THEN skill_chain = [li-bestskill(search), li-skillcreate, li-manage]

## Debug Intent
IF action=fix/debug AND structure=code/error
THEN skill_chain = [li-debug, li-diagnose]

## Hardware Intent
IF domain=hardware/FPGA/Arduino/verilog
THEN skill_chain = [li-hardware, li-debug, li-sync]

## Learning Intent
IF action=learn/understand/explain
THEN skill_chain = [li-mindcoach, li-analyze]

## Maintenance Intent
IF action=sync/clean/organize
THEN skill_chain = [li-sync, li-manage, li-infra]

## Decision Intent
IF action=decide/choose/evaluate
THEN skill_chain = [li-devil, li-mindcoach]

## Cross-workspace Mapping
| Workspace | Primary Intents | Top SOPs |
|-----------|----------------|----------|
| mutual | management, optimization | SOP index, routing rules |
| competition | hardware, debugging, delivery | FPGA delivery, RTL verification |
| creation | content creation, analysis | Input clarity, content quality |
| job-hunting | resume, interview | Resume optimization, interview prep |
| personal | learning, reflection, planning | Feynman test, retrospective |
"""
with open(os.path.join(refs_dir, 'intent-patterns-full.md'), 'w', encoding='utf-8') as f:
    f.write(patterns)

# references/case-studies.md
cases = """# Case Studies - li-intent

## Case 1: Cross-workspace Intent Resolution
**Scenario**: In competition workspace, "analyze this technical solution"
**Without li-intent**: Matches "analyze" -> generic li-analyze
**With li-intent**: workspace=competition -> SOP-06 hardware design review -> li-hardware + li-analyze + li-devil
**Lesson**: Workspace context changes which SOP matches.

## Case 2: Historical Experience Saves Time
**Scenario**: User shares WeChat article URL for the 3rd time
**Without li-intent**: Each time AI starts from scratch
**With li-intent**: Phase 1 finds 2 previous reads -> baoyu-url-to-markdown + li-analyze -> auto-reuse
**Lesson**: Historical experience is cheapest quality improvement.

## Case 3: Intent Ambiguity Resolution
**Scenario**: "This skill doesn't feel right"
**Ambiguous**: Content wrong? Routing wrong? Trigger wrong?
**Resolution**: Multi-signal fusion + historical weighting -> routing issue (0.7) -> li-diagnose + li-skillcreate
**Lesson**: Multi-signal fusion resolves ambiguity.
"""
with open(os.path.join(refs_dir, 'case-studies.md'), 'w', encoding='utf-8') as f:
    f.write(cases)

# references/sop-integration-guide.md
sop_guide = """# SOP Integration Guide

## How It Works
1. User sends message -> li-intent scans for intent signals
2. li-intent reads current workspace SOP index
3. Matches intent to IF/ELSE routing rules
4. Follows chain-of-calls sequence
5. Each call activates appropriate li-skill
6. Feedback updates intent patterns

## SOP Index Structure (Standard)
Every workspace SOP index contains:
- Routing rules: IF/ELSE pattern matching
- Chain-of-calls: SOP A -> SOP B -> SOP C
- Self-learning: feedback -> pattern -> rule promotion
- Cognitive mapping: task type -> theory -> book reference

## Total: 188 SOPs across 5 workspaces

## Adding New SOPs
1. Define IF/ELSE routing rules
2. Define chain-of-calls (which skills, what order)
3. Define feedback collection
4. Add to workspace SOP index
5. li-intent auto-picks up on next execution
"""
with open(os.path.join(refs_dir, 'sop-integration-guide.md'), 'w', encoding='utf-8') as f:
    f.write(sop_guide)

lines = len(skill_md.splitlines())
print(f'li-intent created: SKILL.md ({lines} lines) + _meta.json + eval.json + golden_rules.md + 3 references')
