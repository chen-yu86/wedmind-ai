from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from schemas import ChatRequest

app = FastAPI(title="WedMind Backend Portfolio")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    user_msg = req.message.lower()

    if any(k in user_msg for k in ["流程", "download", "flow", "建議"]):
        timeline = [
            {"step": "迎賓", "duration": 1, "suggestion": "提前 30 分鐘準備迎賓流程"},
            {"step": "儀式", "duration": 2, "suggestion": "確認婚禮儀式順序及音樂"},
            {"step": "午宴", "duration": 2, "suggestion": "安排餐飲及座位表"},
            {"step": "攝影", "duration": 2, "suggestion": "攝影師準備拍攝角度"}
        ]
        return {"reply": "已生成婚禮流程表 📝", "timeline": timeline}

    elif any(k in user_msg for k in ["預算","budget"]):
        budget_allocation = {
            "場地": int(req.budget*0.4),
            "餐飲": int(req.budget*0.3),
            "攝影錄影": int(req.budget*0.15),
            "佈置花藝": int(req.budget*0.15)
        }
        return {"reply": f"婚禮預算建議: {budget_allocation}", "budget": budget_allocation}

    else:
        return {"reply": f"您好！您說的是：{req.message}"}