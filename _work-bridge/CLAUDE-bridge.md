# F:\work 桥接配置

## 背景
F:\work 是用户的实际工作目录（网页设计、个人建站、竞赛等）。
AI 在 F:\work 下工作时，需要加载 F:i产出文件 中的经验、skill 和配置。

## 变量映射
- ${WORK_ROOT} = F:\work
- ${AI_ROOT} = F:i产出文件
- ${KNOWLEDGE_HUB} = F:i产出文件\知识中枢
- ${SHARED_RULES} = F:i产出文件\_sharedules
- ${SKILL_REGISTRY} = F:i产出文件\_shared\skill-registry

## 桥接协议

### 1. 启动时加载
当 AI 在 F:\work 下启动时，自动加载：
1. ${AI_ROOT}/_shared/rules/ 下的所有共享规则
2. ${AI_ROOT}/_shared/skill-registry/skill-routing-table.json
3. ${KNOWLEDGE_HUB}/00-注册表/工作区注册表.md

### 2. 经验读取
工作中的经验记录写入：
- 项目级：${WORK_ROOT}/{项目名}/memory/
- 跨项目：${AI_ROOT}/_shared/lessons/

### 3. Skill 调用
skill 路由表位于 ${AI_ROOT}/_shared/skill-registry/
skill 文件位于 ~/.newmax/skills/

### 4. 文件输出
- 代码文件：留在 F:\work 对应项目目录
- 经验/SOP：写入 ${AI_ROOT}/ 对应工作区
- 归档：写入 ${AI_ROOT}/归档/

## F:\work 项目与 AI 工作区映射

| F:\work 项目 | AI 工作区 | 说明 |
|---------------|----------|------|
| 网页设计 | 创作 | 网页设计相关经验 |
| 个人建站 | 个人 | 个人网站建设经验 |
| 竞赛工作流包 | 竞赛 | 竞赛相关经验 |
| 接单 | 求职 | 接单/自由职业经验 |

## 使用方式
在 F:\work 下启动 AI 时，提示词中包含：
"加载桥接配置：F:i产出文件\_work-bridge\CLAUDE-bridge.md"
