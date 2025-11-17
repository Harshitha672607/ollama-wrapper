from fastapi import APIRouter, Depends, Header, HTTPException
from app.schemas.session_schema import CreateSessionRequest, CreateSessionResponse
from app.services.session_service import SessionService
from app.core.auth import require_bearer_token
from app.core.exceptions import NotFoundError

router = APIRouter()
service = SessionService()

@router.post("/session", response_model=CreateSessionResponse, tags=["sessions"])
async def create_session(req: CreateSessionRequest, authorization: str = Depends(require_bearer_token)):
    if not req.system_prompt or not req.model:
        raise HTTPException(status_code=400, detail="system_prompt and model are required")
    session_id = await service.create_session(system_prompt=req.system_prompt, model=req.model, token=authorization)
    return {"session_id": session_id}

@router.post("/session/{session_id}/chat", tags=["sessions"])
async def chat(session_id: str, body: dict, authorization: str = Depends(require_bearer_token)):
    user_prompt = body.get("user_prompt")
    if not user_prompt:
        raise HTTPException(status_code=400, detail="user_prompt is required")
    try:
        assistant_response = await service.chat(session_id=session_id, user_prompt=user_prompt, token=authorization)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="session not found")
    return {"assistant": assistant_response}

@router.get("/session/{session_id}", tags=["sessions"])
async def get_session(session_id: str, authorization: str = Depends(require_bearer_token)):
    try:
        session = await service.get_session_with_messages(session_id=session_id, token=authorization)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="session not found")
    return session

@router.delete("/session/{session_id}", tags=["sessions"])
async def delete_session(session_id: str, authorization: str = Depends(require_bearer_token)):
    try:
        await service.delete_session(session_id=session_id, token=authorization)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="session not found")
    return {"status": "deleted"}
