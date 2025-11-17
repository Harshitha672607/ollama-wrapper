import requests
import logging
from app.core.config import settings

logger = logging.getLogger("ollama_wrapper")

def call_ollama(model: str, messages: list) -> str:
    payload = {"model": model, "messages": messages}
    try:
        resp = requests.post(settings.OLLAMA_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # Handle multiple possible formats
        if isinstance(data, dict):
            if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                msg = data["choices"][0].get("message")
                if msg:
                    return msg.get("content", "")
            if "message" in data and isinstance(data["message"], dict):
                return data["message"].get("content", "")
            if "result" in data and isinstance(data["result"], str):
                return data["result"]
            if "content" in data and isinstance(data["content"], str):
                return data["content"]
        return resp.text
    except Exception as e:
        logger.exception("Ollama call failed: %s", e)
        raise
