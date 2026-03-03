from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允許跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⭐ 首頁回傳 HTML
@app.get("/", response_class=HTMLResponse)
async def homepage():
    return """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WedMind AI 婚禮助理</title>
<style>
    body { font-family: Arial, sans-serif; margin: 20px; background: #f2f2f2; }
    h1 { color: #333; text-align: center; }
    #chatBox { width: 100%; max-width: 600px; margin: 20px auto; }
    #messages { border: 1px solid #ccc; height: 300px; overflow-y: auto; padding: 10px; background: #fff; }
    .user { color: blue; margin: 5px 0; }
    .bot { color: green; margin: 5px 0; }
    input[type="text"] { width: 70%; padding: 8px; }
    button { padding: 8px 12px; margin-left: 5px; }
</style>
</head>
<body>

<h1>WedMind AI 婚禮助理</h1>

<div id="chatBox">
    <div id="messages"></div>
    <input type="text" id="userInput" placeholder="輸入訊息..." />
    <button onclick="sendMessage()">送出</button>
    <button onclick="generateTimeline()">生成流程</button>
    <button onclick="generateBudget()">生成預算</button>
</div>

<script>
const messagesDiv = document.getElementById("messages");

async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (!message) return;

    appendMessage("user", message);
    input.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });
    const data = await response.json();
    appendMessage("bot", data.reply);
}

async function generateTimeline() {
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "生成流程" })
    });
    const data = await response.json();
    appendMessage("bot", data.reply);
    if (data.timeline) {
        data.timeline.forEach(step => {
            appendMessage("bot", `${step.step} (${step.duration} 小時): ${step.suggestion}`);
        });
    }
}

async function generateBudget() {
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "預算" })
    });
    const data = await response.json();
    appendMessage("bot", data.reply);
    if (data.budget) {
        Object.entries(data.budget).forEach(([key, value]) => {
            appendMessage("bot", `${key}: ${value} 元`);
        });
    }
}

function appendMessage(sender, text) {
    const div = document.createElement("div");
    div.className = sender;
    div.textContent = text;
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
</script>

</body>
</html>
"""

# ===== API 區 =====

class ChatRequest(BaseModel):
    message: str
    guests: int = 100
    budget: int = 100000
    style: str = "西式"

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
        return {"reply": "婚禮預算建議如下 💰", "budget": budget_allocation}

    else:
        return {"reply": f"您好！您說的是：{req.message}"}