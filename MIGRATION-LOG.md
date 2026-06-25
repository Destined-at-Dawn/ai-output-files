# 迁移日志

## 迁移时间
2026-06-25 20:04:06

## 迁移内容

### Phase 1: 目录骨架
- 创建 F:i产出文件\ 主目录结构
- 包含 7 个工作区 + 共享层 + 桥接层 + 知识中枢 + 归档

### Phase 2: 工作区迁移

| 工作区 | 文件数 | 路径替换 | 状态 |
|--------|--------|----------|------|
| mutual | 1020 | 28 | 完成 |
| 竞赛 | 511 | 24 | 完成 |
| 创作 | 597 | 3 | 完成 |
| 求职 | 245 | 2 | 完成 |
| 个人 | 11637 | 1 | 完成 |
| 学习 | 77 | 0 | 完成 |
| 日常学习 | 1146 | - | 完成 |
| 论文 | - | - | 不存在 |

### Phase 3: 共享资源整合
- 19 个共享规则 -> _sharedules- skill-routing-table.json -> _shared\skill-registry- CLAUDE.md 标准模板 -> _shared	emplates
### Phase 4: 桥接层
- CLAUDE-bridge.md -> _work-bridge
### Phase 5: 文档
- VARIABLE-REFERENCE.md -> 变量参考手册
- MIGRATION-LOG.md -> 本文件

## 大文件处理

| 目录 | 大小 | 处理方式 |
|------|------|----------|
| 竞赛/projects/ | 13GB | 保留原位，创建 DATA-LOCATION.md 说明 |
| 创作/outputs/ | 8.4GB | 保留原位，创建 DATA-LOCATION.md 说明 |
| 创作/projects/ | 4GB | 保留原位，创建 DATA-LOCATION.md 说明 |
| 个人/百大认知书籍/ | ~2GB | 已复制 |

## 下一步

1. 测试新路径下的 CLAUDE.md 是否能被 Claude Code 正确加载
2. 测试 skill 路由是否正常工作
3. 更新 ~/.newmax/ 中的全局配置
4. 逐步将新工作迁移到 F:i产出文件