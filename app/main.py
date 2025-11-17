from fastapi import FastAPI
from app.api.v1.routes.sessions import router as sessions_router
from app.api.v1.routes.chat import router as chat_router

app = FastAPI(title="Ollama Chat Wrapper")

app.include_router(sessions_router)
app.include_router(chat_router)
