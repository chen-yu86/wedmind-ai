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
    message = body.get("message", "").lower()

    # ------------------ 關鍵字群組 ------------------

    timeline_keywords = [
        "流程","時間","順序","儀式","宴客",
        "安排","進行","步驟","典禮"
    ]

    budget_keywords = [
        "預算","花費","多少錢","費用",
        "開銷","價格","金額","成本"
    ]

    # ------------------ 計分機制 ------------------

    timeline_score = sum(word in message for word in timeline_keywords)
    budget_score = sum(word in message for word in budget_keywords)

    timeline = None
    budget = None

    # ------------------ 判斷 ------------------

    if timeline_score > budget_score and timeline_score > 0:
        reply = "我幫您規劃婚禮流程時間軸 💍"

        timeline = [
            {"step":"迎賓","duration":1,"suggestion":"播放輕音樂"},
            {"step":"證婚儀式","duration":1.5,"suggestion":"交換誓詞"},
            {"step":"宴客","duration":2,"suggestion":"安排抽捧花"},
            {"step":"送客","duration":1,"suggestion":"發送小禮物"}
        ]

    elif budget_score > timeline_score and budget_score > 0:
        reply = "我幫您分析婚禮預算分配 💰"

        budget = {
            "場地":50000,
            "餐飲":80000,
            "攝影":30000,
            "婚紗":40000,
            "佈置":20000
        }

    else:
        reply = "我可以幫您規劃婚禮流程或分析預算，請告訴我您的需求 💍"

    return {
        "reply": reply,
        "timeline": timeline,
        "budget": budget
    }

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