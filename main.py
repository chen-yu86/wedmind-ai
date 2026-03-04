from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import ChatHistory
from schemas import ChatRequest, ChatResponse, TokenResponse
from auth import create_access_token, verify_token

Base.metadata.create_all(bind=engine)

app = FastAPI(title="WedMind Backend Portfolio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/token", response_model=TokenResponse)
def login(username: str, password: str):
    if username == "admin" and password == "123456":
        token = create_access_token({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

def get_current_user(token: str = Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest,
         db: Session = Depends(get_db),
         user: str = Depends(get_current_user)):

    message = req.message.lower()

    if "流程" in message:
        reply = "婚禮流程建議：迎賓 → 儀式 → 宴客 → 送客"
    elif "預算" in message:
        reply = "預算分配建議：場地40%、餐飲30%、攝影15%、佈置15%"
    elif "攝影" in message:
        reply = "建議提前與攝影師溝通拍攝清單與時間安排"
    else:
        reply = f"您好，您說的是：{req.message}"

    chat_record = ChatHistory(message=req.message, reply=reply)
    db.add(chat_record)
    db.commit()

    return {"reply": reply}

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    return db.query(ChatHistory).all()