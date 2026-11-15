import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret-not-for-production-use-0123456789"
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import Base, engine
Base.metadata.create_all(bind=engine)

c = TestClient(app)

def token(email, role):
    c.post("/api/auth/register", json={"email": email, "password": "password123", "role": role})
    return {"Authorization": "Bearer " + c.post("/api/auth/login", data={"username": email, "password": "password123"}).json()["access_token"]}

def test_admin_cannot_self_register():
    assert c.post("/api/auth/register", json={"email": "a@x.com", "password": "password123", "role": "admin"}).status_code == 422

def test_buyer_cannot_create_listing_seller_can():
    body = {"grain": "Wheat", "quantity_tonnes": 5, "price_per_quintal": 2400, "location": "Hisar"}
    assert c.post("/api/marketplace/listings", json=body, headers=token("b@x.com", "buyer")).status_code == 403
    assert c.post("/api/marketplace/listings", json=body, headers=token("s@x.com", "seller")).status_code == 201

def test_requires_auth():
    assert c.get("/api/marketplace/listings").status_code == 401

def test_inquiry_flow():
    s, b = token("s2@x.com", "seller"), token("b2@x.com", "buyer")
    lid = c.post("/api/marketplace/listings", json={"grain": "Rice", "quantity_tonnes": 2, "price_per_quintal": 3300, "location": "Ludhiana"}, headers=s).json()["id"]
    assert c.post(f"/api/marketplace/listings/{lid}/inquiries", json={"message": "Interested"}, headers=s).status_code == 403
    assert c.post(f"/api/marketplace/listings/{lid}/inquiries", json={"message": "Interested"}, headers=b).status_code == 201
    assert len(c.get("/api/marketplace/inquiries", headers=s).json()) == 1
    assert c.get("/api/marketplace/inquiries", headers=token("s3@x.com", "seller")).json() == []

import cv2, numpy as np
from app.chatbot.tools import run_tool
from app.database.session import SessionLocal
from app.models.models import User

def test_disease_demo_never_fabricates():
    ok, buf = cv2.imencode(".png", np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8))
    r = c.post("/api/disease-detection/analyze", files={"file": ("g.png", buf.tobytes(), "image/png")}, data={"grain_type": "Wheat"}, headers=token("f@x.com", "farmer"))
    assert r.status_code == 200 and r.json()["prediction"] is None and r.json()["mode"] == "demo"

def test_non_image_rejected_and_buyer_blocked():
    h = token("f2@x.com", "farmer")
    assert c.post("/api/disease-detection/analyze", files={"file": ("a.txt", b"hi", "text/plain")}, headers=h).status_code == 415
    assert c.post("/api/disease-detection/analyze", files={"file": ("a.png", b"x", "image/png")}, headers=token("b3@x.com", "buyer")).status_code == 403

def test_market_tool_reports_no_data_and_prices_need_admin_import():
    with SessionLocal() as db:
        u = db.query(User).first()
        assert run_tool("get_market_prices", {"commodity": "Nonexistent"}, db, u)["results"] == []
    assert c.post("/api/market-data/import?commodity=Wheat", headers=token("s9@x.com", "seller")).status_code == 403

def test_order_lifecycle_and_inventory_limit():
    seller = token("order-seller@example.com", "seller")
    buyer = token("order-buyer@example.com", "buyer")
    listing = c.post("/api/marketplace/listings", json={"grain":"Wheat","quantity_tonnes":2,"price_per_quintal":2500,"location":"Karnal"}, headers=seller).json()
    created = c.post("/api/orders", json={"listing_id":listing["id"],"quantity_tonnes":1.5}, headers=buyer)
    assert created.status_code == 201
    assert c.post("/api/orders", json={"listing_id":listing["id"],"quantity_tonnes":1}, headers=buyer).status_code == 400
    oid=created.json()["id"]
    assert c.patch(f"/api/orders/{oid}/status", json={"status":"accepted"}, headers=seller).status_code == 200
    assert c.patch(f"/api/orders/{oid}/status", json={"status":"completed"}, headers=seller).status_code == 200

def test_seller_declaration_pdf_and_storage_screening():
    seller=token("cert-seller@example.com","seller")
    listing=c.post("/api/marketplace/listings",json={"grain":"Rice","quantity_tonnes":1,"price_per_quintal":3000,"location":"Amritsar"},headers=seller).json()
    cert=c.post("/api/certificates",json={"listing_id":listing["id"],"certificate_type":"seller_declaration","notes":"Seller supplied details"},headers=seller)
    assert cert.status_code==201
    pdf=c.get(f"/api/certificates/{cert.json()['id']}/pdf",headers=seller)
    assert pdf.status_code==200 and pdf.headers["content-type"]=="application/pdf"
    result=c.post("/api/storage/risk-assessment",json={"temperature_c":32,"humidity_pct":80,"grain_moisture_pct":15,"grain_type":"Rice"},headers=seller)
    assert result.status_code==200 and result.json()["risk_level"]=="high"
    assert "not a trained predictive model" in result.json()["limitations"]
