from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import chat_service

router = APIRouter(prefix="/sessions", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/{session_id}/chat")
async def chat(session_id: str, req: ChatRequest):
    response = await chat_service.send_message(session_id, req.message)

    if response is None:
        raise HTTPException(404, "Session not found")

    return {"response": response}
