from fastapi import APIRouter, HTTPException
from app.services.session_service import session_service

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("")
def create_session():
    session = session_service.create_session()
    return {"session_id": session.session_id}

@router.get("/{session_id}")
def get_history(session_id: str):
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session

@router.delete("/{session_id}")
def delete_session(session_id: str):
    removed = session_service.delete_session(session_id)
    if not removed:
        raise HTTPException(404, "Session not found")
    return {"message": "Session deleted"}
