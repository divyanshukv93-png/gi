from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, chat, disease, environment, market_data, marketplace, orders, certificates, iot, storage, assistant
from app.core.config import settings
from app.database.session import engine
from app.models import models  # noqa: F401


app = FastAPI(title="Grain Intelligence API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins.split(","), allow_methods=["*"], allow_headers=["*"])
for r in (auth.router, marketplace.router, environment.router, chat.router, disease.router, market_data.router, orders.router, certificates.router, iot.router, storage.router, assistant.router):
    app.include_router(r)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "grain-intelligence-api"}

@app.get("/api/ready")
def readiness():
    from sqlalchemy import text
    try:
        with engine.connect() as conn: conn.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(503, "Database unavailable")
