# backend.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# 允許前端呼叫
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 建立 SQLite DB
conn = sqlite3.connect("wedmind.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS wedding_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    data TEXT
)
""")
conn.commit()

class WeddingData(BaseModel):
    username: str
    data: str  # JSON 字串

@app.post("/save_data")
def save_data(item: WeddingData):
    cursor.execute("INSERT INTO wedding_data (username, data) VALUES (?, ?)", 
                   (item.username, item.data))
    conn.commit()
    return {"status": "success", "message": "資料已儲存"}

@app.get("/get_data/{username}")
def get_data(username: str):
    cursor.execute("SELECT data FROM wedding_data WHERE username = ?", (username,))
    rows = cursor.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="使用者資料不存在")
    return {"username": username, "data": [row[0] for row in rows]}
