from typing import Dict
from app.models.session import Session

class MemoryStore:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def create_session(self, session: Session):
        self.sessions[session.session_id] = session

    def get_session(self, session_id: str):
        return self.sessions.get(session_id)

    def save_session(self, session: Session):
        self.sessions[session.session_id] = session

    def delete_session(self, session_id: str):
        return self.sessions.pop(session_id, None)

store = MemoryStore()
