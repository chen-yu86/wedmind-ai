from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

# 如果前端需要跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 首頁路由，回傳 index.html
@app.get("/")
async def home():
    return FileResponse("frontend/index.html")

# 範例 chat API
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    
    # 這裡你可以接入你的 AI 邏輯
    reply = f"你剛剛說: {message}"
    
    # 範例回傳流程表或預算表
    timeline = [
        {"step": "迎賓", "duration": 1, "suggestion": "準備迎賓桌"},
        {"step": "婚禮儀式", "duration": 2, "suggestion": "音樂與流程"}
    ]
    budget = {"場地": 50000, "餐點": 20000}

    return {"reply": reply, "timeline": timeline, "budget": budget}

# 其他 API 路由照舊
# @app.post("/save_data")
# @app.get("/get_data/{username}")
