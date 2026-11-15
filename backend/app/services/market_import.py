from datetime import datetime
import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.models import MarketPrice

class MarketImportError(Exception):
    pass

def _num(v):
    try: return float(v)
    except (TypeError, ValueError): return None

def import_prices(db: Session, commodity: str, limit: int = 100) -> int:
    if not settings.data_gov_api_key or not settings.market_resource_id:
        raise MarketImportError("DATA_GOV_API_KEY and MARKET_RESOURCE_ID are not set")
    try:
        r = httpx.get(f"https://api.data.gov.in/resource/{settings.market_resource_id}",
                      params={"api-key": settings.data_gov_api_key, "format": "json", "limit": limit, "filters[commodity]": commodity}, timeout=30)
        r.raise_for_status()
        records = r.json().get("records", [])
    except (httpx.HTTPError, ValueError) as e:
        raise MarketImportError(f"data.gov.in request failed: {e}")
    added = 0
    for rec in records:
        try: day = datetime.strptime(rec["arrival_date"], "%d/%m/%Y").date()
        except (KeyError, ValueError): continue
        modal = _num(rec.get("modal_price"))
        if modal is None: continue
        market, com = str(rec.get("market", ""))[:100], str(rec.get("commodity", commodity))[:60]
        if db.scalar(select(MarketPrice.id).where(MarketPrice.commodity == com, MarketPrice.market == market, MarketPrice.arrival_date == day)): continue
        db.add(MarketPrice(commodity=com, state=str(rec.get("state", ""))[:60], district=str(rec.get("district", ""))[:80], market=market,
                           min_price=_num(rec.get("min_price")), max_price=_num(rec.get("max_price")), modal_price=modal, arrival_date=day))
        added += 1
    db.commit()
    return added
