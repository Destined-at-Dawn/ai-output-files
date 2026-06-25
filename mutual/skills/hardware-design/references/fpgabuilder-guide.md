## 核心设计理念

### 工具链解耦

FPGABuilder 将开发项目与具体工具链完全解耦：

```
传统方式：项目文件 → 特定工具链脚本 → 厂商工具
FPGABuilder方式：项目配置 → 插件管理器 → 厂商插件 → 具体工具链
```

**解耦优势**：
- **可移植性**：同一项目可在 Vivado ↔ Quartus 间切换，只需改 YAML 中的 vendor 字段
- **可维护性**：工具链更新不影响项目配置
- **可扩展性**：新增厂商只需实现插件接口

### 配置驱动

所有项目行为由 `fpga_project.yaml` 定义，支持版本控制和团队协作。

## 项目结构（推荐）

```
my_project/
├── fpga_project.yaml      # 工程配置文件（核心）
├── src/
│   ├── hdl/               # HDL 源代码
│   │   ├── *.sv           # SystemVerilog（推荐）
│   │   ├── *.v            # Verilog
│   │   └── *.vhd          # VHDL
│   ├── constraints/       # 约束文件（XDC/SDC）
│   └── ip/                # 自带 IP 核
├── ip_repo/               # 第三方 IP 核（git submodule）
├── lib/                   # 第三方库（git submodule）
├── docs/                  # 项目文档
├── build/                 # 构建输出
│   ├── reports/           # 时序/面积报告
│   ├── bitstreams/        # 比特流文件
│   └── logs/              # 构建日志
└── tests/                 # 测试文件
```

## YAML 配置文件

### 完整示例

```yaml
project:
  name: "my_fpga_project"
  version: "1.0.0"
  description: "项目描述"

fpga:
  vendor: "xilinx"         # xilinx | intel | lattice
  family: "zynq-7000"      # 器件系列
  part: "xc7z045ffg676-2"  # 具体器件型号
  top_module: "system_wrapper"

source:
  hdl:
    - path: "src/hdl/**/*.sv"
      language: "systemverilog"
    - path: "src/hdl/**/*.v"
      language: "verilog"
    - path: "src/hdl/**/*.vhd"
      language: "vhdl"
  constraints:
    - path: "src/constraints/*.xdc"

dependencies:
  git_submodules:
    - path: "lib/common"
      url: "git@example.com:fpga/common.git"

build:
  synthesis:
    strategy: "out_of_context"
  implementation:
    opt_design: true
    place_design: true
    route_design: true
  hooks:
    pre_build: "scripts/env_check.sh"
    pre_synth: "scripts/pre_synth.tcl"
    post_synth: "scripts/post_synth.py"
    pre_impl: "scripts/pre_impl.sh"
    post_impl: "scripts/post_impl.py"
    post_bitstream: "scripts/copy_bitstream.sh"
    custom_scripts:
      timing_report: "scripts/timing_summary.tcl"
```

### 关键配置项说明

| 字段 | 说明 | 常用值 |
|------|------|--------|
| fpga.vendor | FPGA 厂商 | xilinx, intel, lattice |
| fpga.family | 器件系列 | Zynq-7000, Kintex-7, Cyclone V 等 |
| fpga.part | 精确器件型号 | 工具会根据型号选择封装 |
| build.synthesis.strategy | 综合策略 | out_of_context, default |
| build.hooks.* | 构建钩子 | 支持 .sh / .tcl / .py 脚本 |

## CLI 命令速查

### 项目初始化

```bash
# 创建新项目（指定厂商和器件）
FPGABuilder init my_project --vendor xilinx --part xc7z045ffg676-2

# 创建 Zynq 模板项目
FPGABuilder init my_zynq --vendor xilinx --part xc7z045ffg676-2 --template zynq

# 交互式配置（menuconfig 界面）
FPGABuilder config
```

### 构建命令

```bash
# 完整构建（综合 → 实现 → 比特流）
FPGABuilder build

# 仅综合
FPGABuilder synth

# 仅实现（布局布线）
FPGABuilder impl

# 仅生成比特流
FPGABuilder bitstream

# 烧录到 FPGA
FPGABuilder program --cable xilinx_tcf --target hw_server:3121

# 清理构建产物
FPGABuilder clean --all
```

### IP 核管理

```bash
# 创建 AXI4-Lite IP 核
FPGABuilder ip create axi_uart --type axi4lite

# 管理第三方 IP（git submodule）
FPGABuilder ip add <repo_url> --path ip_repo/my_ip
```

### 辅助命令

```bash
# 生成项目文档
FPGABuilder docs --format mkdocs --output docs/

# 查看帮助
FPGABuilder --help
FPGABuilder <command> --help

# 查看版本
FPGABuilder --version
```

## 构建流程（Vivado 后端）

```
FPGABuilder build
  |
  +-- 1. 解析 fpga_project.yaml
  |
  +-- 2. 调用 Vivado 插件
  |     +-- 创建工程（.xpr）
  |     +-- 添加源文件和约束
  |     +-- 设置器件型号
  |
  +-- 3. 综合（Synthesis）
  |     +-- pre_synth hook
  |     +-- run_synth_design
  |     +-- post_synth hook
  |
  +-- 4. 实现（Implementation）
  |     +-- pre_impl hook
  |     +-- opt_design → place_design → route_design
  |     +-- post_impl hook
  |
  +-- 5. 比特流生成
  |     +-- write_bitstream
  |     +-- bin_merge_script（可选，用于 Zynq 合并 BOOT.BIN）
  |     +-- post_bitstream hook
  |
  +-- 6. 输出：build/bitstreams/*.bit / *.bin
```

## 构建钩子（Hooks）系统

钩子允许在构建流程的关键节点插入自定义脚本：

| 钩子 | 触发时机 | 典型用途 |
|------|---------|---------|
| pre_build | 构建开始前 | 环境检查、依赖下载 |
| pre_synth | 综合前 | 自定义 Tcl 预处理 |
| post_synth | 综合后 | 生成综合报告 |
| pre_impl | 实现前 | 资源预分配 |
| post_impl | 实现后 | 时序分析、报告生成 |
| post_bitstream | 比特流后 | 文件拷贝、通知发送 |
| bin_merge_script | 比特流合并 | Zynq BOOT.BIN 生成 |
| custom_scripts.* | 自定义 | 任意扩展脚本 |

钩子脚本支持 `.sh`、`.tcl`、`.py` 三种格式。

## 多厂商支持

### Xilinx Vivado

- 完整支持 Zynq-7000、Kintex-7、Artix-7、UltraScale 等系列
- 自动调用 Vivado Tcl 命令（create_project, synth_design, place_design, route_design）
- 支持 ILA 在线调试核生成

### Intel Quartus

- 支持 Cyclone V、Arria 10、Stratix 10 等系列
- 通过 Quartus 插件调用 quartus_sh 脚本
- SignalTap II 集成支持

### 切换厂商

只需修改 `fpga_project.yaml` 中的 vendor 和 part 字段，无需修改 RTL 代码（前提是 RTL 未使用厂商原语）。

## 从传统项目迁移

如果你已有 Vivado/Quartus 项目，可以迁移到 FPGABuilder 管理：

1. 创建 `fpga_project.yaml`：填写器件信息和源文件路径
2. 整理目录结构：将源码移入 `src/hdl/`，约束移入 `src/constraints/`
3. 提取约束：将 TCL 脚本中的约束转为 XDC/SDC 文件
4. 验证构建：运行 `FPGABuilder build` 对比结果

## 与 RTL 编码规范的配合

FPGABuilder 与上文的 RTL 编码规范协同工作：

1. **RTL 编码** → 按 SystemVerilog 规范编写（always_comb/always_ff 分离、命名规范等）
2. **Lint 检查** → Verilator --lint-only 通过后再提交
3. **项目配置** → YAML 中指定源文件路径和约束文件
4. **自动构建** → FPGABuilder build 一键完成综合→实现→比特流
5. **报告审查** → 查看 build/reports/ 中的时序和资源报告
6. **迭代优化** → 根据报告修改 RTL，重复步骤 1-5

## 推荐工作流

```bash
# 1. 编写 RTL（遵循编码规范）
vim src/hdl/my_module.sv

# 2. Lint 检查
verilator --lint-only -Wall src/hdl/my_module.sv

# 3. 单元测试
verilator --binary -Wall my_module_tb.sv my_module.sv && ./obj_dir/Vmy_module_tb

# 4. 提交代码
git add src/hdl/ && git commit -m "feat: add my_module"

# 5. 自动构建
FPGABuilder build

# 6. 检查报告
cat build/reports/timing_summary.rpt
cat build/reports/utilization.rpt

# 7. 烧录验证
FPGABuilder program --cable xilinx_tcf
```

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| 时序不收敛 | 增加流水级、调整约束、更换器件速度等级 |
| LUT 用量超限 | 优化状态机编码、复用逻辑、使用 BRAM 替代 LUT RAM |
| CDC 违例 | 添加同步器、使用 gray 码 FIFO |
| Vivado 找不到器件 | 检查 fpga.part 是否正确、安装对应器件包 |
| 构建脚本不执行 | 检查脚本权限、路径是否正确 |
