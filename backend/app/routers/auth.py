from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import LoginRequest
from ..security import verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
def login(p: LoginRequest, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == p.email).first()
    if not u or not verify_password(p.password, u.password):
        raise HTTPException(401, "Invalid credentials")
    return {
        "id": u.id,
        "name": u.name,
        "role": u.role,
        "department": u.department,
        "green_credits": u.green_credits
    }
