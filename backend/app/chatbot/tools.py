from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.models import Inquiry, Listing, MarketPrice, User

def _t(name, desc, props, req=()):
    return {"type": "function", "function": {"name": name, "description": desc, "parameters": {"type": "object", "properties": props, "required": list(req)}}}
S, I = {"type": "string"}, {"type": "integer"}
TOOLS = [
    _t("search_listings", "Search marketplace grain listings", {"grain": S, "max_price": I, "location": S}),
    _t("get_market_prices", "Latest imported mandi prices in Rs per quintal", {"commodity": S, "state": S}, ["commodity"]),
    _t("my_inquiries", "Buyer inquiries on the current seller's listings", {}),
]

def run_tool(name: str, args: dict, db: Session, user: User):
    if name == "search_listings":
        q = select(Listing).limit(10)
        if args.get("grain"): q = q.where(Listing.grain.ilike(str(args["grain"])))
        if args.get("location"): q = q.where(Listing.location.ilike(f"%{args['location']}%"))
        if isinstance(args.get("max_price"), int): q = q.where(Listing.price_per_quintal <= args["max_price"])
        return [{"id": l.id, "grain": l.grain, "tonnes": l.quantity_tonnes, "price_per_quintal": l.price_per_quintal, "location": l.location, "certificate": l.certificate_source or "none"} for l in db.scalars(q)]
    if name == "get_market_prices":
        q = select(MarketPrice).where(MarketPrice.commodity.ilike(f"%{args.get('commodity', '')}%")).order_by(MarketPrice.arrival_date.desc()).limit(10)
        if args.get("state"): q = q.where(MarketPrice.state.ilike(f"%{args['state']}%"))
        rows = [{"market": p.market, "state": p.state, "modal_price": p.modal_price, "date": str(p.arrival_date), "source": p.source} for p in db.scalars(q)]
        return rows or {"results": [], "note": "No imported price data for this query"}
    if name == "my_inquiries":
        if user.role not in ("seller", "farmer"): return {"error": "Not permitted for this role"}
        q = select(Inquiry).join(Listing, Listing.id == Inquiry.listing_id).where(Listing.seller_id == user.id).limit(10)
        return [{"listing_id": i.listing_id, "message": i.message} for i in db.scalars(q)]
    return {"error": "Unknown tool"}
