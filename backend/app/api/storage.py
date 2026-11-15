from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.api.deps import current_user
from app.models.models import User

router=APIRouter(prefix="/api/storage",tags=["storage"])
class StorageIn(BaseModel):
    temperature_c:float=Field(ge=-10,le=60)
    humidity_pct:float=Field(ge=0,le=100)
    grain_moisture_pct:float=Field(ge=0,le=40)
    grain_type:str=Field("Wheat",max_length=40)

@router.post("/risk-assessment")
def assess(body:StorageIn,_:User=Depends(current_user)):
    # Transparent rule-based screening only; deliberately not a shelf-life model.
    flags=[]; score=0
    if body.humidity_pct>=70: flags.append("Ambient humidity is high; inspect ventilation and condensation."); score+=2
    elif body.humidity_pct>=60: flags.append("Ambient humidity is elevated; monitor conditions."); score+=1
    if body.grain_moisture_pct>=14: flags.append("Grain moisture is elevated; verify with a calibrated moisture meter."); score+=3
    elif body.grain_moisture_pct>=12.5: flags.append("Check grain moisture against the applicable commodity and storage standard."); score+=1
    if body.temperature_c>=30: flags.append("Storage temperature is high; consider cooling and more frequent inspection."); score+=2
    elif body.temperature_c>=25: flags.append("Monitor temperature trends."); score+=1
    level="high" if score>=4 else "watch" if score>=2 else "lower"
    return {"assessment_type":"rule_based_screening","source":"calculated_from_user_inputs","risk_level":level,"risk_score":score,"flags":flags or ["No threshold flags from the supplied values."],"grain_type":body.grain_type,"inputs":body.model_dump(),"limitations":"Not a trained predictive model, food-safety determination, or estimate of remaining shelf life. Confirm with calibrated instruments and qualified inspection."}
