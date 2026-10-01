from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import GreenCredit, User
from ..schemas import CreditCreate

router = APIRouter(prefix="/api/credits", tags=["credits"])

@router.get("/{user_id}")
def history(user_id:int, db:Session=Depends(get_db)):
    return db.query(GreenCredit).filter(GreenCredit.user_id==user_id).order_by(GreenCredit.created_at.desc()).all()

@router.post("")
def add_credit(p:CreditCreate, db:Session=Depends(get_db)):
    u=db.query(User).filter(User.id==p.user_id).first()
    if not u: return {"error":"user not found"}
    item=GreenCredit(**p.model_dump())
    u.green_credits += p.points
    db.add(item); db.commit(); db.refresh(item)
    return item
