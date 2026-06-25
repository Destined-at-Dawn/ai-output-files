"""
数据集融合脚本：将 CPLID + MPID + InsPLAD 统一为 Unified4S 格式
用法：python prepare_unified4s.py
输出：D:/AICompData/Unified4S/
"""
import os
import shutil
import json
import random
from pathlib import Path
from collections import defaultdict

random.seed(42)

# ===== 配置 =====
BASE = Path("D:/AICompData")
UNIFIED = BASE / "Unified4S"
CPLID_YOLO = BASE / "CPLID" / "YOLO_format"
MPID = Path("${WORKSPACE_ROOT}/Yolo算法比赛/data/processed/mpid_composite")
INSPLAD = BASE / "InsPLAD-fault-classification-main"

CLASSES = {
    0: "insulator_normal",     # 正常绝缘子
    1: "insulator_defect",     # 缺陷绝缘子
}

VAL_RATIO = 0.15

# ===== 创建目录 =====
for split in ["train", "val"]:
    (UNIFIED / "images" / split).mkdir(parents=True, exist_ok=True)
    (UNIFIED / "labels" / split).mkdir(parents=True, exist_ok=True)

stats = defaultdict(int)
files = []  # (img_path, label_path, source)

# ===== 1. CPLID =====
print("\n=== Processing CPLID ===")
for split_src in ["train", "val"]:
    img_dir = CPLID_YOLO / "images" / split_src
    lbl_dir = CPLID_YOLO / "labels" / split_src
    if not img_dir.exists():
        print(f"  SKIP: {img_dir} not found")
        continue
    for lbl_file in lbl_dir.glob("*.txt"):
        img_file = img_dir / (lbl_file.stem + ".jpg")
        if not img_file.exists():
            continue
        files.append((img_file, lbl_file, "CPLID"))
        stats["CPLID"] += 1
print(f"  CPLID: {stats['CPLID']} samples")

# ===== 2. MPID =====
print("\n=== Processing MPID ===")
for split_src in ["train", "val"]:
    img_dir = MPID / "images" / split_src
    lbl_dir = MPID / "labels" / split_src
    if not img_dir.exists():
        print(f"  SKIP: {img_dir} not found")
        continue
    for lbl_file in lbl_dir.glob("*.txt"):
        img_file = img_dir / (lbl_file.stem + ".jpg")
        if not img_file.exists():
            # Try .png
            img_file = img_dir / (lbl_file.stem + ".png")
        if not img_file.exists():
            continue
        # MPID 只有 iso_poly (class 0)，直接保留
        files.append((img_file, lbl_file, "MPID"))
        stats["MPID"] += 1
print(f"  MPID: {stats['MPID']} samples")

# ===== 3. InsPLAD =====
print("\n=== Processing InsPLAD ===")
if INSPLAD.exists():
    for subdir in INSPLAD.iterdir():
        if not subdir.is_dir() or subdir.name.startswith('.'):
            continue
        # Check for images/labels structure
        img_dir = subdir / "images"
        lbl_dir = subdir / "labels"
        if not img_dir.exists():
            # Maybe flat structure - look for image files directly
            for img_file in subdir.glob("*.jpg"):
                lbl_file = lbl_dir / (img_file.stem + ".txt") if lbl_dir.exists() else None
                if lbl_file and lbl_file.exists():
                    files.append((img_file, lbl_file, "InsPLAD"))
                    stats["InsPLAD"] += 1
            continue
        for lbl_file in lbl_dir.glob("*.txt"):
            img_file = img_dir / (lbl_file.stem + ".jpg")
            if not img_file.exists():
                for ext in [".png", ".jpeg"]:
                    img_file = img_dir / (lbl_file.stem + ext)
                    if img_file.exists():
                        break
            if not img_file.exists():
                continue
            files.append((img_file, lbl_file, "InsPLAD"))
            stats["InsPLAD"] += 1
print(f"  InsPLAD: {stats['InsPLAD']} samples")

# ===== 分割 =====
print(f"\n=== Total: {len(files)} samples ===")
random.shuffle(files)
val_count = int(len(files) * VAL_RATIO)
val_files = files[:val_count]
train_files = files[val_count:]

print(f"  Train: {len(train_files)}")
print(f"  Val: {len(val_count)}")

# ===== 复制文件 =====
def copy_files(file_list, split):
    count = 0
    for img_path, lbl_path, source in file_list:
        # 复制图片
        dst_img = UNIFIED / "images" / split / img_path.name
        # 处理重名（加来源前缀）
        if dst_img.exists():
            dst_img = UNIFIED / "images" / split / f"{source}_{img_path.name}"
        shutil.copy2(img_path, dst_img)

        # 复制标签（内容保持不变，类别已统一）
        dst_lbl = UNIFIED / "labels" / split / (dst_img.stem + ".txt")
        shutil.copy2(lbl_path, dst_lbl)
        count += 1
    return count

train_count = copy_files(train_files, "train")
val_count_actual = copy_files(val_files, "val")

# ===== 写 data.yaml =====
yaml_content = f"""# Unified4S - 电力巡检绝缘子检测统一数据集
# 融合来源：CPLID（国家电网）+ MPID（Zenodo）+ InsPLAD（Mendeley）
# 创建日期：2026-06-12

path: D:/AICompData/Unified4S
train: images/train
val: images/val

nc: {len(CLASSES)}
names:
  0: insulator_normal
  1: insulator_defect

# 数据来源统计
# CPLID: {stats['CPLID']} samples (国家电网，CC BY 4.0)
# MPID: {stats['MPID']} samples (Zenodo #14604384，CC BY 4.0)
# InsPLAD: {stats['InsPLAD']} samples (Mendeley Data，CC BY 4.0)
"""

yaml_path = UNIFIED / "data.yaml"
with open(yaml_path, 'w', encoding='utf-8') as f:
    f.write(yaml_content)

# ===== 汇总 =====
print(f"\n{'='*50}")
print(f"Unified4S 数据集构建完成！")
print(f"  总样本：{len(files)}")
print(f"  训练集：{train_count}")
print(f"  验证集：{val_count_actual}")
print(f"  类别数：{len(CLASSES)}")
print(f"  输出路径：{UNIFIED}")
print(f"  配置文件：{yaml_path}")
print(f"\n来源统计：")
for src, cnt in stats.items():
    print(f"  {src}: {cnt}")
print(f"{'='*50}")
