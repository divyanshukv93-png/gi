from datetime import date, datetime, timezone
from sqlalchemy import Date, DateTime, UniqueConstraint, Text, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base

def now(): return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20))  # farmer | seller | buyer | admin
    language: Mapped[str] = mapped_column(String(5), default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Listing(Base):
    __tablename__ = "marketplace_listings"
    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    grain: Mapped[str] = mapped_column(String(40), index=True)
    quantity_tonnes: Mapped[float] = mapped_column(Float)
    price_per_quintal: Mapped[int] = mapped_column(Integer, index=True)
    location: Mapped[str] = mapped_column(String(120))
    certificate_source: Mapped[str | None] = mapped_column(String(20), nullable=True)  # ai_assessment | human_verified | lab_certified
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Inquiry(Base):
    __tablename__ = "buyer_inquiries"
    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("marketplace_listings.id"), index=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    message: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class MarketPrice(Base):
    __tablename__ = "market_prices"
    __table_args__ = (UniqueConstraint("commodity", "market", "arrival_date", name="uq_price"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    commodity: Mapped[str] = mapped_column(String(60), index=True)
    state: Mapped[str] = mapped_column(String(60), index=True)
    district: Mapped[str] = mapped_column(String(80))
    market: Mapped[str] = mapped_column(String(100))
    min_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    modal_price: Mapped[float] = mapped_column(Float)  # Rs per quintal
    arrival_date: Mapped[date] = mapped_column(Date, index=True)
    source: Mapped[str] = mapped_column(String(80), default="data.gov.in (AGMARKNET)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class DiseaseReport(Base):
    __tablename__ = "disease_reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    grain_type: Mapped[str] = mapped_column(String(20))
    mode: Mapped[str] = mapped_column(String(20))  # demo | trained
    predicted_class: Mapped[str | None] = mapped_column(String(60), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Certificate(Base):
    __tablename__ = "certificates"
    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("marketplace_listings.id"), index=True)
    issuer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    certificate_type: Mapped[str] = mapped_column(String(30), default="seller_declaration")
    status: Mapped[str] = mapped_column(String(20), default="issued")
    notes: Mapped[str] = mapped_column(Text, default="")
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("marketplace_listings.id"), index=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    quantity_tonnes: Mapped[float] = mapped_column(Float)
    agreed_price_per_quintal: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default="requested")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(String(100), index=True)
    location: Mapped[str] = mapped_column(String(120), default="")
    temperature_c: Mapped[float] = mapped_column(Float)
    humidity_pct: Mapped[float] = mapped_column(Float)
    grain_moisture_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(20), default="live")
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, index=True)
