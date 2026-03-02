from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

app = FastAPI(title="WedMind AI - 婚禮流程計畫")

# -----------------------
# 讀取 dashboard.html
# -----------------------
@app.get("/", response_class=HTMLResponse)
def read_dashboard():
    with open("dashboard.html", "r", encoding="utf-8") as f:
        return f.read()

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
# 聊天功能
# -----------------------
@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.lower()

    # 預算建議
    if "預算" in msg or "多少錢" in msg:
        reply = """
💰 婚禮預算建議：

✔ 場地：約 40%
✔ 餐飲：約 30%
✔ 攝影錄影：約 15%
✔ 佈置花藝：約 15%

建議預留 10% 作為突發備用金。
"""

    # 流程建議
    elif "流程" in msg or "安排" in msg:
        reply = """
📋 標準婚禮流程建議：

1️⃣ 迎賓 & 賓客入場
2️⃣ 新人進場
3️⃣ 主持人開場
4️⃣ 交換誓詞
5️⃣ 戒指儀式
6️⃣ 用餐 & 敬酒
7️⃣ 送客合影

可依中式或西式再調整。
"""

    # 場地建議
    elif "場地" in msg:
        reply = """
🏰 場地選擇建議：

✔ 西式：戶外草地、莊園
✔ 中式：飯店宴會廳
✔ 韓式：證婚堂 + 小型宴客
✔ 日式：神社或簡約會館

選場地時要考慮交通與賓客數量。
"""

    # 賓客人數
    elif "人數" in msg or "賓客" in msg:
        reply = """
👥 賓客規劃建議：

✔ 50人以下：溫馨小型婚禮
✔ 100人左右：標準宴客規模
✔ 200人以上：大型宴會

建議預估 10% 缺席率。
"""

    # 亞洲婚禮
    elif "中式" in msg:
        reply = "🇹🇼 中式婚禮通常包含文定、迎娶、拜別父母與宴客。"

    elif "日式" in msg:
        reply = "🇯🇵 日式婚禮常見神前式與教堂式，流程簡潔典雅。"

    elif "韓式" in msg:
        reply = "🇰🇷 韓式婚禮偏向快速儀式 + 宴客自助餐形式。"

    # 預設回答
    else:
        reply = """
🤖 我是 WedMind AI 婚禮顧問。

你可以詢問：
- 婚禮流程安排
- 婚禮預算分配
- 場地建議
- 中式 / 日式 / 韓式婚禮特色
- 賓客人數規劃

請告訴我你想了解哪一部分 💍
"""

    return {"reply": reply}

# -----------------------
# 婚禮流程生成
# -----------------------
@app.post("/smart_generate")
def smart_generate(req: SmartPlanRequest):
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