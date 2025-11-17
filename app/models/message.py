from pydantic import BaseModel

class Message(BaseModel):
    role: str  # system | user | assistant
    content: str
