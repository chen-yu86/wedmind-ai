from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    guests: int = 100
    budget: int = 100000
    style: str = "西式"

class UserCreate(BaseModel):
    username: str
    password: str