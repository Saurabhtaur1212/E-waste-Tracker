from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Notification

router=APIRouter(prefix="/api/notifications",tags=["notifications"])

@router.get("")
def all_notifications(db:Session=Depends(get_db)):
    return db.query(Notification).order_by(Notification.created_at.desc()).limit(50).all()
