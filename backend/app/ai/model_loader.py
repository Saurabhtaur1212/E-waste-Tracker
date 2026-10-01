import os

_model = None

def get_model():
    global _model
    path = os.getenv("YOLO_MODEL_PATH", "./models/waste.pt")
    if _model is None and os.path.exists(path):
        try:
            from ultralytics import YOLO
            _model = YOLO(path)
        except Exception:
            _model = None
    return _model
