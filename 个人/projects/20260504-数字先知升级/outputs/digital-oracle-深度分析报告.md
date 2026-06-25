# Digital Oracle 深度阅读分析报告

> 任务：深度阅读digital-oracle SKILL.md和12个provider源码
> 完成时间：2026-05-04
> 仓库：https://github.com/komako-workshop/digital-oracle (v1.0.3)

---

## 一、核心架构总结

### 设计哲学
Digital Oracle 的核心信念是**"价格包含一切公开信息"**（有效市场假说）。它不消费新闻、观点或统计报告，只从交易数据中挖掘概率信号。

### 五大铁律
1. **只用交易数据** — 价格、成交量、持仓、利差、溢价，禁止引用分析师观点
2. **从价格到判断的显式推理** — 解释"为什么这个价格回答了这个问题"
3. **多信号交叉验证** — 至少3个独立维度，禁止单一信号定论
4. **标注每个信号的时间窗口** — 期权定价3个月，设备订单定价3年，禁止混用
5. **结构化输出** — 分层信号表 → 矛盾分析 → 概率场景 → 一致性评估

### 技术架构
- **依赖注入模式**：所有Provider接受可选 `http_client` 参数，Protocol-based设计
- **部分失败容忍**：`gather()` 并行调用，单个数据源失败不影响其他结果
- **快照测试**：RecordingHttpClient/ReplayHttpClient 实现HTTP录制/回放
- **零依赖优先**：14个Provider中12个纯Python标准库，仅2个需要yfinance
- **~4,778行Python代码**，全部MIT开源

---

## 二、14个Provider完整能力图谱

### Tier 1：预测市场（事件概率定价）

| Provider | 数据类型 | API端点 | 关键限制 |
|----------|---------|---------|---------|
| **PolymarketProvider** | 预测市场合约 | gamma-api.polymarket.com | slug搜索是模糊的，需标题二次过滤；流动性<$100K的合约应打折 |
| **KalshiProvider** | SEC监管二元合约 | api.elections.kalshi.com | 不支持关键词搜索，必须用series_ticker；价格单位是美分需/100 |

**对百大认知书籍的意义**：这两个Provider直接定价"事件发生的概率"——是《社会动物》群体心理、《垃圾桶模型》时机分析的**实时数据引擎**。

### Tier 2：宏观金融信号

| Provider | 数据类型 | API端点 | 关键限制 |
|----------|---------|---------|---------|
| **USTreasuryProvider** | 国债收益率曲线+汇率 | home.treasury.gov + api.fiscaldata.treasury.gov | CSV解析，支持nominal/real/bill/long_term四种曲线 |
| **CMEFedWatchProvider** | FOMC利率隐含概率 | cmegroup.com/services/fed-funds-target | CME端点偶尔不可用，可回退到Kalshi KXFED |
| **BisProvider** | 央行政策利率+信贷/GDP缺口 | stats.bis.org/api/v1 | 数据更新慢（月度/季度），适合长期趋势 |
| **WorldBankProvider** | GDP/人口/贸易发展指标 | api.worldbank.org/v2 | 数据滞后1-2年，最新年份可能为None |

**对百大认知书籍的意义**：《权力》的权力流向分析需要央行利率+国债收益率；《反脆弱》的杠铃策略需要收益率曲线形态判断经济周期位置。

### Tier 3：市场情绪与机构仓位

| Provider | 数据类型 | API端点 | 关键限制 |
|----------|---------|---------|---------|
| **FearGreedProvider** | CNN恐惧贪婪指数（7信号合成0-100） | production.dataviz.cnn.io | 需浏览器UA头防封，单值但综合7个维度 |
| **CftcCotProvider** | 期货持仓报告（机构方向） | publicreporting.cftc.gov | 每周二更新，周五发布；commodity_name用大写 |
| **EdgarProvider** | SEC内部人交易Form 4 | data.sec.gov + efts.sec.gov | 必须在User-Agent中带email否则403 |

**对百大认知书籍的意义**：CFTC持仓是《结构洞》信息不对称套利的直接证据；FearGreed是《社会动物》从众心理的量化温度计。

### Tier 4：价格与衍生品数据

| Provider | 数据类型 | API端点 | 关键限制 |
|----------|---------|---------|---------|
| **YahooPriceProvider** | 全球价格历史（股/ETF/外汇/商品） | yfinance库 | 需pip install yfinance |
| **YFinanceProvider** | US期权链+Black-Scholes Greeks | yfinance库 | 需pip install yfinance；盘后IV可能不准 |
| **DeribitProvider** | 加密衍生品（期货曲线+期权链） | deribit.com/api/v2 | 最复杂的Provider(~547行)，多API调用+年化基差计算 |
| **CoinGeckoProvider** | 加密现货价格/市值 | api.coingecko.com/api/v3 | 免费API有速率限制(~10-30 req/min) |
| **StooqProvider** | 价格数据兼容层 | 委托给YahooPriceProvider | 实际是Stooq→Yahoo符号映射层 |

**对百大认知书籍的意义**：期权链（IV/Greeks/max pain）是量化"市场恐惧"的数学工具；Deribit期货曲线（contango/backwardation）是加密市场风险偏好的直接指标。

### Tier 5：通用信息获取

| Provider | 数据类型 | API端点 | 关键限制 |
|----------|---------|---------|---------|
| **WebSearchProvider** | DuckDuckGo搜索+页面抓取 | html.duckduckgo.com/html | 2秒全局速率限制；CAPTCHA检测+重试 |

**特殊地位**：VIX、MOVE、CDS利差、TTF天然气、BDI运价等数据无结构化API，只能通过WebSearch获取。这些仍是交易数据，符合方法论。

---

## 三、核心工具函数

### `gather()` — 并行数据拉取
```python
gather(tasks_dict, max_workers=8, timeout_seconds=60, fail_fast=False) -> GatherResult
```
- 使用 `ThreadPoolExecutor` 并行执行
- `GatherResult.get(key)` 获取结果，`GatherResult.get_or(key, default)` 带默认值
- `GatherResult.errors` 记录失败的任务（部分失败不中断其他任务）

### `black_scholes_greeks()` — 期权Greeks计算
- 纯Python标准库实现（math.erf），无需scipy
- 返回 OptionGreeks(delta, gamma, theta, vega)

---

## 四、数据源×百大认知书籍 初步映射关系

| 书籍核心概念 | 最匹配的数据源组合 | 决策场景 |
|------------|-----------------|---------|
| 《反脆弱》杠铃策略 | VIX(WebSearch) + 收益率曲线(Treasury) + FearGreed | 实时反脆弱调仓：极端恐惧时加仓风险端 |
| 《权力》权力流向 | SEC内部人交易(EDGAR) + 央行利率(BIS) + 国债收益率 | 权力资本地图：内部人集中减持=权力转移信号 |
| 《社会动物》从众分析 | Polymarket概率 + FearGreed + Put/Call比率(YFinance) | 群体非理性窗口：极端情绪=逆向指标 |
| 《结构洞》网络套利 | CFTC持仓(COT) + 多市场价格差异 | 信息不对称信号：机构仓位vs价格分歧 |
| 《垃圾桶模型》时机 | 事件概率流(Polymarket+Kalshi) + 市场波动率 | 决策垃圾桶能量：多个不相关市场同时异动=高能量窗口 |
| 《错觉》注意盲区 | 内部人交易(EDGAR) + 行业ETF偏离 | 识别市场忽视的信号：基本面vs价格偏离 |
| 《延伸的表型》 | 行业上游设备订单 + CapEx趋势(WebSearch) | 产业链因果链：上游先行指标→下游跟随 |
| 《聪明却散漫》执行功能 | FearGreed + VIX + max_pain(YFinance) | 纪律化决策：用量化信号替代情绪判断 |

---

## 五、环境搭建状态

### 已完成
- ✅ 仓库已克隆到 `digital-oracle/` 子目录
- ✅ 目录结构完整：providers(18个.py) + references + scripts + tests

### 待完成（Phase 1 剩余）
- ⬜ 安装uv包管理器
- ⬜ 安装yfinance依赖：`uv pip install yfinance`
- ⬜ 运行demo脚本验证连通性

---

## 六、关键发现与注意事项

1. **StooqProvider是兼容层**：README说12个数据源，但Stooq实际委托给YahooPriceProvider，不是独立数据源。实际独立API=13个（加上WebSearch=14个Provider，12个独立数据API）。

2. **时间窗口是核心**：SKILL.md反复强调"不要混合不同时间窗口的信号"。短期（3-12月）看预测市场/VIX/价格反应；中期（1-3年）看营收共识/CapEx；长期（3-10年）看设备订单/不可逆资本配置。

3. **"方向对但时机错"不等于矛盾**：短期看空+长期看多 ≠ 矛盾，= S曲线拐点。这是《反脆弱》杠铃策略的数学基础。

4. **EDGAR需要邮箱**：`EdgarProvider(user_email="xxx@example.com")`，否则SEC返回403。

5. **CoinGecko有速率限制**：免费API约10-30 req/min，不要在单次gather中塞太多CoinGecko调用。

6. **Kalshi不支持关键词搜索**：必须用series_ticker（如KXFED、KXINX、KXGDP）或event_ticker过滤。

7. **WebSearch是万能后备**：VIX、MOVE、CDS、BDI等没有结构化API的数据，统一走DuckDuckGo搜索。


---

## 认知科学支撑：深度分析报告的认知原理（百大认知书籍）

| 认知机制 | 来源 | 在深度分析报告中的应用 |
|---------|------|------------------------------|
| **深度加工** | 009-认知天性 §concept1 | 深度分析=深度加工——"不是'看表面数据'→是'挖掘数据背后的意义'"→"深度加工=长时记忆的条件"→"浅加工→遗忘→深加工→记忆持久" |
| **批判性思维** | 023-认知觉醒 §concept1 | 深度分析=批判性思维——"数据可信吗？来源可靠吗？结论合理吗？"→"批判性思维='不轻信'→'追问为什么'→'验证假设'"→"批判性=分析质量的保障" |
| **决策支持** | 010-思考快与慢 §concept1 | 分析报告=决策支持——"不是'做决定'→是'提供做决定的信息'"→"好的分析→清晰的选项+每个选项的风险/收益"→"决策者=人→信息提供者=报告"→"分工=最优" |
