# Local ChatBot 🤖 (Ollama + FastAPI + Streamlit)

A fully self-hosted chat application that runs a local LLM end to end — **no API keys, no
cloud, no data leaving your machine.** Three containers wired together with Docker Compose:
an Ollama model server, a FastAPI backend, and a Streamlit chat UI.

```
┌────────────┐      POST /chat       ┌────────────┐   /api/chat   ┌────────────┐
│  Streamlit │ ───────────────────►  │  FastAPI   │ ────────────► │   Ollama   │
│  UI :8501  │ ◄───────────────────  │  API :8000 │ ◄──────────── │ llama3     │
└────────────┘   {"reply": ...}      └────────────┘               │ :11434     │
   keeps chat history in session       stateless relay            └────────────┘
```

## Run it

```bash
git clone https://github.com/Anas-Amiar/chatbot-project.git
cd chatbot-project
docker compose up --build
```

Then pull the model once (first run only) and open the UI:

```bash
docker exec -it ollama ollama pull llama3
```

- Chat UI → http://localhost:8501
- API docs → http://localhost:8000/docs
- Health → http://localhost:8000/health

## How it works

- **`frontend/` (Streamlit)** — chat interface; keeps the running conversation in
  `st.session_state` and sends each turn (plus prior history) to the backend.
- **`backend/` (FastAPI)** — a thin, stateless relay: `POST /chat` takes `{message, history}`,
  forwards the full message list to Ollama's chat API, and returns the assistant reply.
- **`ollama` (model server)** — runs `llama3` locally; the model volume persists between
  restarts so you only pull once.

Because the whole stack is local, it's a good base for anything privacy-sensitive: swap
`llama3` for any Ollama model, or point the backend at a different provider by changing one
URL in `backend/main.py`.

## Stack

Python · FastAPI · Streamlit · Ollama (llama3) · Docker Compose · httpx
