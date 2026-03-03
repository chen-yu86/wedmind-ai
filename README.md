# WedMind – Rule-Based Wedding Planning API

## 📌 Project Overview
WedMind 是依循規則的婚禮流程規劃後端系統，使用 FastAPI 建構。  
它能提供婚禮流程時間軸生成、預算分配建議，以及簡單的聊天互動。  

這個專案展示：

- RESTful API 設計
- 物件導向 (OOP)
- 分層設計 (Separation of Concerns)
- 輸入驗證 (Input Validation)
- 雲端部署 (Render)

---

## 🏗 Architecture

專案結構分層清楚：

- `main.py`  
  - 處理 HTTP 請求  
  - 使用 Pydantic 驗證輸入  
  - 與業務邏輯層分離  

- `planner.py`  
  - 封裝婚禮規劃核心邏輯  
  - 生成流程時間軸與預算建議  
  - 實作簡單的規則判斷

---

## 🚀 Tech Stack

- Python 3
- FastAPI
- Pydantic
- Uvicorn
- Render (Cloud Deployment)

---

## 📡 API Endpoint

### POST /chat

Request Body 範例：

```json
{
  "message": "請給我預算建議",
  "guests": 100,
  "budget": 100000,
  "style": "西式"
}
{
  "reply": "已生成預算圓餅圖",
  "budget": {
    "場地": 40000,
    "餐飲": 30000,
    "攝影": 15000,
    "佈置": 15000
  }
}

Design Concept
核心邏輯封裝在 WeddingPlanner 類別中
API 層與業務邏輯層分離
實作基本輸入驗證
系統設計可擴充，方便未來加入新功能

Live Demo
已部署於 Render：
https://wedmind-ai.onrender.com

Future Improvements
加入資料庫整合 (Database Integration)
實作使用者認證 (Authentication)
強化規則判斷邏輯 (Rule-based NLP)
撰寫單元測試 (Unit Tests)