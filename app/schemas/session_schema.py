from pydantic import BaseModel

class CreateSessionRequest(BaseModel):
    system_prompt: str
    model: str

class CreateSessionResponse(BaseModel):
    session_id: str
