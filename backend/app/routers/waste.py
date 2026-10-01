from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import WasteEvent, User, GreenCredit, AuditLog
from ..ai.classifier import classify

router = APIRouter(prefix="/api/waste", tags=["waste"])

@router.post("/classify")
async def classify_waste(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = await file.read()
    if not data:
        raise HTTPException(400, "Empty image")
    result = classify(data)
    event = WasteEvent(
        user_id=1,
        item_name=result["item_name"],
        category=result["category"],
        confidence=result["confidence"],
        bin_type=result["bin_type"],
        credits=result["credits"],
        location="Campus"
    )
    db.add(event)
    user = db.query(User).filter(User.id == 1).first()
    if user:
        user.green_credits += result["credits"]
    db.add(GreenCredit(
        user_id=1,
        action=f"AI verified disposal: {result['category']}",
        points=result["credits"],
        reference=result["item_name"],
        verified=result["confidence"] >= .75
    ))
    db.add(AuditLog(actor="student", action="Waste classified", reference=result["item_name"]))
    db.commit()
    db.refresh(event)
    return {**result, "id": event.id, "manual_review": result["confidence"] < .75}

@router.get("")
def recent(db: Session = Depends(get_db)):
    return db.query(WasteEvent).order_by(WasteEvent.created_at.desc()).limit(100).all()
