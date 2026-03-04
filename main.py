from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json

app = FastAPI()

# 允許前端跨域存取
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite 初始化
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS user_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    data TEXT
)
""")
conn.commit()

# -------------------- Chat API --------------------
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")
    
    # 模擬回覆
    reply = f"您好，您說的是：{message}"
    
    # 可加婚禮流程或預算的回覆
    timeline = [{"step":"迎賓","duration":2,"suggestion":"準備紅毯"}] if "流程" in message else None
    budget = {"場地":20000,"餐飲":15000} if "預算" in message else None
    
    return {"reply": reply, "timeline": timeline, "budget": budget}

# -------------------- 儲存使用者資料 --------------------
@app.post("/save_data")
async def save_data(request: Request):
    body = await request.json()
    username = body.get("username")
    data = body.get("data")
    c.execute("INSERT INTO user_data(username, data) VALUES (?, ?)", (username, data))
    conn.commit()
    return {"status":"ok"}

@app.get("/get_data/{username}")
async def get_data(username: str):
    c.execute("SELECT * FROM user_data WHERE username=? ORDER BY id", (username,))
    rows = c.fetchall()
    return {"data":[{"id":r[0],"username":r[1],"data":r[2]} for r in rows]}
