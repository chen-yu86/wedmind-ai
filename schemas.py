from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str