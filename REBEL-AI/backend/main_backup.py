from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="REBEL AI")

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:3b"


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


@app.get("/")
def home():
    return {
        "name": "REBEL AI",
        "status": "Online",
        "engine": "Local Ollama"
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [
        {
            "role": "system",
            "content": (
                "You are REBEL AI, a private personal assistant. "
                "Be helpful, accurate and direct."
            )
        }
    ]

    messages.extend(request.history)
    messages.append({
        "role": "user",
        "content": request.message
    })

    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": False
                }
            )

            response.raise_for_status()
            result = response.json()

        return {
            "assistant": "REBEL AI",
            "reply": result["message"]["content"]
        }

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=503,
            detail=f"Local AI engine unavailable: {error}"
        )

app.mount(
    "/app",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)
