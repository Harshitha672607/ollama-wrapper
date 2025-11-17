def mock_insert_response(*args, **kwargs):
    return {"status": "ok"}

def mock_list_response_for_session(session_id):
    return {"data":[{"session_id": session_id, "system_prompt": "you are an agent", "model": "llama3", "created_at": "2025-01-01T00:00:00Z"}]}

def mock_list_response_for_messages(session_id):
    return {"data":[{"role":"system","session_id":session_id,"created_at":"2025-01-01T00:00:00Z","message_id":"m1","content":"you are an agent"}]}
