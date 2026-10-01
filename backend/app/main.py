from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, waste, ewaste, bins, dashboard, credits, reports, notifications

Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="GreenTrace Pro API",
    description="AI Waste + E-Waste Lifecycle + Smart Bin + Green Credits platform",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

for router in [auth.router,waste.router,ewaste.router,bins.router,dashboard.router,credits.router,reports.router,notifications.router]:
    app.include_router(router)

@app.get("/")
def root():
    return {"project":"GreenTrace Pro","status":"online","version":"2.0.0"}

@app.get("/health")
def health():
    return {"status":"healthy"}
