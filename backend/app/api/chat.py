from typing import Literal
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from pydantic import ConfigDict
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.chatbot.orchestrator import chat
from app.database.session import get_db
from app.models.models import User

router = APIRouter(prefix="/api/chat", tags=["chat"])

class Msg(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=4000)

class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: list[Msg] = Field(default_factory=list)
    language: str = Field("en", max_length=5)

@router.post("")
async def send(body: ChatIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    return await chat(db, user, body.message, [m.model_dump() for m in body.history], body.language)
