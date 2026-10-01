# Optional YOLOv8 training starter.
# pip install ultralytics
from ultralytics import YOLO

model = YOLO("yolov8n-cls.pt")
model.train(
    data="ml/dataset",
    epochs=30,
    imgsz=224,
    batch=16,
    project="ml/runs",
    name="greentrace_waste"
)
