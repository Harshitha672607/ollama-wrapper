import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PI_BASE_URL: str = os.getenv("PI_BASE_URL", "https://ig.gov-cloud.ai/pi-entity-instances-service/v2.0")
    SESSIONS_SCHEMA_ID: str = os.getenv("SESSIONS_SCHEMA_ID", "691b1f9219be331b9bebe0a5")
    MESSAGES_SCHEMA_ID: str = os.getenv("MESSAGES_SCHEMA_ID", "691b217419be331b9bebe0a7")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
    TRANSACTION_ID: str = os.getenv("TRANSACTION_ID", "transactionID123")

settings = Settings()
