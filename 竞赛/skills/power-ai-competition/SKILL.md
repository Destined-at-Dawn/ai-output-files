# Skill: power-ai-competition

> **电力 AI 视觉巡检竞赛全流程 Skill**
> 覆盖数据集管理 → 数据预处理 → 模型训练 → 量化优化 → 竞赛 SOP → 论文产出
> 创建日期：2026-06-12
> 版本：v1.0

---

## 一、Skill 定位

本 skill 是 2026 电力行业大学生电力 AI 视觉巡检竞赛（常规赛道）的**全流程工作流引擎**。

### 覆盖范围
1. **数据集搜索与下载**：CPLID、InsPLAD、IDID、TLID、MPID 等公开数据集
2. **数据预处理**：VOC→YOLO 格式转换、类别映射、数据集融合、EDA
3. **模型训练**：YOLO12n 多源融合训练、超参优化、消融实验
4. **模型量化与优化**：FP32→FP16→INT8、ONNX 导出、边缘部署
5. **竞赛 SOP**：6 个实操单元 + 4 个理论模块
6. **论文产出**：方法论、实验结果、消融实验、参考文献管理

### 触发条件
- 用户提到"竞赛""电力巡检""绝缘子检测""数据集""YOLO训练""量化""部署"
- 用户要求搜索新数据集、改进训练、准备竞赛材料

---

## 二、数据集管理子工作流

### 2.1 已知数据集清单

| 数据集 | 来源 | 规模 | 标签格式 | 缺陷标注 | 下载方式 | 本地路径 |
|--------|------|------|----------|----------|----------|----------|
| **MPID** | Zenodo #14604384 | 646张 | YOLO TXT | ❌ 无 | Zenodo直下 | `Yolo算法比赛/data/processed/mpid_composite/` |
| **CPLID** | 国家电网 | 848张 | VOC XML→YOLO | ✅ 有 | GitHub | `D:/AICompData/CPLID/` |
| **InsPLAD** | Mendeley Data | 10,607张 | COCO JSON→YOLO | ✅ 有 | Mendeley | `D:/AICompData/InsPLAD/` |
| **IDID V1.1** | EPRI/IEEE DataPort | ~700张 | YOLO | ✅ 有 | IEEE DataPort | 待下载 |
| **TLID** | 华北电力大学 | 未公开 | VOC | ✅ 有 | 邮件申请 | 待申请 |

### 2.2 数据集下载脚本

```python
# scripts/download_datasets.py
# 一键下载所有可公开获取的数据集
# 用法：python scripts/download_datasets.py --datasets cplid insplad idid
```

### 2.3 数据集融合规范

**类别映射表**（Unified4S 标准）：

| 原始类别 | 来源 | Unified4S ID | 说明 |
|----------|------|-------------|------|
| insulator/normal | CPLID+MPID+InsPLAD | 0 | 正常绝缘子 |
| defect | CPLID+InsPLAD | 1 | 绝缘子缺陷 |
| broken_shackle | InsPLAD | 2 | 破损卸扣 |
| corrosion | InsPLAD | 3 | 锈蚀 |
| flash_burn | InsPLAD | 4 | 灼伤 |

**数据目录结构**：
```
D:/AICompData/
├── Unified4S/           # 融合后的统一数据集
│   ├── images/
│   │   ├── train/       # 拼接所有来源的训练图
│   │   └── val/
│   ├── labels/
│   │   ├── train/       # 统一类别的YOLO标签
│   │   └── val/
│   └── data.yaml        # nc=5, names映射
├── CPLID/               # 原始CPLID
├── InsPLAD/             # 原始InsPLAD
└── Papers/              # 相关论文PDF
```

---

## 三、训练子工作流

### 3.1 训练配置标准

```yaml
# 推荐训练配置
model: yolo12n.pt        # 预训练权重
data: D:/AICompData/Unified4S/data.yaml
epochs: 100
imgsz: 640
batch: 16                # RTX 5070 Ti 12GB
device: 0
workers: 8
patience: 20
seed: 42
```

### 3.2 训练结果记录格式

```
| 实验 | 数据集 | 类别数 | Epoch | mAP50 | mAP50-95 | 推理速度 | 模型大小 |
|------|--------|--------|-------|-------|----------|----------|----------|
| exp_01 | MPID | 1 | 100 | 96.6% | 74.1% | 1.8ms | 5.3MB |
| exp_02 | Unified4S | 5 | 80 | ? | ? | ? | ? |
```

### 3.3 消融实验矩阵

| 实验 | 模型 | 数据增强 | 额外模块 | 目的 |
|------|------|----------|----------|------|
| baseline | YOLO12n | 默认 | 无 | 基线 |
| +aug | YOLO12n | Mosaic+MixUp+CopyPaste | 无 | 数据增强效果 |
| +cbam | YOLO12n | 默认 | CBAM注意力 | 注意力效果 |
| +fusion | YOLO12n | 默认 | 无 | 多源数据融合效果 |

---

## 四、论文引用库

### 4.1 关键论文

| # | 简称 | 方法 | 数据集 | 年份 | 引用场景 |
|---|------|------|--------|------|----------|
| 1 | APF-YOLOV8 | 自适应池化融合 | MPID | 2025 | 数据集来源 |
| 2 | ES-YOLO | 增强小目标YOLOv8s | CPLID+自采 | 2025 | 小目标检测方法 |
| 3 | EMA-YOLOv8 | EMA+BiFPN+C2f | CPLID+SFID | 2025 | 融合模块设计 |
| 4 | Focaler-Wise-SIoU | 自适应IoU损失 | CPLID+SFID | 2025 | 损失函数改进 |
| 5 | NWD-RKA | 归一化Wasserstein | DroneVehicle | 2025 | 小目标检测 |
| 6 | UF-YOLOv8 | 超分辨率融合 | CPLID | 2025 | 小目标增强 |
| 7 | DFM-YOLOv8s | 多尺度融合 | CPLID | 2025 | 多尺度检测 |
| 8 | IDPC-YOLO | 动态卷积 | CPLID | 2025 | 轻量化 |
| 9 | PC-YOLO | 渐进式压缩 | CPLID | 2025 | 模型压缩 |
| 10 | LWD-YOLO | 轻量级小目标 | CPLID+SFID | 2025 | 轻量化 |

### 4.2 可复用方法（按优先级）

1. **BiFPN（加权双向特征金字塔）** → 替换 YOLO12 的 FPN
2. **EMA 注意力模块** → 嵌入 backbone
3. **CIoU/EIoU/SIoU 损失** → 替换默认损失
4. **Mosaic + MixUp + CopyPaste** → 数据增强
5. **INT8 量化** → 模型压缩（已完成：5.3MB→3.0MB）

---

## 五、论文写作工作流

### 5.1 论文结构

```
1. 引言 — 电力巡检背景 + 绝缘子检测意义 + 现有方法不足 + 本文贡献
2. 相关工作 — 绝缘子检测综述 + YOLO系列演进 + 注意力机制 + 数据集
3. 方法 — 模型架构 + 改进模块 + 训练策略
4. 实验 — 数据集 + 评价指标 + 实验结果 + 消融实验 + 可视化
5. 结论 — 总结 + 未来工作
```

### 5.2 论文产出路径

- `Yolo算法比赛/outputs/论文/` — 论文 Markdown 源文件
- `Yolo算法比赛/outputs/论文/参考文献.bib` — BibTeX 引用库
- 论文导出：md → docx（python-docx）→ PDF（fpdf2/weasyprint）

### 5.3 关键实验结果来源

- 训练日志：`Yolo算法比赛/outputs/train/{experiment}/results.csv`
- PR 曲线：`Yolo算法比赛/outputs/train/{experiment}/PR_curve.png`
- 混淆矩阵：`Yolo算法比赛/outputs/train/{experiment}/confusion_matrix.png`
- 推理结果：`Yolo算法比赛/outputs/predict/`

---

## 六、竞赛 SOP 速查

### 6.1 常规赛道 6 单元

| 单元 | 内容 | 我们的状态 | 关键文件 |
|------|------|-----------|----------|
| 1. 硬件连接 | 摄像头+边缘设备接线 | ⏳ 等硬件 | 实操SOP/01_硬件连接与配置SOP.md |
| 2. 环境搭建 | Python+依赖+CUDA | ✅ 已完成 | requirements.txt |
| 3. 数据准备 | 现场标注+格式转换 | ✅ 有经验 | scripts/prepare_dataset.py |
| 4. 模型训练 | YOLO训练+调参 | ✅ mAP50=96.6% | outputs/train/ |
| 5. 模型导出 | PT→ONNX→量化 | ✅ INT8 3.0MB | weights/best_int8.onnx |
| 6. 模型部署 | 边缘设备推理 | ⏳ 等硬件 | 边缘部署实施方案.md |

### 6.2 理论 4 模块

- 电力设施巡检 → `outputs/理论笔记/`
- 数字图像处理 → `outputs/理论笔记/`
- 计算机视觉 → `outputs/理论笔记/`
- 人工智能算法 → `outputs/理论笔记/`
- 模拟题库 100 题 → `outputs/理论笔记/综合模拟题100题.md`

---

## 七、踩坑记录（来自本工作区实战）

| # | 教训 | 根因 | 正确做法 |
|---|------|------|----------|
| 1 | PyTorch CPU 版无法训练 | pip install torch 默认装 CPU | `pip install torch --index-url https://download.pytorch.org/whl/cu128` |
| 2 | RTX 5070 Ti 是 sm_120 架构 | 旧 PyTorch 不支持 Blackwell | 需要 PyTorch 2.11+cu128 |
| 3 | Git LFS 未安装导致图片为空 | InsPLAD 用 LFS 存储大文件 | `git lfs install && git lfs pull` |
| 4 | VOC→YOLO 类别 ID 不一致 | 不同数据集 class name 不同 | 统一类别映射表 |
| 5 | 整数截断导致 bbox 坐标全 0 | `int(cx)` 当 cx<1 时截断为 0 | 用 round 或直接保留浮点 |
| 6 | mAP50=96.6% 可能是假象 | 单类别+小验证集+简单任务 | 加多类别数据验证 |
| 7 | Bash heredoc 中文路径必炸 | MSYS2 编码问题 | Python 脚本处理中文路径 |

---

## 八、执行决策树

```
收到任务
  ├─ 搜索/下载数据集 → §二 数据集管理
  ├─ 数据预处理/转换 → §二.3 融合规范
  ├─ 训练/优化模型 → §三 训练工作流
  ├─ 写论文/整理结果 → §五 论文工作流
  ├─ 准备竞赛/复习 → §六 竞赛 SOP
  ├─ 查方法/引论文 → §四 论文引用库
  └─ 排查问题/避坑 → §七 踩坑记录
```

---

## 九、依赖关系

- 训练依赖：`ultralytics>=8.4.0`, `torch>=2.11.0+cu128`
- 数据处理：`opencv-python`, `Pillow`, `pyyaml`
- 论文写作：`python-docx`, `fpdf2`
- 模型导出：`onnx`, `onnxruntime`

---

## 版本记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-06-12 | v1.0 | 初始创建：数据集管理+训练+论文+竞赛SOP+踩坑记录 |
