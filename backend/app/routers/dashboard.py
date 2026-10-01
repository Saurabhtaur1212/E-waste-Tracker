from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import *

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    cats = {a:b for a,b in db.query(WasteEvent.category, func.count(WasteEvent.id)).group_by(WasteEvent.category).all()}
    return {
        "waste_events": db.query(WasteEvent).count(),
        "e_waste_assets": db.query(EWasteAsset).count(),
        "recycled_assets": db.query(EWasteAsset).filter(EWasteAsset.status == "Recycled").count(),
        "active_bins": db.query(Bin).count(),
        "overflow_alerts": db.query(Bin).filter(Bin.fill_level >= 90).count(),
        "green_credits": db.query(func.sum(User.green_credits)).scalar() or 0,
        "by_category": cats,
        "segregation_rate": 87
    }

@router.get("/trends")
def trends():
    return [
        {"day":"Mon","waste":42,"recycled":21},
        {"day":"Tue","waste":58,"recycled":29},
        {"day":"Wed","waste":51,"recycled":34},
        {"day":"Thu","waste":73,"recycled":39},
        {"day":"Fri","waste":66,"recycled":43},
        {"day":"Sat","waste":48,"recycled":31},
        {"day":"Sun","waste":35,"recycled":22}
    ]

@router.get("/notifications")
def notifications(db: Session = Depends(get_db)):
    return db.query(Notification).order_by(Notification.created_at.desc()).limit(30).all()

@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    return [
        {"name":u.name, "department":u.department, "credits":u.green_credits}
        for u in db.query(User).order_by(User.green_credits.desc()).limit(10)
    ]

@router.get("/lifecycle/{asset_id}")
def lifecycle(asset_id: str, db: Session = Depends(get_db)):
    return db.query(EWasteLifecycle).filter(EWasteLifecycle.asset_id == asset_id).order_by(EWasteLifecycle.timestamp.asc()).all()
