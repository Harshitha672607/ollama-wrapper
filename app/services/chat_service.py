from app.store.memory_store import store
from app.core.ollama_client import ollama_client
from app.models.message import Message

class ChatService:

    async def send_message(self, session_id: str, user_input: str, model="llama3"):
        session = store.get_session(session_id)
        if not session:
            return None

        # Add user message
        session.messages.append(Message(role="user", content=user_input))

        # Prepare message list for Ollama
        msg_list = [msg.dict() for msg in session.messages]

        # Call Ollama
        assistant_reply = await ollama_client.chat(model=model, messages=msg_list)

        # Add assistant reply
        session.messages.append(Message(role="assistant", content=assistant_reply))

        store.save_session(session)
        return assistant_reply

chat_service = ChatService()
