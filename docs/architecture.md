# Architecture

Camera / IoT
    |
    v
Next.js Frontend
    |
    v
FastAPI API
    |
    +--> AI Classifier (YOLOv8/TFLite-ready)
    +--> Waste Events
    +--> E-Waste Lifecycle
    +--> Smart Bin Telemetry
    +--> Collection Tasks
    +--> Green Credits
    +--> Analytics / Alerts
    |
    v
SQLite demo / PostgreSQL-Supabase production
