from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json
from database import SessionLocal, WeddingRecord, init_db

init_db()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Chat 模擬
@app.post("/chat")
def chat(message: dict):
    text = message.get("message", "")
    reply = f"您好，您說的是：{text}"
    # 簡單示範流程表
    timeline = [{"step":"訂婚儀式","duration":2,"suggestion":"上午舉行"}] if "流程" in text else None
    # 簡單示範預算表
    budget = {"場地": 50000,"餐飲":30000} if "預算" in text else None
    return {"reply": reply, "timeline": timeline, "budget": budget}

# 儲存紀錄
@app.post("/save_record")
def save_record(user_id: int, record_type: str, content: dict, db: Session = Depends(get_db)):
    record = WeddingRecord(
        user_id=user_id,
        record_type=record_type,
        content=json.dumps(content)
    )
    db.add(record)
    db.commit()
    return {"msg": "保存成功"}

# 取得紀錄
@app.get("/my_records/{user_id}")
def get_records(user_id: int, db: Session = Depends(get_db)):
    records = db.query(WeddingRecord).filter(WeddingRecord.user_id == user_id).all()
    return [
        {"record_type": r.record_type, "content": json.loads(r.content)}
        for r in records
    ]
