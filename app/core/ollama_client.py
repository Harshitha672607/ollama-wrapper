import httpx

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    async def chat(self, model: str, messages: list):
        payload = {
            "model": model,
            "messages": messages
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
            # Ollama streams; the final message usually holds content
            return data.get("message", {}).get("content", "")
        
ollama_client = OllamaClient()
