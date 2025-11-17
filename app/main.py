from fastapi import FastAPI
from app.api.v1.routes import sessions, messages, health
from app.core.logging import setup_logging

app = FastAPI(title="Ollama Wrapper API")

setup_logging()

app.include_router(health.router, prefix="/v1")
app.include_router(sessions.router, prefix="/v1")
app.include_router(messages.router, prefix="/v1")


@app.get("/", tags=["root"])
async def root():
    return {"status": "ok", "service": "ollama-wrapper-api"}
