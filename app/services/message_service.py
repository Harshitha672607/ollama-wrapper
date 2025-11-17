import uuid
from app.core.pi_client import pi_client
from app.core.config import settings
from app.utils.timestamps import now_iso

class MessageService:

    async def create_message(self, session_id: str, role: str, content: str, token: str) -> str:
        message_id = str(uuid.uuid4())
        payload = {"data":[{"role": role, "session_id": session_id, "created_at": now_iso(), "message_id": message_id, "content": content}]}
        pi_client.insert_instance(settings.MESSAGES_SCHEMA_ID, payload, token)
        return message_id

    async def get_messages_by_session(self, session_id: str, token: str):
        resp = pi_client.list_instances(settings.MESSAGES_SCHEMA_ID, token)
        return [m for m in resp.get("data", []) if m.get("session_id") == session_id]
