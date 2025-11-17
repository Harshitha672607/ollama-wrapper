import uuid
from app.core.pi_client import pi_client
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import NotFoundError
from app.utils.timestamps import now_iso
from app.services.utils import call_ollama

class SessionService:

    async def create_session(self, system_prompt: str, model: str, token: str) -> str:
        session_id = str(uuid.uuid4())
        created_at = now_iso()
        payload = {
            "data": [
                {
                    "last_updated": created_at,
                    "metadata": {},
                    "session_id": session_id,
                    "created_at": created_at,
                    "model": model,
                    "system_prompt": system_prompt,
                }
            ]
        }
        logger.info("Creating session %s", session_id)
        pi_client.insert_instance(settings.SESSIONS_SCHEMA_ID, payload, token)

        # Insert system message in messages table
        message_payload = {
            "data": [
                {
                    "role": "system",
                    "session_id": session_id,
                    "created_at": created_at,
                    "message_id": str(uuid.uuid4()),
                    "content": system_prompt,
                }
            ]
        }
        pi_client.insert_instance(settings.MESSAGES_SCHEMA_ID, message_payload, token)
        return session_id

    async def get_session_with_messages(self, session_id: str, token: str) -> dict:
        # Query session
        session_resp = pi_client.list_instances(settings.SESSIONS_SCHEMA_ID, token)
        session_data = [s for s in session_resp.get("data", []) if s.get("session_id") == session_id]
        if not session_data:
            raise NotFoundError()
        session_obj = session_data[0]

        # Query messages
        messages_resp = pi_client.list_instances(settings.MESSAGES_SCHEMA_ID, token)
        messages = [m for m in messages_resp.get("data", []) if m.get("session_id") == session_id]
        messages_sorted = sorted(messages, key=lambda m: m.get("created_at", ""))
        return {
            "session_id": session_id,
            "model": session_obj.get("model"),
            "system_prompt": session_obj.get("system_prompt"),
            "messages": messages_sorted,
        }

    async def delete_session(self, session_id: str, token: str):
        filter_payload = {"filter": {"session_id": session_id}}
        logger.info("Deleting messages for session %s", session_id)
        pi_client.delete_instances(settings.MESSAGES_SCHEMA_ID, filter_payload, token)
        logger.info("Deleting session %s", session_id)
        pi_client.delete_instances(settings.SESSIONS_SCHEMA_ID, filter_payload, token)

    async def chat(self, session_id: str, user_prompt: str, token: str) -> str:
        # Fetch session
        session_resp = pi_client.list_instances(settings.SESSIONS_SCHEMA_ID, token)
        session_data = [s for s in session_resp.get("data", []) if s.get("session_id") == session_id]
        if not session_data:
            raise NotFoundError()
        session_obj = session_data[0]
        model = session_obj.get("model")

        # Fetch messages
        messages_resp = pi_client.list_instances(settings.MESSAGES_SCHEMA_ID, token)
        messages = [m for m in messages_resp.get("data", []) if m.get("session_id") == session_id]
        messages_sorted = sorted(messages, key=lambda m: m.get("created_at", ""))

        # Build Ollama messages array
        ollama_messages = []
        system_msg = next((m for m in messages_sorted if m.get("role")=="system"), None)
        if system_msg:
            ollama_messages.append({"role": "system", "content": system_msg.get("content")})
        else:
            ollama_messages.append({"role": "system", "content": session_obj.get("system_prompt")})
        for m in messages_sorted:
            if m.get("role") != "system":
                ollama_messages.append({"role": m.get("role"), "content": m.get("content")})
        ollama_messages.append({"role": "user", "content": user_prompt})

        assistant_text = call_ollama(model=model, messages=ollama_messages)

        # Persist user and assistant messages
        created_at = now_iso()
        user_payload = {"data":[{"role":"user","session_id":session_id,"created_at":created_at,"message_id":str(uuid.uuid4()),"content":user_prompt}]}
        assistant_payload = {"data":[{"role":"assistant","session_id":session_id,"created_at":now_iso(),"message_id":str(uuid.uuid4()),"content":assistant_text}]}
        pi_client.insert_instance(settings.MESSAGES_SCHEMA_ID, user_payload, token)
        pi_client.insert_instance(settings.MESSAGES_SCHEMA_ID, assistant_payload, token)

        # Update session last_updated
        update_payload = {"primarykeyEnable": True, "data":{"session_id":session_id, "last_updated": now_iso()}}
        try:
            pi_client.update_instances(settings.SESSIONS_SCHEMA_ID, update_payload, token)
        except Exception:
            logger.warning("Failed to update session last_updated for %s", session_id)

        return assistant_text
