import qrcode
from pathlib import Path

def create_qr(asset_id: str, base_url: str = "http://localhost:3000/ewaste"):
    out = Path("uploads/assets")
    out.mkdir(parents=True, exist_ok=True)
    img = qrcode.make(f"{base_url}/{asset_id}")
    path = out / f"{asset_id}.png"
    img.save(path)
    return str(path)
