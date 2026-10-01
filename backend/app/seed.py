from .database import Base, engine, SessionLocal
from .models import *
from .security import hash_password

def seed():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()

    if not db.query(User).count():
        db.add_all([
            User(name="Saurabh Demo",email="student@example.com",password=hash_password("student123"),role="student",department="CSE",green_credits=145),
            User(name="Campus Admin",email="admin@example.com",password=hash_password("admin123"),role="admin",department="Administration",green_credits=320),
            User(name="Collection Officer",email="collector@example.com",password=hash_password("collector123"),role="collector",department="Facilities",green_credits=80)
        ])

    if not db.query(Recycler).count():
        db.add_all([
            Recycler(name="GreenCycle Recycler",license_number="EPR-DEMO-001",verified=True,contact="recycler@greencycle.example"),
            Recycler(name="EcoRecover",license_number="EPR-DEMO-002",verified=True,contact="contact@ecorecover.example")
        ])

    if not db.query(EWasteAsset).count():
        db.add_all([
            EWasteAsset(asset_id="SGI-LAB-CPU-00231",device_type="Desktop CPU",serial_number="CPU-DEMO-231",institution="SGI",department="CSE",condition="Deprecated",status="Decommissioned"),
            EWasteAsset(asset_id="SGI-LAB-LAP-00118",device_type="Laptop",serial_number="LAP-DEMO-118",institution="SGI",department="IT Lab",condition="Damaged",status="Collected",recycler="GreenCycle Recycler"),
            EWasteAsset(asset_id="SGI-LAB-UPS-00071",device_type="UPS Battery",serial_number="UPS-DEMO-071",institution="SGI",department="Electrical Lab",condition="Expired",status="Recycled",recycler="EcoRecover",recycler_verified=True,certificate_id="CERT-2026-0071")
        ])
        db.add_all([
            EWasteLifecycle(asset_id="SGI-LAB-CPU-00231",new_status="Decommissioned",actor="admin",location="CSE"),
            EWasteLifecycle(asset_id="SGI-LAB-LAP-00118",new_status="Decommissioned",actor="admin",location="IT Lab"),
            EWasteLifecycle(asset_id="SGI-LAB-LAP-00118",previous_status="Decommissioned",new_status="Collected",actor="collector",location="IT Lab"),
            EWasteLifecycle(asset_id="SGI-LAB-UPS-00071",new_status="Decommissioned",actor="admin",location="Electrical Lab"),
            EWasteLifecycle(asset_id="SGI-LAB-UPS-00071",previous_status="Decommissioned",new_status="Collected",actor="collector",location="Electrical Lab"),
            EWasteLifecycle(asset_id="SGI-LAB-UPS-00071",previous_status="Collected",new_status="Sent to Recycler",actor="admin",location="EcoRecover"),
            EWasteLifecycle(asset_id="SGI-LAB-UPS-00071",previous_status="Sent to Recycler",new_status="Recycled",actor="EcoRecover",location="EcoRecover",remarks="Certificate verified")
        ])

    if not db.query(Bin).count():
        db.add_all([
            Bin(bin_id="BIN-CSE-01",location="CSE Block Ground Floor",waste_type="Dry Recyclable",fill_level=74,temperature=29,battery=93,latitude=16.7051,longitude=74.2431),
            Bin(bin_id="BIN-CSE-02",location="CSE Block First Floor",waste_type="Biodegradable",fill_level=48,temperature=28,battery=91,latitude=16.7054,longitude=74.2434),
            Bin(bin_id="BIN-LAB-03",location="Central Computer Lab",waste_type="E-Waste",fill_level=92,temperature=31,battery=84,latitude=16.7048,longitude=74.2428,status="Collection Required"),
            Bin(bin_id="BIN-CANTEEN-01",location="Main Canteen",waste_type="Biodegradable",fill_level=88,temperature=30,battery=89,latitude=16.7058,longitude=74.2424,status="Monitor")
        ])

    if not db.query(Notification).count():
        db.add_all([
            Notification(title="E-waste collection required",message="BIN-LAB-03 crossed 90% capacity.",severity="critical"),
            Notification(title="Recycler certificate pending",message="SGI-LAB-LAP-00118 needs certificate verification.",severity="warning"),
            Notification(title="Green milestone",message="Campus crossed 1,000 verified Green Credits.",severity="success")
        ])

    db.commit()
    db.close()
    print("GreenTrace seed complete.")

if __name__=="__main__":
    seed()
