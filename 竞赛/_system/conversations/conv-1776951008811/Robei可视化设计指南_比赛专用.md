# Robei EDA 可视化设计完整指南
## 安全通信系统 - 比赛专用

> ⚠️ 比赛要求：必须基于Robei EDA进行可视化模块设计，不能直接复制开源代码！

---

## 📋 设计原则

### 1. 模块设计规则
```
✅ 可以做：
- 参考架构设计思想
- 自己写算法代码（原创）
- 可视化连线和例化
- 拖入子模块并连接

❌ 不能做：
- 直接复制开源Verilog代码
- 导入已有的.v文件
- 用打孔代替连线
```

### 2. 连线规则
```
顶层连线：
┌─────────────────────────────────────┐
│  模块A      ────线────▶    模块B    │  ✅ 正确：模块间连线
│  端口A     ────线────▶    端口B    │
└─────────────────────────────────────┘

❌ 错误：打孔连接（只有模块内部允许）
```

---

## 🎯 系统架构（可视化设计）

### 第一层：顶层模块 `secure_comm_top`
```
┌─────────────────────────────────────────────────────────┐
│                    secure_comm_top                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │uart_comm│    │ crypto   │    │ protocol│            │
│  │  _top   │    │   _top   │    │   _ctrl │            │
│  └──────────┘    └──────────┘    └──────────┘            │
│                                                          │
│  clk ─────▶│clk│           │clk│           │clk│       │
│  rst_n ───▶│rst│           │rst│           │rst│       │
│             ▼                 ▼                ▼        │
│         tx_data ───────▶ encrypt ───▶ tx                  │
│         rx    ◀───────  decrypt ◀───── rx_data            │
└─────────────────────────────────────────────────────────┘
```

### 第二层：通信层 `uart_comm_top`
```
┌─────────────────────────────────────────┐
│               uart_comm_top             │
│  ┌────────┐  ┌────────┐  ┌────────┐     │
│  │uart_rx│  │uart_tx │  │ crc16  │     │
│  └────────┘  └────────┘  └────────┘     │
│                                          │
│  rx ──▶│rx│──▶│data│──▶│tx│──▶ tx_data  │
│         ────▶│crc│──▶ crc_out            │
└─────────────────────────────────────────┘
```

### 第三层：密码学层 `crypto_top`
```
┌─────────────────────────────────────────┐
│                crypto_top                │
│  ┌────────┐  ┌────────┐  ┌────────┐     │
│  │  ecdh  │  │   aes  │  │ sha256 │     │
│  └────────┘  └────────┘  └────────┘     │
│                                          │
│  key ──▶│ecdh│──▶ shared ──▶│aes│        │
│       ──▶│aes │◀── key                       │
│  data ─────────────────▶│sha │──▶ hash    │
└─────────────────────────────────────────┘
```

---

## 📝 各模块可视化设计步骤

### 模块1: `uart_tx` - 可视化设计

#### 步骤1: 新建模块
```
菜单: File → New
名称: uart_tx
类型: Module
```

#### 步骤2: 添加引脚（图形化）
```
在模块上右键 → Add Pin

输入引脚（左側）:
┌─ clk       input  1bit  ← 时钟
├─ rst_n     input  1bit  ← 复位
├─ tx_data   input  8bit  ← 发送数据
└─ tx_valid  input  1bit  ← 有效信号

输出引脚（右侧）:
├─ tx        output 1bit  → 串口输出
└─ tx_ready  output 1bit  → 就绪信号
```

#### 步骤3: 输入代码（自己写，不是复制）
```verilog
// 自己写的UART发送模块
always @(posedge clk) begin
    if (!rst_n) begin
        tx_reg <= 1;
    end else if (start) begin
        tx_reg <= 0;  // 起始位
    end
end
```

#### 步骤4: 保存
```
Ctrl+S 保存为 uart_tx
```

---

### 模块2: `crc16` - 可视化设计

#### 步骤1: 新建模块
```
名称: crc16
类型: Module
```

#### 步骤2: 添加引脚
```
输入（左側）:
├─ clk        input  1bit
├─ rst_n      input  1bit
├─ data_in    input  8bit
└─ data_valid input  1bit

输出（右侧）:
├─ crc_out    output 16bit
└─ crc_valid  output 1bit
```

#### 步骤3: 自己写代码（参考原理，自己写）
```verilog
// CRC-16 自己写的校验逻辑
always @(posedge clk) begin
    if (!rst_n)
        crc <= 16'hFFFF;
    else if (data_valid)
        crc <= next_crc;
end
```

---

### 模块3: `aes_core` - 可视化设计

#### 步骤1: 新建模块
```
名称: aes_core
类型: Module
```

#### 步骤2: 添加引脚
```
输入（左側）:
├─ clk        input  1bit
├─ rst_n      input  1bit
├─ plaintext  input  128bit
├─ key        input  128bit
└─ start      input  1bit

输出（右侧）:
├─ ciphertext output 128bit
└─ done       output 1bit
```

#### 步骤3: 自己写代码（关键！）
```verilog
// AES-128 核心 - 自己设计的状态机
reg [3:0] round;
reg busy;

// 10轮加密状态机
always @(posedge clk) begin
    if (!rst_n) begin
        round <= 0;
        busy <= 0;
    end else if (start) begin
        busy <= 1;
        round <= 0;
    end else if (busy) begin
        if (round < 10)
            round <= round + 1;
        else
            busy <= 0;
    end
end
```

---

### 模块4: `sha256` - 可视化设计

#### 步骤1: 新建模块
```
名称: sha256
类型: Module
```

#### 步骤2: 添加引脚
```
输入（左側）:
├─ clk        input  1bit
├─ rst_n      input  1bit
├─ data_in    input  32bit
└─ valid      input  1bit

输出（右侧）:
├─ hash_out   output 256bit
└─ done       output 1bit
```

#### 步骤3: 自己写代码
```verilog
// SHA-256 自己写的压缩函数
reg [31:0] H [0:7];

always @(posedge clk) begin
    if (!rst_n) begin
        // 初始哈希值
        H[0] <= 32'h6a09e667;
        H[1] <= 32'hbb67ae85;
        // ... 其他初始化
    end
end
```

---

### 模块5: `ecdh` - 可视化设计

#### 步骤1: 新建模块
```
名称: ecdh
类型: Module
```

#### 步骤2: 添加引脚
```
输入（左側）:
├─ clk        input  1bit
├─ rst_n      input  1bit
├─ start      input  1bit
├─ priv_key   input  256bit
└─ peer_pub_x input  256bit

输出（右侧）:
├─ pub_key_x  output 256bit
├─ pub_key_y  output 256bit
├─ shared     output 256bit
└─ done       output 1bit
```

#### 步骤3: 自己写代码
```verilog
// ECDH 自己写的点运算
reg [255:0] point_x, point_y;
reg done_reg;

// 简单的标量乘法
always @(posedge clk) begin
    if (!rst_n) begin
        done_reg <= 0;
    end else if (start) begin
        // 自己设计的点加逻辑
    end
end
```

---

## 🔗 第四步：创建顶层模块（可视化连线）

### 步骤1: 新建顶层模块
```
名称: secure_comm_top
类型: Module
```

### 步骤2: 添加顶层引脚
```
输入:
├─ clk        input  1bit
├─ rst_n      input  1bit
├─ rx         input  1bit
├─ crypto_op  input  3bit
└─ crypto_st input  1bit

输出:
├─ tx         output 1bit
└─ crypto_do  output 1bit
```

### 步骤3: 例化子模块（拖入）

```
Tools → Add Module → 选择 uart_tx
Tools → Add Module → 选择 crc16
Tools → Add Module → 选择 aes_core
Tools → Add Module → 选择 sha256
Tools → Add Module → 选择 ecdh
```

### 步骤4: 可视化连线

```
连接 clk:
  clk ──────────┬──▶│uart_tx│ clk
               └──▶│crc16 │ clk
               └──▶│aes   │ clk

连接数据:
  rx ─────────▶│uart_tx│ rx
              └──▶│crc16 │ data_in

  │uart_tx│ tx_data ──▶│aes│ plaintext
  │crc16 │ crc_out ──▶│aes│ key

  │aes│ ciphertext ──▶│uart_tx│ tx_data
  │uart_tx│ tx ─────────────▶ tx
```

### 步骤5: 关键规则

```
✅ 正确做法：
模块A的输出 ──────线──────▶ 模块B的输入

❌ 错误做法（禁止打孔）：
模块A的输出 ──孔──▶ 模块B的输入
             ↑
             └── 这是打孔，只能内部用
```

---

## 📊 引脚互联矩阵

### 顶层 `secure_comm_top`

| 源模块 | 源端口 | 连接目标 | 目标端口 | 线类型 |
|--------|--------|----------|----------|--------|
| clk | 时钟源 | uart_tx | clk | 连线 |
| clk | 时钟源 | crc16 | clk | 连线 |
| clk | 时钟源 | aes_core | clk | 连线 |
| clk | 时钟源 | sha256 | clk | 连线 |
| rst_n | 复位源 | uart_tx | rst_n | 连线 |
| rst_n | 复位源 | crc16 | rst_n | 连线 |
| rst_n | 复位源 | aes_core | rst_n | 连线 |
| rst_n | 复位源 | sha256 | rst_n | 连线 |
| rx | 外部输入 | uart_rx | rx | 连线 |
| uart_rx | data | crc16 | data_in | 连线 |
| crc16 | crc_out | aes_core | key | 连线 |
| aes_core | ciphertext | uart_tx | tx_data | 连线 |
| uart_tx | tx | tx | 连线 |
| crypto_op | 操作码 | crypto_top | op | 连线 |

---

## 🎯 第五步：创建Testbench（可视化）

### 步骤1: 新建Testbench
```
名称: secure_comm_tb
类型: Testbench
```

### 步骤2: 添加激励引脚
```
输入:
├─ clk
├─ rst_n
├─ rx
├─ crypto_op
└─ crypto_start

输出:
├─ tx
└─ crypto_done
```

### 步骤3: 例化顶层模块
```
Tools → Add Module → secure_comm_top
```

### 步骤4: 连接激励
```
clk ──────────▶│secure_comm_top│ clk
rst_n ─────────▶│secure_comm_top│ rst_n
rx ────────────▶│secure_comm_top│ rx
```

### 步骤5: 输入激励代码
```verilog
initial begin
    clk = 0;
    rst_n = 0;
    rx = 1;
    #100 rst_n = 1;
    
    // 发送测试数据 0x55
    #100 rx = 0;  // 起始位
    #1000 rx = 1; // 数据位0
    // ... 更多数据位
    #100 $finish;
end

always #10 clk = ~clk;
```

---

## ⚠️ 重要提醒

### 1. 代码必须原创
```
可以参考：
- 算法原理（维基百科）
- 设计思想（教材）
- 架构设计（自己设计）

不能复制：
- 开源代码（GitHub等）
- 现有Verilog文件
- 别人写好的模块
```

### 2. 连线必须完整
```
每个模块间的连接都必须用线连接
不能使用打孔（孔只能用于模块内部信号）
```

### 3. 参赛提交要求
```
提交内容：
1. Robei工程文件（.rbf格式）
2. 每个模块的可视化截图
3. 顶层模块连线截图
4. 仿真波形截图
```

---

## 📋 设计检查清单

### 每个模块检查
- [ ] 有可视化引脚（不是代码定义）
- [ ] 引脚方向正确（input/output）
- [ ] 有代码实现（自己写的）
- [ ] 代码逻辑正确

### 顶层连线检查
- [ ] 所有模块都已例化
- [ ] 时钟信号都连接
- [ ] 复位信号都连接
- [ ] 数据信号都连接
- [ ] 没有悬空的引脚
- [ ] 没有打孔连接

### Testbench检查
- [ ] 类型设为Testbench
- [ ] 有激励代码
- [ ] $finish结束
- [ ] 能看到波形

---

## 🚀 开始动手

### 第一天：创建5个基础模块
1. `uart_tx` - UART发送
2. `uart_rx` - UART接收
3. `crc16` - CRC校验
4. `frame_parser` - 帧解析
5. `frame_builder` - 帧构建

### 第二天：创建密码学模块
1. `aes_core` - AES核心
2. `sha256` - SHA256
3. `ecdh` - ECDH

### 第三天：创建顶层并连线
1. `comm_top` - 通信顶层
2. `crypto_top` - 密码学顶层
3. `secure_comm_top` - 系统顶层
4. 完成所有连线

### 第四天：创建Testbench并仿真
1. 为每个模块创建TB
2. 运行仿真
3. 截图保存波形

### 第五天：整理提交
1. 截图展示
2. 整理文档
3. 录制视频

---

## 📞 需要帮助？

现在你知道怎么做了：
1. **逐个创建模块**（不是导入代码）
2. **自己写代码**（不是复制）
3. **可视化连线**（不是打孔）
4. **完整例化**（每个子模块都要拖入）

需要我帮你创建**某个具体模块的设计步骤**吗？比如：
- UART模块详细设计
- AES模块详细设计
- 顶层连线详细指导
