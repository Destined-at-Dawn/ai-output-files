"""YOLO12n Merged_4Class training — workers=4, cache=disk, batch=16"""
import os
os.environ['YOLO_SKIP_CHECKS'] = '1'
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ultralytics import YOLO

print("=" * 50)
print("YOLO12n 4-class training — workers=4")
print("=" * 50)

model = YOLO("D:/AICompData/yolo12n.pt")

results = model.train(
    data="D:/AICompData/Merged_4Class/data.yaml",
    epochs=100,
    imgsz=640,
    batch=16,
    workers=4,
    cache='disk',
    device=0,
    project="D:/AICompData/runs",
    name="yolo12n_4class_w4",
    exist_ok=True,
    patience=20,
    optimizer='AdamW',
    lr0=0.001,
    verbose=True,
)

print(f"\nTraining complete!")
print(f"Best mAP50: {results.results_dict.get('metrics/mAP50(B)', 'N/A')}")
print(f"Best mAP50-95: {results.results_dict.get('metrics/mAP50-95(B)', 'N/A')}")
print(f"Weights: D:/AICompData/runs/yolo12n_4class_w4/weights/best.pt")
