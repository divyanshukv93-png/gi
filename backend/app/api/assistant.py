from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.chatbot.orchestrator import chat
from app.database.session import get_db
from app.models.models import User
router=APIRouter(prefix="/api/assistant",tags=["assistant"])
class Ask(BaseModel):
    message:str=Field(min_length=1,max_length=2000)
    history:list[dict]=Field(default_factory=list)
    language:str=Field("en",max_length=5)
@router.post("")
async def ask(body:Ask,db:Session=Depends(get_db),user:User=Depends(current_user)):
    return await chat(db,user,body.message,body.history[-10:],body.language)
