import math, time
from fastapi import APIRouter, Depends
from app.api.deps import current_user
from app.models.models import User

router = APIRouter(prefix="/api/environment", tags=["environment"])

@router.get("/simulated")
def simulated_reading(_: User = Depends(current_user)):
    """Simulated sensor reading. Always labelled; real MQTT readings will use source='live'."""
    t = time.time() / 600
    return {"source": "simulated", "temperature_c": round(26 + 3 * math.sin(t), 1),
            "humidity_pct": round(64 + 6 * math.cos(t / 2)), "grain_moisture_pct": round(13.2 + 0.3 * math.sin(t / 3), 1)}
