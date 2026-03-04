from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json

app = FastAPI()

# CORS
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

# 首頁
@app.get("/")
async def home():
    return FileResponse("frontend/index.html")

# ------------------ Chat API ------------------

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")

    reply = f"婚禮助理建議：{message} 很棒的想法 💍"

    timeline = None
    budget = None

    if "流程" in message:
        timeline = [
            {"step":"迎賓","duration":1,"suggestion":"播放輕音樂"},
            {"step":"證婚儀式","duration":1.5,"suggestion":"安排誓詞"},
            {"step":"宴客","duration":2,"suggestion":"安排抽捧花"},
            {"step":"送客","duration":1,"suggestion":"準備小禮物"}
        ]

    if "預算" in message:
        budget = {
            "場地":50000,
            "餐飲":80000,
            "攝影":30000,
            "婚紗":40000,
            "佈置":20000
        }

    return {"reply": reply, "timeline": timeline, "budget": budget}

# ------------------ 儲存資料 ------------------

@app.post("/save_data")
async def save_data(request: Request):
    body = await request.json()
    username = body.get("username")
    data = body.get("data")

    c.execute("INSERT INTO user_data(username, data) VALUES (?, ?)", (username, json.dumps(data)))
    conn.commit()
    return {"status":"ok"}

@app.get("/get_data/{username}")
async def get_data(username: str):
    c.execute("SELECT data FROM user_data WHERE username=? ORDER BY id DESC LIMIT 1", (username,))
    row = c.fetchone()
    if row:
        return json.loads(row[0])
    return {}