from fastapi import FastAPI
from pydantic import BaseModel
from logic import handle_message

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    budget: int = 100000

@app.post("/chat")
async def chat(req: ChatRequest):
    return handle_message(req.message, req.budget)