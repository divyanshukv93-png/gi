from typing import Literal
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import require_roles
from app.database.session import get_db
from app.ml.disease_detection.pipeline import analyze
from app.models.models import DiseaseReport, User

router = APIRouter(prefix="/api/disease-detection", tags=["disease-detection"])
MAX = 8 * 1024 * 1024
who = require_roles("farmer", "seller", "admin")

@router.post("/analyze")
async def run(file: UploadFile = File(...), grain_type: Literal["Wheat", "Rice", "Maize"] = Form("Wheat"), db: Session = Depends(get_db), user: User = Depends(who)):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(415, "Only JPEG or PNG images are accepted")
    data = await file.read(MAX + 1)
    if len(data) > MAX:
        raise HTTPException(413, "Image larger than 8 MB")
    try: res = analyze(data)
    except ValueError as e: raise HTTPException(422, str(e))
    rep = DiseaseReport(user_id=user.id, grain_type=grain_type, mode=res["mode"], notes=res["message"])
    db.add(rep); db.commit(); db.refresh(rep)
    return {"report_id": rep.id, "grain_type": grain_type, **res}

@router.get("/history")
def history(db: Session = Depends(get_db), user: User = Depends(who)):
    rows = db.scalars(select(DiseaseReport).where(DiseaseReport.user_id == user.id).order_by(DiseaseReport.created_at.desc()).limit(50))
    return [{"id": r.id, "grain_type": r.grain_type, "mode": r.mode, "predicted_class": r.predicted_class, "created_at": r.created_at} for r in rows]
