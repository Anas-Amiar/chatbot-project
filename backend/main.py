from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

OLLAMA_URL = "http://ollama:11434/api/chat"
MODEL = "llama3"


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest):
    messages = req.history + [{"role": "user", "content": req.message}]

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            OLLAMA_URL,
            json={"model": MODEL, "messages": messages, "stream": False},
        )
        response.raise_for_status()
        data = response.json()

    reply = data["message"]["content"]
    return {"reply": reply}
