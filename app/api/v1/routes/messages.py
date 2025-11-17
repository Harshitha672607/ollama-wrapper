from fastapi import APIRouter, Depends
from app.services.message_service import MessageService
from app.core.auth import require_bearer_token
from app.schemas.message_schema import CreateMessageRequest

router = APIRouter()
service = MessageService()

@router.post("/messages", tags=["messages"])
async def create_message(req: CreateMessageRequest, authorization: str = Depends(require_bearer_token)):
    message_id = await service.create_message(session_id=req.session_id, role=req.role, content=req.content, token=authorization)
    return {"message_id": message_id}

@router.get("/messages/session/{session_id}", tags=["messages"])
async def get_messages(session_id: str, authorization: str = Depends(require_bearer_token)):
    messages = await service.get_messages_by_session(session_id=session_id, token=authorization)
    return {"messages": messages}
