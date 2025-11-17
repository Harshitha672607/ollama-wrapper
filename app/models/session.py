from pydantic import BaseModel
from typing import List
from .message import Message

class Session(BaseModel):
    session_id: str
    messages: List[Message] = []
