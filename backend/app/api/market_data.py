from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import current_user, require_roles
from app.database.session import get_db
from app.models.models import MarketPrice, User
from app.services.market_import import MarketImportError, import_prices

router = APIRouter(prefix="/api/market-data", tags=["market-data"])

@router.get("/prices")
def prices(commodity: str | None = None, state: str | None = None, limit: int = Query(100, le=500), db: Session = Depends(get_db), _: User = Depends(current_user)):
    q = select(MarketPrice).order_by(MarketPrice.arrival_date.desc()).limit(limit)
    if commodity: q = q.where(MarketPrice.commodity.ilike(f"%{commodity}%"))
    if state: q = q.where(MarketPrice.state.ilike(f"%{state}%"))
    return [{"commodity": p.commodity, "state": p.state, "district": p.district, "market": p.market, "modal_price": p.modal_price,
             "min_price": p.min_price, "max_price": p.max_price, "unit": "Rs/quintal", "arrival_date": p.arrival_date, "source": p.source, "data_type": "historical"} for p in db.scalars(q)]

@router.post("/import")
def run_import(commodity: str = Query(min_length=2, max_length=60), db: Session = Depends(get_db), _: User = Depends(require_roles("admin"))):
    try: return {"imported": import_prices(db, commodity)}
    except MarketImportError as e: raise HTTPException(502, str(e))
