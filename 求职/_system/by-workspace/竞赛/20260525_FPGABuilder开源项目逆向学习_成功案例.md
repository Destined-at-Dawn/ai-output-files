# FPGABuilder 开源项目逆向学习（2026-05-25）

## 场景
用户要求学习 https://github.com/YiHok/FPGABuilder（65星，CC BY-NC-SA 4.0），提炼可复用模式并改进我们的 Skill 和 SOP。

## 学习过程
1. **全景扫描**：WebFetch 抓取 README + DEVELOPER_OVERVIEW + WORKLOG，10秒建立全局地图
2. **核心代码深挖**：逐个获取 plugin_base.py（插件基类）、plugin.py（Vivado插件）、tcl_templates.py（TCL模板系统）
3. **架构分析**：识别出10个可复用设计模式，对比我们的 gap
4. **知识注入**：提炼为 hardware-design SKILL.md 的新章节 + 跨系统索引新条目

## 提炼的10个核心设计模式

| # | 模式 | FPGABuilder 实现 | 可复用程度 |
|---|------|-----------------|-----------|
| 1 | 插件架构 | `FPGAVendorPlugin` 基类 → Vivado/Quartus 插件 | ★★★ 直接可用 |
| 2 | YAML 配置驱动 | `fpga_project.yaml` 定义全部参数 | ★★★ 直接可用 |
| 3 | Hook 系统 | pre_synth/post_synth 等6个钩子 | ★★★ 直接可用 |
| 4 | 工具自动检测 | `ToolDetector` 找路径和版本 | ★★☆ 需适配 |
| 5 | 版本适配器 | 2019/2023/2024 自动切换 | ★★☆ 需适配 |
| 6 | TCL 模板系统 | 模块化模板组合成完整脚本 | ★★★ 直接可用 |
| 7 | 文件扫描+依赖排序 | 自动扫描 .v/.xdc，按依赖排序 | ★★☆ 需适配 |
| 8 | 三级清理 | soft/hard/all 清理级别 | ★★★ 直接可用 |
| 9 | 设备编程封装 | JTAG/Flash 双模式 | ★★★ 直接可用 |
| 10 | 测试框架 | test_basic/test_hooks | ★☆☆ 暂不需要 |

## 关键架构洞察

### 1. 配置与实现分离（最核心）
```
项目配置(fpga_project.yaml) → 插件管理器 → 厂商插件 → 具体工具链
    ↑描述"做什么"                          ↑实现"怎么做"
```
**启示**：同一份 YAML 可以适配不同厂商工具链。我们目前每次手写 TCL，零复用。

### 2. TCL 模板的模块化
FPGABuilder 把 TCL 脚本拆成独立模板类：
- `BasicProjectTemplate` — 工程创建
- `BDRecoveryTemplate` — Block Design 恢复
- `BuildFlowTemplate` — 完整构建流程
- `CleanTemplate` — 三级清理
- `ProgramDeviceTemplate` — JTAG/Flash 编程

**启示**：我们应该把常用的 TCL 片段模板化，不再从零写。

### 3. Hook 系统的 TCL/非TCL 分离
FPGABuilder 的 hook 系统能自动判断命令是 TCL 还是外部脚本：
- TCL 命令 → 直接嵌入脚本
- Python/Bat 脚本 → 在 Python 层面用 subprocess 执行

**启示**：这是解决"混合构建流程"的关键设计。

### 4. 版本适配器模式
```python
VersionAdapterRegistry.register("vivado", r"2023\..*", Vivado2023Adapter)
```
不同 Vivado 版本有不同的推荐策略和命令参数，适配器自动切换。

### 5. Vivado 工程路径处理
FPGABuilder 特别注意了 Windows 路径问题：
- 统一使用正斜杠 `/` 替代反斜杠 `\`
- 路径构建后 `.replace('\\', '/')`
- 这与我们的 CLAUDE.md §4.3 "中文路径铁律"完全一致

## 与我们的差距总结

| 维度 | FPGABuilder | 我们 |
|------|------------|------|
| 构建自动化 | 一行命令完成全流程 | 每次手写 TCL |
| 多厂商 | 插件适配层 | 只有 Xilinx 经验 |
| 配置管理 | YAML + JSON Schema 验证 | 零配置管理 |
| 代码复用 | 模板系统 + 依赖扫描 | 每次从零开始 |
| 版本兼容 | 自动检测 + 适配器 | 手动确认 |
| 测试 | 自动化测试套件 | 零自动化 |

## 可复用模式
1. **配置驱动思维**：先写配置文件，再执行——不是先执行再配置
2. **模板化 TCL 片段**：常用的 TCL 命令应该模板化，参数化
3. **Hook 系统**：在构建流程的关键节点插入自定义操作
4. **工具检测优先**：执行前先检测环境，而不是执行时报错

## 关联 SOP
- SOP-06 硬件设计与验证（构建流程标准化）
- SOP-08 厂商代码移植（多厂商适配层）
- SOP-01 代码理解重构（插件架构学习）
