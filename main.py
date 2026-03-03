from fastapi import FastAPI
from pydantic import BaseModel
from planner import WeddingPlanner

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    budget: int = 100000

@app.post("/chat")
async def chat(req: ChatRequest):
    planner = WeddingPlanner(budget=req.budget)
    return planner.handle_message(req.message)