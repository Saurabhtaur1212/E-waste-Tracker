from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(String(40), default="student")
    department = Column(String(120), default="General")
    green_credits = Column(Integer, default=0)

class WasteEvent(Base):
    __tablename__ = "waste_events"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    item_name = Column(String(200), nullable=False)
    category = Column(String(80), nullable=False)
    confidence = Column(Float, nullable=False)
    bin_type = Column(String(80), nullable=False)
    credits = Column(Integer, default=0)
    location = Column(String(200), default="Campus")
    created_at = Column(DateTime, default=datetime.utcnow)

class EWasteAsset(Base):
    __tablename__ = "ewaste_assets"
    id = Column(Integer, primary_key=True)
    asset_id = Column(String(100), unique=True, nullable=False)
    device_type = Column(String(100), nullable=False)
    serial_number = Column(String(150))
    institution = Column(String(180), nullable=False)
    department = Column(String(120), nullable=False)
    condition = Column(String(100), default="Deprecated")
    status = Column(String(80), default="Decommissioned")
    recycler = Column(String(200))
    recycler_verified = Column(Boolean, default=False)
    certificate_id = Column(String(150))
    notes = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EWasteLifecycle(Base):
    __tablename__ = "ewaste_lifecycle"
    id = Column(Integer, primary_key=True)
    asset_id = Column(String(100), nullable=False)
    previous_status = Column(String(80))
    new_status = Column(String(80), nullable=False)
    actor = Column(String(150), nullable=False)
    location = Column(String(200))
    remarks = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Recycler(Base):
    __tablename__ = "recyclers"
    id = Column(Integer, primary_key=True)
    name = Column(String(180), nullable=False)
    license_number = Column(String(120))
    verified = Column(Boolean, default=False)
    contact = Column(String(180))

class Bin(Base):
    __tablename__ = "bins"
    id = Column(Integer, primary_key=True)
    bin_id = Column(String(100), unique=True, nullable=False)
    location = Column(String(200), nullable=False)
    waste_type = Column(String(80), nullable=False)
    fill_level = Column(Float, default=0)
    temperature = Column(Float, default=28)
    battery = Column(Float, default=95)
    latitude = Column(Float, default=16.705)
    longitude = Column(Float, default=74.243)
    status = Column(String(60), default="Normal")
    last_collection = Column(DateTime)

class CollectionTask(Base):
    __tablename__ = "collection_tasks"
    id = Column(Integer, primary_key=True)
    bin_id = Column(String(100), nullable=False)
    priority = Column(String(40), default="Medium")
    assigned_to = Column(String(150), default="Unassigned")
    status = Column(String(50), default="Pending")
    eta_minutes = Column(Integer, default=30)
    created_at = Column(DateTime, default=datetime.utcnow)

class GreenCredit(Base):
    __tablename__ = "green_credits"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String(180), nullable=False)
    points = Column(Integer, nullable=False)
    verified = Column(Boolean, default=True)
    reference = Column(String(180))
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(30), default="info")
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    actor = Column(String(200), nullable=False)
    action = Column(String(250), nullable=False)
    reference = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
