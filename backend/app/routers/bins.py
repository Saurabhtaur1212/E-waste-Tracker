from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Bin, CollectionTask, Notification, AuditLog
from ..schemas import Telemetry, TaskCreate

router = APIRouter(prefix="/api/bins", tags=["smart-bins"])

def status(fill):
    if fill >= 90: return "Collection Required"
    if fill >= 75: return "Monitor"
    return "Normal"

@router.get("")
def get_bins(db: Session = Depends(get_db)):
    return db.query(Bin).order_by(Bin.fill_level.desc()).all()

@router.patch("/{bin_id}/telemetry")
def telemetry(bin_id: str, p: Telemetry, db: Session = Depends(get_db)):
    b = db.query(Bin).filter(Bin.bin_id == bin_id).first()
    if not b: raise HTTPException(404, "Bin not found")
    b.fill_level = max(0, min(100, p.fill_level))
    b.temperature = p.temperature
    b.battery = max(0, min(100, p.battery))
    b.status = status(b.fill_level)
    if b.fill_level >= 90:
        db.add(Notification(
            title=f"Overflow risk: {b.bin_id}",
            message=f"{b.location} is at {b.fill_level}% capacity.",
            severity="critical"
        ))
    db.add(AuditLog(actor="iot", action="Bin telemetry updated", reference=bin_id))
    db.commit()
    db.refresh(b)
    return b

@router.get("/tasks")
def tasks(db: Session = Depends(get_db)):
    return db.query(CollectionTask).order_by(CollectionTask.id.desc()).all()

@router.post("/tasks")
def create_task(p: TaskCreate, db: Session = Depends(get_db)):
    task = CollectionTask(**p.model_dump())
    db.add(task)
    db.add(Notification(
        title="Collection task created",
        message=f"{p.bin_id} assigned to {p.assigned_to}.",
        severity="info"
    ))
    db.commit()
    db.refresh(task)
    return task
