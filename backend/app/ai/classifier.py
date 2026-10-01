from io import BytesIO
from PIL import Image
from .model_loader import get_model

def normalize(label: str):
    x = label.lower().replace("-", "_").replace(" ", "_")
    if any(k in x for k in ["battery","pcb","electronic","ewaste","e_waste","hazard"]):
        return "Hazardous/E-Waste", "Red E-Waste Bin", 25
    if any(k in x for k in ["bio","food","organic"]):
        return "Biodegradable", "Green Bin", 5
    return "Dry Recyclable", "Blue Bin", 5

def classify(data: bytes):
    model = get_model()
    if model:
        image = Image.open(BytesIO(data)).convert("RGB")
        result = model.predict(image, verbose=False)[0]
        label, confidence = "unknown", 0.0
        if result.probs is not None:
            idx = int(result.probs.top1)
            confidence = float(result.probs.top1conf)
            label = str(result.names[idx])
        elif result.boxes is not None and len(result.boxes):
            idx = int(result.boxes.cls[0])
            confidence = float(result.boxes.conf[0])
            label = str(result.names[idx])
        category, bin_type, credits = normalize(label)
        return {
            "item_name": label,
            "category": category,
            "confidence": round(confidence, 3),
            "bin_type": bin_type,
            "credits": credits,
            "source": "YOLOv8"
        }

    # Functional demo fallback. This is intentionally labeled as demo data.
    img = Image.open(BytesIO(data)).convert("RGB").resize((1,1))
    r,g,b = img.getpixel((0,0))
    if r > 150 and b > 120:
        item, category, bin_type, credits = "Electronic item (demo)", "Hazardous/E-Waste", "Red E-Waste Bin", 25
    elif g > r and g > b:
        item, category, bin_type, credits = "Organic item (demo)", "Biodegradable", "Green Bin", 5
    else:
        item, category, bin_type, credits = "Plastic/Paper item (demo)", "Dry Recyclable", "Blue Bin", 5
    return {
        "item_name": item,
        "category": category,
        "confidence": 0.82,
        "bin_type": bin_type,
        "credits": credits,
        "source": "DEMO FALLBACK"
    }
