from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI #type:ignore
from .agent import FinAgent
from .datastore import EncryptedStore, TransactionRepo
from .models import ChatRequest, ChatResponse

#wiring + dependency setup
data_path = Path("data/transactions.enc")
store = EncryptedStore(data_path)
repo = TransactionRepo(store)
agent = FinAgent
app = FastAPI(title="Financial Analyzer Agent")

@app.get("/")
def root() -> dict:
    return {
        "message": "Financial anaylyzer agent is running. POST to /chat with {'message': '...'}"
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Simple chat-like endpoint. In a real system, you'd likely:
    - Track user/session
    - Add authentication
    - Possibly expose a WebSocket for real-time streaming responses
    """
    return agent.handle_message(request.message)