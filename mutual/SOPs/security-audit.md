# SOP: 仓库安全审计

> 参考来源：comemo-agent-memory 安全审计（2026-05-28）、我们自己的历史泄露事故
> 适用范围：新仓库创建、CI/CD 集成、代码审计

---

## 三维度安全检查清单

### 维度 1：API Key / Secret 泄露

**检查项**：
- [ ] 全文搜索 `sk-`、`ghp_`、`AKIA`、`xoxb-`、`Bearer` 等密钥前缀模式
- [ ] 检查 `.env`、`*.secret`、`credentials*`、`*.pem`、`*.key`、`*.p12` 是否被提交
- [ ] 检查 `git log -p` 历史中是否有已删除的密钥（浅克隆看不到）
- [ ] 检查 MCP 配置文件（`~/.newmax/.mcp.json`）中是否有明文 API key
- [ ] 检查 `.gitignore` 是否覆盖了 `.env*`、`*.secret`、`*.pem`、`*.key`、`*.p12`

**我们的教训**：MCP 配置写到 `~/.mcp.json`（错误路径）导致配置暴露在非保护目录

### 维度 2：系统代理泄露

**检查项**：
- [ ] 全文搜索 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY`、`SOCKS`、`127.0.0.1:1080`、`localhost:7890` 等代理模式
- [ ] 检查是否有代理地址硬编码在配置文件中
- [ ] 检查 `npm config` 是否残留代理设置（`npm config get proxy`）
- [ ] 检查脚本中是否有 `cmd /c` 包装导致环境变量泄露

**我们的教训**：v2rayN 注入 `HTTP_PROXY=127.0.0.1:10808` 到进程环境变量，代理退出后残留死代理，npm install 将二进制缓存数据写入 JSON 文件导致损坏

### 维度 3：硬编码问题

**检查项**：
- [ ] 搜索个人邮箱（`@gmail.com`、`@qq.com` 等）
- [ ] 搜索绝对路径（`C:\Users\`、`/home/` 等特定用户路径）
- [ ] 搜索特定 IP 地址（非 `0.0.0.0`、`127.0.0.1` 的内网 IP）
- [ ] 搜索数据库连接字符串（`mongodb://`、`postgres://`、`mysql://`）
- [ ] 检查配置文件是否使用占位符（如 `{{API_KEY}}`）而非真实值

---

## 我们 vs comemo 安全实践对比

| 维度 | 我们（历史事故） | comemo（最佳实践） | 改进措施 |
|------|-----------------|-------------------|---------|
| `.gitignore` | 基础配置 | 覆盖 `.env*`/`*.secret`/`*.pem`/`*.key`/`*.p12` | 更新模板 |
| 安全声明 | 无 | `SECURITY.md` 中英双语 | 新项目标配 |
| 代码暴露面 | 有脚本执行 | 纯模板零执行 | 脚本必须审计 |
| MCP 配置 | 写错路径泄露 | 不涉及 | 严守 `~/.newmax/.mcp.json` |
| 代理残留 | npm 代理干扰 | 不涉及 | `npm config set noproxy "*"` |

---

## comemo 值得学习的三个实践

### 实践 1：`.gitignore` 安全模板
```gitignore
# 敏感文件
.env*
*.secret
*.pem
*.key
*.p12
credentials*
```
**为什么好**：覆盖了所有常见敏感文件扩展名，比默认的 Node.js `.gitignore` 更安全。

### 实践 2：`SECURITY.md` 双语安全声明
```markdown
# Security
Do NOT store API keys, passwords, or tokens in comemo memory files.
Comemo memory is plain text stored in your repository.
任何敏感信息都不应该写入 comemo 记忆文件。
```
**为什么好**：从文档层面建立安全边界，用户和 AI 都能看到。双语覆盖中英文用户。

### 实践 3：最小暴露面设计
纯 Markdown 模板仓库 = 从根本上消除代码执行层面的泄露面。
**为什么好**：没有代码 = 没有运行时泄露。这是最安全的设计——从架构层面消除风险，而非靠审计弥补。

---

## 5 分钟快速审计命令

```bash
# 1. API key 扫描
grep -rn "sk-\|ghp_\|AKIA\|xoxb-\|Bearer " . --include="*.md" --include="*.json" --include="*.yml" --include="*.yaml" --include="*.toml" --include="*.py" --include="*.js" --include="*.ts"

# 2. 代理泄露扫描
grep -rn "HTTP_PROXY\|HTTPS_PROXY\|ALL_PROXY\|127.0.0.1:108\|localhost:789" . --include="*.md" --include="*.json" --include="*.yml" --include="*.yaml" --include="*.toml" --include="*.py" --include="*.js"

# 3. 硬编码扫描
grep -rn "@gmail.com\|@qq.com\|@outlook.com\|C:\\\\Users\\\\\|/home/" . --include="*.md" --include="*.json" --include="*.yml" --include="*.yaml" --include="*.toml" --include="*.py" --include="*.js"

# 4. 敏感文件检查
find . -name ".env*" -o -name "*.secret" -o -name "*.pem" -o -name "*.key" -o -name "*.p12" -o -name "credentials*" | grep -v node_modules | grep -v .git

# 5. .gitignore 覆盖检查
echo "=== 应忽略但可能遗漏的文件 ===" && git status --porcelain | grep -E "\.(env|secret|pem|key|p12)$"
```

---

## 场景化检查清单

### 场景 A：新项目启动
- [ ] `.gitignore` 是否覆盖敏感文件扩展名
- [ ] 是否创建了 `SECURITY.md`（中英双语）
- [ ] 代码中是否有硬编码的密钥/路径/邮箱
- [ ] 配置文件是否使用占位符而非真实值

### 场景 B：CI/CD 集成
- [ ] CI 流水线是否集成 `gitleaks` 或 `trufflehog` 密钥扫描
- [ ] 构建产物是否排除敏感文件
- [ ] 环境变量是否通过 CI secrets 注入（而非硬编码在 workflow 文件中）

### 场景 C：代码审计（现有仓库）
- [ ] 执行 5 分钟快速审计命令
- [ ] 检查 Git 完整历史（`git log --all -p`）是否有已删除的密钥
- [ ] 检查所有配置文件（`.json`、`.yml`、`.toml`、`.env`）
- [ ] 检查 `.gitignore` 是否需要更新

---

> 创建日期：2026-05-28
> 来源：comemo-agent-memory 安全审计 + 我们的历史泄露事故
> 相关文件：outputs/security-audit-comemo-2026-05-28.md
