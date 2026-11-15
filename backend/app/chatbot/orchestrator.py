import json
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.chatbot.tools import TOOLS, run_tool
from app.core.config import settings
from app.models.models import User

SYSTEM = ("You are the Grain Intelligence assistant for farmers, sellers and buyers. For any listing, price or inquiry data you MUST call a tool. "
          "Never invent prices, quantities, sensor readings, inspection results or certificates. If a tool returns nothing, say so. "
          "AI assessments are not laboratory certifications.")

async def chat(db: Session, user: User, message: str, history: list[dict], language: str) -> dict:
    msgs = [{"role": "system", "content": f"{SYSTEM} Reply in the language with code '{language}'."}, *history[-10:], {"role": "user", "content": message}]
    used: list[str] = []
    async with httpx.AsyncClient(timeout=90) as c:
        for _ in range(3):
            try:
                r = await c.post(f"{settings.ollama_url}/api/chat", json={"model": settings.ollama_model, "messages": msgs, "tools": TOOLS, "stream": False})
                r.raise_for_status()
            except httpx.HTTPError:
                raise HTTPException(503, f"Ollama is not reachable or the model is missing. Start Ollama and run: ollama pull {settings.ollama_model}")
            m = r.json()["message"]
            calls = m.get("tool_calls")
            if not calls:
                return {"reply": m.get("content", ""), "provider": "ollama", "tools_used": used}
            msgs.append(m)
            for call in calls:
                fn = call["function"]; used.append(fn["name"])
                msgs.append({"role": "tool", "tool_name": fn["name"], "content": json.dumps(run_tool(fn["name"], fn.get("arguments") or {}, db, user), default=str)})
    return {"reply": "I could not complete that request. Please rephrase it.", "provider": "ollama", "tools_used": used}
