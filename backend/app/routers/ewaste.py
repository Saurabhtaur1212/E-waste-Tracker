from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import EWasteAsset, EWasteLifecycle, AuditLog, Recycler
from ..schemas import AssetCreate, AssetStatus
from ..utils.qr_generator import create_qr

router = APIRouter(prefix="/api/assets", tags=["e-waste"])

@router.get("")
def assets(db: Session = Depends(get_db)):
    return db.query(EWasteAsset).order_by(EWasteAsset.id.desc()).all()

@router.post("")
def create_asset(p: AssetCreate, db: Session = Depends(get_db)):
    if db.query(EWasteAsset).filter(EWasteAsset.asset_id == p.asset_id).first():
        raise HTTPException(409, "Asset already exists")
    x = EWasteAsset(**p.model_dump())
    db.add(x)
    db.add(EWasteLifecycle(asset_id=p.asset_id, new_status="Decommissioned", actor="admin", location=p.department, remarks="Asset registered"))
    db.add(AuditLog(actor="admin", action="E-waste asset created", reference=p.asset_id))
    db.commit()
    db.refresh(x)
    try:
        create_qr(p.asset_id)
    except Exception:
        pass
    return x

@router.get("/{asset_id}")
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    x = db.query(EWasteAsset).filter(EWasteAsset.asset_id == asset_id).first()
    if not x:
        raise HTTPException(404, "Asset not found")
    lifecycle = db.query(EWasteLifecycle).filter(EWasteLifecycle.asset_id == asset_id).order_by(EWasteLifecycle.timestamp.asc()).all()
    return {"asset": x, "lifecycle": lifecycle}

@router.patch("/{asset_id}/status")
def update_status(asset_id: str, p: AssetStatus, db: Session = Depends(get_db)):
    x = db.query(EWasteAsset).filter(EWasteAsset.asset_id == asset_id).first()
    if not x:
        raise HTTPException(404, "Asset not found")
    previous = x.status
    x.status = p.status
    x.recycler = p.recycler or x.recycler
    x.certificate_id = p.certificate_id or x.certificate_id
    x.notes = p.notes or x.notes
    x.recycler_verified = p.recycler_verified
    db.add(EWasteLifecycle(
        asset_id=asset_id,
        previous_status=previous,
        new_status=p.status,
        actor=p.actor,
        location=p.location or x.department,
        remarks=p.notes
    ))
    db.add(AuditLog(actor=p.actor, action=f"Asset status changed {previous} -> {p.status}", reference=asset_id))
    db.commit()
    db.refresh(x)
    return x

@router.get("/recyclers/list")
def recyclers(db: Session = Depends(get_db)):
    return db.query(Recycler).filter(Recycler.verified == True).all()
