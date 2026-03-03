from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "WedMind AI API is running 🚀"}

# 允許前端跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    guests: int = 100
    budget: int = 100000
    style: str = "西式"

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    user_msg = req.message.lower()

    # 婚禮流程
    if any(k in user_msg for k in ["流程", "download", "flow", "建議"]):
        timeline = [
            {"step": "迎賓", "duration": 1, "suggestion": "提前 30 分鐘準備迎賓流程"},
            {"step": "儀式", "duration": 2, "suggestion": "確認婚禮儀式順序及音樂"},
            {"step": "午宴", "duration": 2, "suggestion": "安排餐飲及座位表"},
            {"step": "攝影", "duration": 2, "suggestion": "攝影師準備拍攝角度"}
        ]
        return {"reply": "已生成婚禮流程表 📝", "timeline": timeline}

    # 預算建議
    elif any(k in user_msg for k in ["預算","budget"]):
        budget_allocation = {
            "場地": int(req.budget*0.4),
            "餐飲": int(req.budget*0.3),
            "攝影錄影": int(req.budget*0.15),
            "佈置花藝": int(req.budget*0.15)
        }
        return {"reply": f"婚禮預算建議: {budget_allocation}", "budget": budget_allocation}

    # 一般聊天
    else:
        return {"reply": f"您好！您說的是：{req.message}"}
