# 绝缘子检测相关 GitHub 仓库

> 更新：2026-06-12

---

## 数据集仓库

### 1. CPLID — 中国电力线路绝缘子数据集 ⭐⭐⭐⭐⭐

- **URL**：https://github.com/InsulatorData/InsulatorDataSet
- **来源**：国家电网
- **规模**：848 张（600 正常 + 248 缺陷）
- **格式**：PASCAL VOC (XML)
- **标注**：绝缘子边界框 + 缺陷区域
- **本地路径**：`D:\AICompData\datasets\cplid`
- **转换状态**：✅ 已转 YOLO TXT（1321 绝缘子框 + 248 缺陷框）

### 2. InsPLAD — 电力组件检测数据集 ⭐⭐⭐⭐

- **URL**：https://github.com/andreluizbvs/InsPLAD-few-shot
- **来源**：学术团队（IJRS 期刊论文配套）
- **规模**：10,607 张 1920×1080 无人机图像
- **格式**：COCO JSON
- **标注**：17 类电力组件 + 28,000+ 标注框
- **需 Git LFS**：是（已安装 LFS 3.6.1）
- **本地路径**：`D:\AICompData\datasets\InsPLAD`（待 git lfs pull）
- **注意**：数据量大（~10GB），下载需要时间

### 3. TLID — 输电线路绝缘子缺陷数据集

- **URL**：需邮件申请
- **来源**：华北电力大学 + 国网湖北 + 武汉大学
- **论文**：IEEE TII 2024（IEEE 工业信息学汇刊）
- **申请方式**：邮件至 caughyhzd@foxmail.com
- **内容**：目标检测 + 缺陷分类 + 航拍图像三元组
- **本地路径**：待申请

### 4. SFID — 小故障绝缘子数据集

- **URL**：https://github.com/InsulatorData/SmallFaultInsulatorDataset
- **特点**：专注微小缺陷检测
- **下载**：需自定义 API（hai_api），非直接下载
- **本地路径**：待下载

---

## 模型/框架仓库

### 5. YOLO12 官方实现

- **URL**：https://github.com/sunsmarterjie/yolov12
- **说明**：YOLO12 架构实现
- **本地已使用**：yolo12n.pt 预训练权重

### 6. ultralytics

- **URL**：https://github.com/ultralytics/ultralytics
- **说明**：YOLOv8~YOLO12 统一框架
- **版本**：8.4.62（本地安装）

### 7. MMDetection

- **URL**：https://github.com/open-mmlab/mmdetection
- **说明**：OpenMMLab 检测工具箱，支持 RTDETR 等 Transformer 检测器
- **适用**：如果要尝试 M2-RTDETR 等非 YOLO 方法

### 8. YOLOv9

- **URL**：https://github.com/WongKinYiu/yolov9
- **说明**：YOLOv9 架构（论文 #10 使用的基础框架）

---

## 工具仓库

### 9. labelImg（标注工具）

- **URL**：https://github.com/HumanSignal/labelImg
- **用途**：竞赛现场数据标注（实操单元 3）

### 10. CVAT（在线标注平台）

- **URL**：https://github.com/opencv/cvat
- **用途**：团队协作标注

---

## 下载状态追踪

| 仓库 | 本地路径 | 状态 | 备注 |
|------|----------|------|------|
| CPLID | `D:\AICompData\datasets\cplid` | ✅ 已下载+转换 | 848 张，YOLO 格式 |
| InsPLAD | `D:\AICompData\datasets\InsPLAD` | ⏳ 已克隆，待 LFS pull | 需执行 git lfs pull |
| TLID | — | ❌ 未申请 | 需邮件 |
| SFID | — | ❌ 未下载 | 需自定义 API |
