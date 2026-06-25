# li-competition — 电力AI竞赛全流程 Skill

> 适用：2026年电力行业大学生电力AI视觉巡检竞赛（常规赛道）
> 创建：2026-06-12
> 版本：v1.0

---

## 一、竞赛信息速查

- **主办**：中国电力教育协会
- **承办**：上海电力大学 + 深圳市物新智能科技有限公司
- **时间**：2026年11月7-9日（报到11月6日）
- **报名截止**：2026年10月10日
- **赛道**：常规赛道（2人队）
- **地点**：上海电力大学

### 实操 6 单元
1. 硬件连接与配置
2. 开发环境搭建
3. 数据准备
4. 模型训练
5. 模型编译与可执行文件生成
6. 模型部署与集成

### 理论 4 模块
- 电力设施巡检
- 数字图像处理
- 计算机视觉技术
- 人工智能算法

---

## 二、数据集管理

### 2.1 已下载数据集

| 数据集 | 路径 | 规模 | 格式 | 类别 | 来源 |
|--------|------|------|------|------|------|
| MPID | `Yolo算法比赛/data/processed/mpid_composite/` | 646张 | YOLO TXT | iso_poly | Zenodo #14604384 |
| CPLID | `D:/电力数据集/CPLID_yolo/` | 848张 | YOLO TXT | insulator+defect | 国家电网/飞桨 |
| 合并数据集 | `Yolo算法比赛/data/processed/merged_mpid_cplid/` | ~1494张 | YOLO TXT | 2类 | MPID+CPLID |
| InsPLAD-faulty | `D:/电力数据集/InsPLAD-faulty/` | 10607张 | COCO JSON | 17类+缺陷 | Mendeley Data |
| TLID | 需邮件申请 | 30052张 | PASCAL VOC | 4类 | 华北电力大学 |

### 2.2 待获取数据集

| 数据集 | 获取方式 | 优先级 | 用途 |
|--------|----------|--------|------|
| TLID | 邮件申请 caughyhzd@foxmail.com | 高 | 多类别检测+跨域验证 |
| UPID | GitHub shenchuang86/UPID | 中 | 元数据集+论文支撑 |
| SFID | GitHub zhangzhengde0225/FINet | 中 | 缺陷分类 |
| IDID V1.1 | IEEE DataPort / Kaggle | 中 | 美国EPRI权威数据 |

### 2.3 数据集格式转换

#### VOC → YOLO（CPLID 已完成）
```python
# 核心逻辑：读 XML → class_id + normalize
for obj in root.findall('object'):
    cls = class_map[obj.find('name').text]  # 'insulator'→0, 'defect'→1
    xmlbox = obj.find('bndbox')
    bb = [float(xmlbox.find(x).text) for x in ['xmin','xmax','ymin','ymax']]
    # normalize to 0-1
    x_center = ((bb[0]+bb[1])/2) / img_w
    y_center = ((bb[2]+bb[3])/2) / img_h
    w = (bb[1]-bb[0]) / img_w
    h = (bb[3]-bb[2]) / img_h
```

#### COCO → YOLO（InsPLAD 需转换）
```python
# COCO bbox = [x,y,w,h] (pixels) → YOLO class cx cy w h (normalized)
```

---

## 三、模型训练 SOP

### 3.1 环境要求
- PyTorch: 2.11.0+cu128（需要 CUDA 版本！）
- ultralytics: 8.4.62+
- GPU: RTX 5070 Ti (12GB)
- Python: 需要 conda 环境或带 CUDA 的 pip

### 3.2 训练命令
```bash
# 单类别基线
yolo train data=data/processed/mpid_composite/data.yaml model=yolo12n.pt epochs=100 imgsz=640

# 多类别（合并数据集）
yolo train data=data/processed/merged_mpid_cplid/data.yaml model=yolo12n.pt epochs=150 imgsz=640 batch=16
```

### 3.3 关键指标记录模板
| 指标 | 值 | 口径 | 数据集 | 日期 |
|------|-----|------|--------|------|
| mAP@0.5 | — | 验证集 | — | — |
| mAP@0.5:0.95 | — | 验证集 | — | — |
| 推理速度 | — | GPU | — | — |
| 模型大小 | — | — | — | — |

### 3.4 导出
```bash
yolo export model=best.pt format=onnx opset=20
yolo export model=best.pt format=onnx int8=True data=data.yaml  # INT8量化
```

---

## 四、论文支撑素材

### 4.1 论文-数据集-方法速查表（10篇2026年论文）

| 论文 | 方法 | 数据集 | 发表 |
|------|------|--------|------|
| TE-YOLOv8 | 小波+纹理增强 | CPLID+自采 | Frontiers AI |
| RDA-YOLO | 旋转检测增强 | CPLID+自采 | PLOS ONE |
| FAEM-YOLO | 特征聚合+高效混合 | CPLID+自采 | AIMS Math |
| IDD-DETR | 可变形DETR | CPLID+自采 | Remote Sensing |
| INS-DETR | 混合编码器 | CPLID+自采 | Sensors |
| DSC-DETR | 动态稀疏 | 瓷/玻璃/复合绝缘子 | Adv. Eng. Informatics |
| POLD-YOLO | 高效检测 | 复合绝缘子 | Sensors |
| CWSP-YOLO | 跨层小波 | 混合缺陷数据集 | Scientific Reports |
| DETR-IS | 编码器-解码器增强 | CPLID+自采 | Electronics |
| YOLOv12 | 注意力+CNN | COCO | arXiv |

### 4.2 论文PDF下载位置
`outputs/references/papers/`

---

## 五、竞赛踩坑日志

### 5.1 环境踩坑
- **PyTorch CPU vs CUDA**：`pip install ultralytics` 可能只装 CPU 版。必须先确认 `torch.cuda.is_available()`
- **Git LFS**：大数据集（InsPLAD 等）用 LFS 存储，需安装 `git-lfs` 才能拉取实际数据
- **RTX 5070 Ti (Blackwell)**：需要 PyTorch 2.11+ 才支持 sm_120 架构

### 5.2 数据集踩坑
- **MPID 高 mAP 可能是假象**：单类别 + 小验证集 + 简单任务 → mAP50=96.6% 可能过拟合
- **CPLID 命名规则**：图片和标签命名不完全对应，需要自动匹配
- **UPID 不含原图**：只有元数据，需要从其他来源获取图片

### 5.3 竞赛策略踩坑
- **竞赛官方数据未知**：实操单元3"数据准备"可能是现场给数据+现场标注
- **不能只训练一个数据集**：需要展示多源数据融合能力

---

## 六、任务依赖图

```
数据集下载/转换 → 合并数据集 → 训练模型 → 量化导出 → 论文终稿
                                           ↓
                                    实操SOP → 硬件部署
```

---

## 七、关联文件索引

| 文件 | 路径 | 说明 |
|------|------|------|
| 竞赛通知OCR | `outputs/references/competition_notice_ocr.txt` | 8页原文 |
| 基线权重 | `Yolo算法比赛/outputs/train/yolo12_mpid-2/weights/best.pt` | mAP50=96.6% |
| 论文 | `Yolo算法比赛/outputs/论文/基于YOLO12的无人机电力巡检绝缘子检测方法.md` | 含量化章节 |
| 实操SOP | `outputs/实操SOP/` | 7份文档 |
| 理论笔记 | `outputs/理论笔记/` | 4模块+100题 |

---

## 迭代日志

| 日期 | 触发事件 | 原流程 | 发现的问题 | 更新内容 | 版本 |
|------|---------|--------|-----------|---------|------|
| 2026-06-12 | 用户要求建立竞赛 skill | 无 | 无统一的竞赛管理流程 | 初始创建：数据集管理+训练SOP+论文素材+踩坑日志 | v1.0 |
