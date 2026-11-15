from typing import Literal
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import current_user, require_roles
from app.database.session import get_db
from fastapi import HTTPException
from app.models.models import Inquiry, Listing, User

router = APIRouter(prefix="/api/marketplace", tags=["marketplace"])

class ListingIn(BaseModel):
    grain: Literal["Wheat", "Rice", "Maize"]
    quantity_tonnes: float = Field(gt=0, le=100000)
    price_per_quintal: int = Field(gt=0, le=1000000)
    location: str = Field(min_length=2, max_length=120)

class ListingOut(ListingIn):
    id: int; seller_id: int; certificate_source: str | None
    model_config = {"from_attributes": True}

@router.get("/listings", response_model=list[ListingOut])
def list_listings(grain: str | None = None, max_price: int | None = None, location: str | None = None,
                  limit: int = Query(50, le=100), offset: int = 0,
                  db: Session = Depends(get_db), _: User = Depends(current_user)):
    q = select(Listing).order_by(Listing.created_at.desc()).limit(limit).offset(offset)
    if grain: q = q.where(Listing.grain == grain)
    if max_price: q = q.where(Listing.price_per_quintal <= max_price)
    if location: q = q.where(Listing.location.ilike(f"%{location}%"))
    return db.scalars(q).all()

@router.post("/listings", response_model=ListingOut, status_code=201)
def create_listing(body: ListingIn, db: Session = Depends(get_db), user: User = Depends(require_roles("seller", "farmer"))):
    item = Listing(**body.model_dump(), seller_id=user.id)
    db.add(item); db.commit(); db.refresh(item)
    return item

class InquiryIn(BaseModel):
    message: str = Field(min_length=1, max_length=1000)

class InquiryOut(InquiryIn):
    id: int; listing_id: int; buyer_id: int
    model_config = {"from_attributes": True}

@router.post("/listings/{listing_id}/inquiries", response_model=InquiryOut, status_code=201)
def send_inquiry(listing_id: int, body: InquiryIn, db: Session = Depends(get_db), user: User = Depends(require_roles("buyer"))):
    if not db.get(Listing, listing_id):
        raise HTTPException(404, "Listing not found")
    inq = Inquiry(listing_id=listing_id, buyer_id=user.id, message=body.message)
    db.add(inq); db.commit(); db.refresh(inq)
    return inq

@router.get("/inquiries", response_model=list[InquiryOut])
def my_inquiries(db: Session = Depends(get_db), user: User = Depends(require_roles("seller", "farmer"))):
    q = select(Inquiry).join(Listing, Listing.id == Inquiry.listing_id).where(Listing.seller_id == user.id).order_by(Inquiry.created_at.desc())
    return db.scalars(q).all()
