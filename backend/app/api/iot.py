from datetime import datetime, timezone
import secrets
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.api.deps import current_user
from app.database.session import get_db
from app.models.models import SensorReading, User

router=APIRouter(prefix="/api/iot",tags=["iot"])
class ReadingIn(BaseModel):
    device_id:str=Field(min_length=2,max_length=100)
    location:str=Field("",max_length=120)
    temperature_c:float=Field(ge=-30,le=80)
    humidity_pct:float=Field(ge=0,le=100)
    grain_moisture_pct:float|None=Field(None,ge=0,le=100)
    recorded_at:datetime|None=None

@router.post("/readings",status_code=201)
def ingest(body:ReadingIn,x_device_token:str|None=Header(None),db:Session=Depends(get_db)):
    if not settings.iot_device_token or not x_device_token or not secrets.compare_digest(x_device_token,settings.iot_device_token): raise HTTPException(401,"Invalid device token")
    row=SensorReading(**body.model_dump(exclude={"recorded_at"}),recorded_at=body.recorded_at or datetime.now(timezone.utc),source="live")
    db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id,"device_id":row.device_id,"source":"live","recorded_at":row.recorded_at}

@router.get("/readings")
def readings(device_id:str|None=None,limit:int=Query(100,ge=1,le=500),db:Session=Depends(get_db),_:User=Depends(current_user)):
    q=select(SensorReading).order_by(SensorReading.recorded_at.desc()).limit(limit)
    if device_id:q=q.where(SensorReading.device_id==device_id)
    return [{"device_id":r.device_id,"location":r.location,"temperature_c":r.temperature_c,"humidity_pct":r.humidity_pct,"grain_moisture_pct":r.grain_moisture_pct,"source":r.source,"recorded_at":r.recorded_at} for r in db.scalars(q)]
