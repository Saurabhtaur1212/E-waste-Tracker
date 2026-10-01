from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class AssetCreate(BaseModel):
    asset_id: str
    device_type: str
    serial_number: Optional[str] = None
    institution: str
    department: str
    condition: str = "Deprecated"

class AssetStatus(BaseModel):
    status: str
    recycler: Optional[str] = None
    certificate_id: Optional[str] = None
    notes: Optional[str] = None
    recycler_verified: bool = False
    actor: str = "admin"
    location: Optional[str] = None

class Telemetry(BaseModel):
    fill_level: float
    temperature: float = 28
    battery: float = 95

class TaskCreate(BaseModel):
    bin_id: str
    priority: str = "High"
    assigned_to: str = "Collection Team"
    eta_minutes: int = 30

class CreditCreate(BaseModel):
    user_id: int
    action: str
    points: int
    reference: Optional[str] = None
