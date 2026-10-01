from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import WasteEvent, EWasteAsset, Bin, CollectionTask

router=APIRouter(prefix="/api/reports",tags=["reports"])

@router.get("/overview")
def overview(db:Session=Depends(get_db)):
    return {
        "waste_events":db.query(WasteEvent).count(),
        "assets":db.query(EWasteAsset).count(),
        "recycled":db.query(EWasteAsset).filter(EWasteAsset.status=="Recycled").count(),
        "bins":db.query(Bin).count(),
        "pending_collection_tasks":db.query(CollectionTask).filter(CollectionTask.status=="Pending").count()
    }
