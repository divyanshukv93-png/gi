from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.core.security import hash_password, make_token, verify_password
from app.database.session import get_db
from app.models.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Literal["farmer", "seller", "buyer"]  # admin accounts cannot self-register

class UserOut(BaseModel):
    id: int; email: str; role: str; language: str
    model_config = {"from_attributes": True}

@router.post("/register", response_model=UserOut, status_code=201)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == body.email.lower())):
        raise HTTPException(409, "Email already registered")
    user = User(email=body.email.lower(), hashed_password=hash_password(body.password), role=body.role)
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username.lower()))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Incorrect email or password")
    return {"access_token": make_token(user.id), "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user
