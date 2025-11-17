from pydantic import BaseModel
from typing import Literal

class CreateMessageRequest(BaseModel):
    session_id: str
    role: Literal["system", "user", "assistant"]
    content: str
