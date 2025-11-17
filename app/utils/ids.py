import uuid

def new_session_id() -> str:
    return str(uuid.uuid4())

def new_message_id() -> str:
    return str(uuid.uuid4())
