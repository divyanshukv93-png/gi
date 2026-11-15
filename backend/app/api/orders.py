from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.api.deps import current_user, require_roles
from app.database.session import get_db
from app.models.models import Listing, Order, User

router = APIRouter(prefix="/api/orders", tags=["orders"])
class OrderIn(BaseModel):
    listing_id: int
    quantity_tonnes: float = Field(gt=0)
class OrderStatus(BaseModel):
    status: Literal["accepted", "rejected", "completed", "cancelled"]

def out(o):
    return {"id":o.id,"listing_id":o.listing_id,"buyer_id":o.buyer_id,"quantity_tonnes":o.quantity_tonnes,"agreed_price_per_quintal":o.agreed_price_per_quintal,"status":o.status,"created_at":o.created_at}

@router.post("", status_code=201)
def create(body: OrderIn, db: Session=Depends(get_db), user: User=Depends(require_roles("buyer"))):
    listing=db.get(Listing, body.listing_id)
    if not listing: raise HTTPException(404,"Listing not found")
    reserved=db.scalar(select(func.coalesce(func.sum(Order.quantity_tonnes),0)).where(Order.listing_id==listing.id,Order.status.in_(["requested","accepted","completed"]))) or 0
    if body.quantity_tonnes + reserved > listing.quantity_tonnes: raise HTTPException(400,"Requested quantity exceeds available listed quantity")
    if listing.seller_id == user.id: raise HTTPException(400,"You cannot order your own listing")
    o=Order(listing_id=listing.id,buyer_id=user.id,quantity_tonnes=body.quantity_tonnes,agreed_price_per_quintal=listing.price_per_quintal)
    db.add(o); db.commit(); db.refresh(o); return out(o)

@router.get("")
def mine(db: Session=Depends(get_db), user: User=Depends(current_user)):
    if user.role in ("seller","farmer"):
        rows=db.scalars(select(Order).join(Listing).where(Listing.seller_id==user.id).order_by(Order.created_at.desc())).all()
    else: rows=db.scalars(select(Order).where(Order.buyer_id==user.id).order_by(Order.created_at.desc())).all()
    return [out(o) for o in rows]

@router.patch("/{order_id}/status")
def update(order_id:int, body:OrderStatus, db:Session=Depends(get_db), user:User=Depends(current_user)):
    o=db.get(Order,order_id)
    if not o: raise HTTPException(404,"Order not found")
    listing=db.get(Listing,o.listing_id)
    allowed=(user.role=="admin" or (user.id==listing.seller_id and body.status in ("accepted","rejected","completed")) or (user.id==o.buyer_id and body.status=="cancelled"))
    if not allowed: raise HTTPException(403,"Not permitted to change this order")
    valid=(o.status=="requested" and body.status in ("accepted","rejected","cancelled")) or (o.status=="accepted" and body.status=="completed")
    if not valid: raise HTTPException(409,"Invalid order status transition")
    o.status=body.status; db.commit(); db.refresh(o); return out(o)
