from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="WedMind AI - 婚禮流程計畫")

# -----------------------
# 請求模型
# -----------------------
class ChatRequest(BaseModel):
    message: str

class SmartPlanRequest(BaseModel):
    style: str
    guests: int
    budget: float
    start_time: str

# -----------------------
# 假聊天功能
# -----------------------
@app.post("/chat")
def chat(req: ChatRequest):
    # 假 AI 回覆
    return {"reply": f"您好！您說的是：{req.message}"}

# -----------------------
# 假婚禮流程生成
# -----------------------
@app.post("/smart_generate")
def smart_generate(req: SmartPlanRequest):
    # 假 AI 生成婚禮流程
    return {
        "result": f"""
婚禮形式：{req.style}
賓客人數：{req.guests}
總預算：{req.budget}
開席時間：{req.start_time}

✔ 儀式流程：
- 迎賓
- 交換誓詞
- 戒指儀式

✔ 宴客流程：
- 新人進場
- 用餐
- 敬酒
- 送客

✔ 預算建議：
場地 40%
餐飲 30%
攝影 15%
佈置 15%
"""
    }

# -----------------------
# 根目錄測試頁
# -----------------------
@app.get("/")
def root():
    return {"message": "WedMind AI 婚禮流程計畫服務已啟動 🚀"}