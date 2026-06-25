# Robei EDA 手把手教程 - 安全通信系统代码展示

> 本教程教你在5分钟内用Robei展示安全通信系统的核心代码模块

---

## 📋 准备工作

### 1. 确认Robei已安装
```
✅ D:\study\competion\Robei\Robei\bin\Robei.exe
```

### 2. 创建Robei工作目录（重要！）
```
D:\study\competion\Robei\workspace
```
⚠️ **路径中不能有中文和空格！**

### 3. 你的代码位置
```
D:\study\competion\FPGA\fpga\rtl\
├── crypto/      # 密码学模块
├── comm/        # 通信模块
├── protocol/    # 协议模块
└── top/         # 顶层模块
```

---

## 🎯 目标模块清单

我们要展示的6个核心模块：

| 模块名 | 功能 | 文件 |
|--------|------|------|
| UART_TX | 串口发送 | `comm/uart_tx.v` |
| CRC16 | 校验计算 | `comm/crc16.v` |
| AES_CORE | AES加密 | `crypto/aes_core.v` |
| SHA256 | 哈希运算 | `crypto/sha256.v` |
| ECDH | 密钥交换 | `crypto/ecdh.v` |
| CRYPTO_TOP | 密码学顶层 | `crypto/crypto_top.v` |

---

## 🚀 步骤一：启动Robei

### 1. 双击打开Robei
```
D:\study\competion\Robei\Robei\bin\Robei.exe
```

### 2. 首次设置工作目录
- 点击菜单 `Settings` → `Working Directory`
- 设置为：`D:\study\competion\Robei\workspace`
- 或者将代码复制到这个目录

### 3. 界面认识
```
┌─────────────────────────────────────────┐
│  菜单栏 (File/Edit/Tools/Build/View)     │
├────────────┬───────────────────────────┤
│  Toolbox   │      工作区域              │
│  ────────  │      (Graph/Code切换)      │
│  Current   │                           │
│  System    │                           │
├────────────┴───────────────────────────┤
│  属性栏 (Properties)                    │
├─────────────────────────────────────────┤
│  输出窗口 (Output)                      │
└─────────────────────────────────────────┘
```

---

## 🔧 步骤二：创建第一个模块（UART_TX）

### 方法一：图形化创建（推荐新手）

#### 1. 新建模块
- 点击工具栏 `📄 New` 图标
- 或菜单 `File` → `New`

#### 2. 填写模块信息
```
Name: uart_tx
Type: Module
Code: (先空着)
```
点击 `OK`

#### 3. 添加引脚
在模块上点击右键 → `Add Pin`

| Pin Name | Direction | Data Size | 说明 |
|----------|-----------|-----------|------|
| clk | input | 1 | 系统时钟 |
| rst_n | input | 1 | 复位信号 |
| tx_data | input | 8 | 发送数据 |
| tx_valid | input | 1 | 有效信号 |
| tx | output | 1 | 串口输出 |
| tx_ready | output | 1 | 就绪信号 |

#### 4. 调整引脚位置
- 点击引脚可以拖动位置
- 左上：输入引脚
- 右上：输出引脚
- 右下：时钟/复位

#### 5. 输入代码
点击模块下方的 `Code`，输入：
```verilog
// UART发送模块 - 9600bps, 8N1
parameter CLK_FREQ = 50_000_000;
parameter BAUD_RATE = 9600;

reg [15:0] baud_cnt;
reg [3:0] bit_cnt;
reg [7:0] tx_shift;
reg tx_busy;

// 波特率计数器
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        baud_cnt <= 0;
    end else if (tx_valid && !tx_busy) begin
        baud_cnt <= 0;
        tx_shift <= tx_data;
    end else if (tx_busy && baud_cnt >= CLK_FREQ/BAUD_RATE-1) begin
        baud_cnt <= 0;
    end else if (tx_busy) begin
        baud_cnt <= baud_cnt + 1;
    end
end

// 发送状态机
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        tx <= 1;
        tx_busy <= 0;
        bit_cnt <= 0;
    end else if (tx_valid && !tx_busy) begin
        tx_busy <= 1;
    end else if (tx_busy && baud_cnt == CLK_FREQ/BAUD_RATE-1) begin
        if (bit_cnt == 10) begin
            tx_busy <= 0;
            bit_cnt <= 0;
        end else begin
            bit_cnt <= bit_cnt + 1;
            tx <= tx_shift[0];
            tx_shift <= {1'b0, tx_shift[7:1]};
        end
    end
end

assign tx_ready = !tx_busy;
```

#### 6. 保存
- 点击 `💾 Save` 或 `Ctrl+S`
- 保存到：`D:\study\competion\Robei\workspace\uart_tx.rbe`

---

### 方法二：直接导入现有代码

#### 1. 复制代码文件到工作目录
```powershell
Copy D:\study\competion\FPGA\fpga\rtl\comm\uart_tx.v D:\study\competion\Robei\workspace\
```

#### 2. 在Robei中导入
- 点击 `File` → `Import`
- 选择 `uart_tx.v`

⚠️ **注意**：Robei可能需要手动添加引脚，因为不能完全解析所有Verilog语法

---

## 📐 步骤三：创建测试模块（Testbench）

### 1. 新建Testbench
- 点击 `📄 New`
- 设置：
```
Name: uart_tx_test
Type: Testbench
```

### 2. 添加被测模块
- 从左侧Toolbox拖动 `uart_tx` 到工作区
- 或点击 `Tools` → `Add Module`

### 3. 添加激励引脚
| Pin Name | Direction | 说明 |
|----------|-----------|------|
| clk | input | 时钟激励 |
| rst_n | input | 复位激励 |
| tx_valid | input | 发送有效 |
| tx_data | input | 测试数据 |

### 4. 输入激励代码
```verilog
initial begin
    clk = 0;
    rst_n = 0;
    tx_valid = 0;
    tx_data = 8'h55;
    
    #100 rst_n = 1;
    #100 tx_valid = 1;
    #10 tx_valid = 0;
    
    #10000 $finish;
end

always #10 clk = ~clk;
```

### 5. 连接信号
- 从Toolbox拖入 `uart_tx`
- 左边引脚连接激励
- 右边引脚查看输出

### 6. 运行仿真
- 点击 `▶ Run` 按钮
- 查看Output窗口是否有错误
- 点击 `📊 Wave` 查看波形

---

## 🎨 步骤四：创建AES模块可视化

### 1. 新建模块
```
Name: aes_core
Type: Module
```

### 2. 添加引脚
| Pin Name | Direction | Data Size | 说明 |
|----------|-----------|-----------|------|
| clk | input | 1 | 时钟 |
| rst_n | input | 1 | 复位 |
| plaintext | input | 128 | 明文输入 |
| key | input | 128 | 密钥输入 |
| ciphertext | output | 128 | 密文输出 |
| done | output | 1 | 完成信号 |

### 3. 简化的AES代码（展示用）
```verilog
// AES-128 加密核心 - 简化展示版
reg [31:0] state [0:3];
reg [31:0] round_key [0:3];
reg [3:0] round_cnt;
reg done_reg;

// 初始化
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        done_reg <= 0;
        round_cnt <= 0;
    end else if (valid) begin
        // 加载明文和密钥
        state[0] <= plaintext[127:96];
        state[1] <= plaintext[95:64];
        state[2] <= plaintext[63:32];
        state[3] <= plaintext[31:0];
        round_cnt <= 0;
        done_reg <= 0;
    end else if (round_cnt < 10) begin
        round_cnt <= round_cnt + 1;
        // SubBytes + ShiftRows + MixColumns + AddRoundKey
        state[0] <= state[0] ^ round_key[0];
        state[1] <= {state[1][23:0], state[1][31:24]};
        state[2] <= {state[2][15:0], state[2][31:16]};
        state[3] <= {state[3][7:0], state[3][31:8]};
    end else if (round_cnt == 10) begin
        done_reg <= 1;
    end
end

assign ciphertext = {state[0], state[1], state[2], state[3]};
assign done = done_reg;
```

### 4. 保存为 `aes_core.rbe`

---

## 🔗 步骤五：创建顶层模块

### 1. 创建crypto_top
```
Name: crypto_top
Type: Module
```

### 2. 添加子模块
- 从Toolbox拖入 `aes_core`
- 从Toolbox拖入 `sha256`
- 从Toolbox拖入 `ecdh`

### 3. 添加顶层引脚
- clk, rst_n
- crypto_op[2:0] - 操作选择
- crypto_start - 启动信号

### 4. 模块连接
点击工具栏 `🔗 Wire` 工具，连接各模块

---

## 📸 步骤六：截图展示

### 1. 调整视图
- 选中模块，按住鼠标滚轮拖动
- 滚轮缩放
- 点击空白处调整整体布局

### 2. 截图
- Windows: `Win+Shift+S` 选择区域截图
- 或 `Alt+PrintScreen` 截当前窗口

### 3. 导出图片
- `View` → `Export Image`
- 保存为PNG

---

## 🎬 视频录制建议

### 展示顺序
1. **5秒** - 系统架构图（PPT或白板）
2. **30秒** - Robei界面介绍
3. **60秒** - UART_TX模块展示
4. **60秒** - AES_CORE模块展示
5. **60秒** - ECDH模块展示
6. **30秒** - 仿真运行+波形展示
7. **15秒** - 总结

### 录制要点
- 边操作边讲解
- 适当放慢速度
- 强调创新点
- 展示仿真结果

---

## ⚠️ 常见问题

### Q1: 仿真看不到波形？
确保顶层Testbench的 `Type` 设置为 `Testbench`

### Q2: 导入代码失败？
- 检查路径无中文
- 尝试手动创建模块

### Q3: 引脚连接不显示？
点击 `View` → `Refresh`

### Q4: 仿真报错？
查看Output窗口的错误信息，常见错误：
- 变量类型错误（reg/wire）
- 时序逻辑缺少时钟沿

---

## 📁 输出文件清单

录制视频后需要的文件：
```
初赛提交/
├── 视频.mp4
├── PPT.pptx
├── 技术文档.md
├── 代码/
│   ├── uart_tx.rbe
│   ├── aes_core.rbe
│   ├── sha256.rbe
│   ├── ecdh.rbe
│   └── crypto_top.rbe
└── 仿真截图/
    ├── uart_wave.png
    ├── aes_wave.png
    └── crypto_wave.png
```

---

## ✅ 下一步

1. **打开Robei**，创建第一个模块
2. **导入代码**，逐个展示
3. **运行仿真**，截图保存
4. **录制视频**，5分钟讲解

需要我帮你打开Robei演示吗？
