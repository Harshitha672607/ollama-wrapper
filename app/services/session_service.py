from app.utils.id_generator import generate_session_id
from app.store.memory_store import store
from app.models.session import Session
from app.models.message import Message

class SessionService:

    def create_session(self):
        session_id = generate_session_id()
        session = Session(session_id=session_id, messages=[])
        store.create_session(session)
        return session

    def get_session(self, session_id):
        return store.get_session(session_id)

    def delete_session(self, session_id):
        return store.delete_session(session_id)

session_service = SessionService()
