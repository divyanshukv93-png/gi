from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Literal
from sqlalchemy import select
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.api.deps import current_user, require_roles
from app.database.session import get_db
from app.models.models import Certificate, Listing, User

router=APIRouter(prefix="/api/certificates",tags=["certificates"])
class CertIn(BaseModel):
    listing_id:int
    certificate_type:Literal["seller_declaration"]="seller_declaration"
    notes:str=Field("",max_length=2000)

@router.post("",status_code=201)
def issue(body:CertIn,db:Session=Depends(get_db),user:User=Depends(require_roles("seller","farmer","admin"))):
    listing=db.get(Listing,body.listing_id)
    if not listing: raise HTTPException(404,"Listing not found")
    if user.role!="admin" and listing.seller_id!=user.id: raise HTTPException(403,"Only the listing owner or admin can issue a declaration")
    c=Certificate(listing_id=listing.id,issuer_id=user.id,certificate_type=body.certificate_type,notes=body.notes)
    db.add(c); db.commit(); db.refresh(c)
    return {"id":c.id,"listing_id":c.listing_id,"certificate_type":c.certificate_type,"status":c.status,"issued_at":c.issued_at,"important":"This is a seller declaration, not an independent laboratory certificate."}

@router.get("")
def list_mine(db:Session=Depends(get_db),user:User=Depends(current_user)):
    q=select(Certificate).order_by(Certificate.issued_at.desc())
    if user.role!="admin": q=q.where(Certificate.issuer_id==user.id)
    return [{"id":c.id,"listing_id":c.listing_id,"certificate_type":c.certificate_type,"status":c.status,"issued_at":c.issued_at,"notes":c.notes} for c in db.scalars(q)]

@router.get("/{certificate_id}/pdf")
def pdf(certificate_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    cert=db.get(Certificate,certificate_id)
    if not cert: raise HTTPException(404,"Certificate not found")
    listing=db.get(Listing,cert.listing_id)
    if user.role!="admin" and user.id not in (cert.issuer_id,listing.seller_id): raise HTTPException(403,"Not permitted")
    buf=BytesIO(); p=canvas.Canvas(buf,pagesize=A4); p.setTitle(f"Grain declaration {cert.id}")
    p.setFont("Helvetica-Bold",18); p.drawString(55,790,"GRAIN INTELLIGENCE")
    p.setFont("Helvetica-Bold",14); p.drawString(55,750,f"Quality record #{cert.id}")
    p.setFont("Helvetica",11)
    lines=[f"Grain: {listing.grain}",f"Quantity: {listing.quantity_tonnes} tonnes",f"Asking price: INR {listing.price_per_quintal:,} per quintal",f"Location: {listing.location}",f"Record type: {cert.certificate_type}",f"Issued: {cert.issued_at.isoformat()}",f"Notes: {cert.notes or 'None'}"]
    y=710
    for line in lines: p.drawString(55,y,line[:110]); y-=25
    p.setFont("Helvetica-Bold",10); p.drawString(55,500,"IMPORTANT DISCLAIMER")
    p.setFont("Helvetica",9)
    for i,line in enumerate(["This document records information entered in Grain Intelligence.","It is not proof of laboratory testing, regulatory compliance, or food safety.","A lab-certified result must be obtained from an accredited independent laboratory."]): p.drawString(55,480-i*16,line)
    p.showPage(); p.save(); buf.seek(0)
    return StreamingResponse(buf,media_type="application/pdf",headers={"Content-Disposition":f'attachment; filename="grain-record-{cert.id}.pdf"'})
