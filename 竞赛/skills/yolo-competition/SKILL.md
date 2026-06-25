# YOLO 竞赛全流程 Skill

> **版本**：v1.0 | **创建**：2026-06-12
> **适用场景**：电力 AI 视觉巡检竞赛（YOLO 绝缘子检测）全流程管理
> **触发词**：竞赛、YOLO、绝缘子、训练、数据集、CPLID、模型优化、边缘部署

---

## 一、Skill 概述

本 Skill 覆盖从数据集准备到竞赛现场的完整工作流，整合了：
- 多源公开数据集管理（MPID / CPLID / InsPLAD / TLID）
- YOLO12n 模型训练与优化
- 边缘部署方案
- 论文写作支撑
- 理论考试复习

**核心原则**：每个环节产出可验证的证据文件，不做无据声称。

---

## 二、数据集管理

### 2.1 当前可用数据集

| 数据集 | 路径 | 类别数 | 样本数 | 标签格式 | 来源权威性 |
|--------|------|--------|--------|----------|-----------|
| **MPID** | `D:\AICompData\datasets\mpid_composite` | 1（iso_poly） | 646 | YOLO TXT | ⭐⭐⭐ 学术 |
| **CPLID** | `D:\AICompData\datasets\cplid` | 2（insulator+defect） | 848 | VOC XML→YOLO | ⭐⭐⭐⭐⭐ 国网 |
| **合并4类** | `D:\AICompData\datasets\merged_4class` | 4（iso_poly/glass/ceramic/defect） | 2700 | YOLO TXT | ⭐⭐⭐⭐ |

### 2.2 数据集操作流程

**Step 1：下载新数据集**
```bash
# CPLID（已下载）
git clone https://github.com/InsulatorData/InsulatorDataSet.git D:/AICompData/datasets/cplid_raw

# InsPLAD（需 Git LFS）
git lfs install
git clone https://github.com/andreluizbvs/InsPLAD-few-shot.git D:/AICompData/datasets/InsPLAD
cd D:/AICompData/datasets/InsPLAD && git lfs pull

# TLID（需邮件申请）
# 邮件至 caughyhzd@foxmail.com，附全名+机构+用途
```

**Step 2：格式统一（→YOLO TXT）**
- VOC XML → YOLO：`voc2yolo.py`（已在 outputs/ 中）
- COCO JSON → YOLO：`coco2yolo.py`（需时编写）
- 关键：统一类别 ID 映射，保留 source 字段追溯

**Step 3：数据集合并**
```python
# 合并策略：按类别映射 + 过采样小类
# 当前最优配置：2x oversample（v2，mAP50=99.0%）
```

### 2.3 标签格式规范

```
# YOLO 格式：class_id x_center y_center width height（归一化 0~1）
# 4类映射：
0 iso_poly       # 复合绝缘子
1 iso_glass      # 玻璃绝缘子
2 iso_ceramic    # 瓷绝缘子
3 defect         # 缺陷
```

---

## 三、模型训练

### 3.1 训练环境

- **GPU**：RTX 5070 Ti Laptop（12GB VRAM，Blackwell sm_120）
- **PyTorch**：2.11.0+cu128
- **ultralytics**：8.4.62
- **Python**：3.14（venv 路径：`D:\AICompData\venv\Scripts\python.exe`）

### 3.2 训练历史（证据路径）

| 实验 | 配置 | mAP50 | mAP50-95 | 权重路径 |
|------|------|-------|----------|----------|
| mpid-2 | MPID 646, ep100, img640 | 96.6% | 74.1% | `Yolo算法比赛/outputs/train/yolo12_mpid-2/weights/best.pt` |
| cplid-2 | CPLID 848, ep100, img640 | 99.3% | 83.0% | `D:\AICompData\runs\yolo12n_cplid-2\weights\best.pt` |
| 4class | 合并2700, ep100, img640 | 86.3% | 59.3% | `D:\AICompData\runs\yolo12n_4class\weights\best.pt` |
| **4class_v2** | 合并2700 2x过采样, ep100, img640 | **99.0%** | **94.1%** | `D:\AICompData\runs\yolo12n_4class_v2\weights\best.pt` |
| enhanced_v3 | 合并+ECA/ELA注意力, ep100 | 98.2% | 89.5% | `D:\AICompData\runs\yolo12n_enhanced_v3-9\weights\best.pt` |

### 3.3 最优训练配置（v2）

```python
# 关键超参（从 args.yaml 提取）
model: yolo12n.pt       # 预训练权重
epochs: 100
imgsz: 640
batch: 16
lr0: 0.01
lrf: 0.01
optimizer: AdamW
patience: 50
augment: True           # Mosaic + MixUp + HSV
# 数据增强：2x oversample 小类
```

### 3.4 训练命令模板

```python
from ultralytics import YOLO

# 加载预训练模型
model = YOLO('yolo12n.pt')

# 训练
results = model.train(
    data='D:/AICompData/datasets/merged_4class/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='yolo12n_experiment_name',
    project='D:/AICompData/runs',
    exist_ok=True,
    patience=50,
    augment=True,
)
```

---

## 四、模型优化与部署

### 4.1 量化对比

| 版本 | 大小 | 压缩率 | 推理速度 |
|------|------|--------|----------|
| FP32 ONNX | 10.1 MB | — | 1.8 ms/图 |
| INT8 ONNX | 3.0 MB | 70.4% | 更快（待测） |

### 4.2 导出流程

```python
# FP32 ONNX
model = YOLO('best.pt')
model.export(format='onnx', opset=20)

# INT8 量化
from ultralytics import YOLO
model = YOLO('best.pt')
model.export(format='onnx', int8=True, data='data.yaml')
```

### 4.3 边缘部署方案

详见 `E:\ai产出文件\牛马\竞赛\竞赛\outputs\边缘部署实施方案.md`
- 平台A：树莓派 5 + Hailo-8（26 TOPS）
- 平台B：Jetson Orin Nano
- 平台C：竞赛指定硬件（待确认）

---

## 五、论文写作支撑

### 5.1 论文现状

- **初稿**：`Yolo算法比赛/outputs/论文/基于YOLO12的无人机电力巡检绝缘子检测方法.md`（346行）
- **待补充**：多源数据集实验（CPLID 合并结果）、边缘部署数据

### 5.2 关键论文参考（2026年最新）

| 论文 | 方法 | 指标 | 数据集 | DOI/来源 |
|------|------|------|--------|----------|
| NHWD-YOLOv8 (2025) | GSConv+BiFormer+MPDIoU | mAP@0.5=98.90% | CPLID | 10.1038/s41598-025-86926-2 |
| CAF-YOLO (2024) | C2fGhost+ASPP+SPPF | 参数仅2.12M | CPLID+自有 | 10.3390/s24186055 |
| ISF-YOLOv8 (2024) | FasterNet+SPPFCSPC+BiFormer | 47.9%↑参数↓14.7% | CPLID+INS | 10.3390/electronics13234741 |
| CSMB-YOLOv8 (2026) | SMMFusion+C2f-DSConv | mAP50提升 | CPLID | 10.3390/math13244076 |
| ITC-YOLO (2026) | DWT低频+CDA+WDloss | mAP@0.5=97.23% | CPLID | 10.3390/app15041841 |
| PatchEloss+RTMDet (2025) | PatchShuffle+EfficientViT | 各尺寸均衡 | CPLID | 10.3390/math13111824 |
| APF-YOLOV8 (2025) | ACmix+自适应+高效特征 | SOTA | MPID | PMC/PMC12125146 |
| DA-YOLO (2026) | 可变形注意力 | 精度↑2.04%推理↓0.9ms | CPLID | 10.3390/drones9050327 |
| M2-RTDETR (2026) | RTDETR变体 | mAP50=96.9% | CPLID | 10.3390/math13132210 |
| Multi-features+YOLOv9 (2025) | MSKA+FEM+C2f-MF | mAP@0.5=93.5% | CPLID | 10.3390/fractalfract9060368 |

**关键发现**：所有2026年论文都以 CPLID 为基准数据集。我们已下载 CPLID 并完成4类训练。

### 5.3 写作工具

- **RXtal**：专用论文写作工具（用户提到的）
- **pandoc**：MD→DOCX/PDF 转换
- **python-docx**：程序化生成 Word

---

## 六、理论考试（4 模块）

笔记路径：`E:\ai产出文件\牛马\竞赛\竞赛\outputs\理论笔记\`

| 模块 | 文件 | 状态 |
|------|------|------|
| 电力设施巡检 | `模块1_电力设施巡检.md` | ✅ |
| 数字图像处理 | `模块2_数字图像处理.md` | ✅ |
| 计算机视觉技术 | `模块3_计算机视觉技术.md` | ✅ |
| 人工智能算法 | `模块4_人工智能算法.md` | ✅ |
| 综合模拟题 | `综合模拟题100题.md` | ✅ |

---

## 七、竞赛日程

| 节点 | 日期 | 行动 |
|------|------|------|
| 报名截止 | 2026-10-10 | 必须在此之前完成报名 |
| 报到 | 2026-11-06 | 到达上海电力大学 |
| 竞赛 | 2026-11-07~09 | 理论考试 + 实操6单元 |

---

## 八、教训与最佳实践

### 踩坑记录

| 日期 | 坑 | 根因 | 修正 |
|------|-----|------|------|
| 2026-06-12 | Git LFS 未安装导致 InsPLAD 只有 14 张图 | 系统未预装 LFS | 安装 Git LFS 3.6.1 后 git lfs pull |
| 2026-06-12 | PyTorch CPU 版无法训练 | pip 默认装 CPU 版 | 需指定 cu128 索引 |
| 2026-06-12 | 4类合并后 mAP50 仅 86.3% | 类别不平衡（defect 仅 124） | 2x 过采样小类→99.0% |
| 2026-06-12 | Windows venv 中 CUDA 不可用 | venv 缺 CUDA 依赖 | 用 conda 环境或全局 pip |

### 最佳实践

1. **数据增强**：过采样比 Mosaic 更有效（2x oversample 提升 12.7%）
2. **多类训练**：先单类验证→再逐步增加类别
3. **模型选择**：YOLO12n 在小数据集上表现优异（5.3MB，96%+ mAP50）
4. **竞赛策略**：实操考核考流程完整性，不是比最高精度

---

## 九、工作流决策树

```
收到竞赛相关任务？
  ├─ 数据集相关 → §二 数据集管理
  ├─ 训练相关 → §三 模型训练
  ├─ 优化/部署 → §四 模型优化
  ├─ 论文相关 → §五 论文写作
  ├─ 理论考试 → §六 理论考试
  └─ 不确定 → 查 §九 决策树 或问项目状态
```

---

## 十、版本记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-06-12 | v1.0 | 初始创建：整合数据集管理+训练+优化+论文+理论全流程 |
