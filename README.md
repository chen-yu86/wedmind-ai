# WedMind – Rule-Based Wedding Planning API

## 📌 Project Overview

WedMind is a rule-based backend system built with FastAPI.
It provides wedding planning suggestions including timeline generation and budget allocation.

This project demonstrates:

- RESTful API design
- Object-Oriented Programming (OOP)
- Separation of Concerns
- Input validation
- Cloud deployment

---

## 🏗 Architecture

The project separates API layer and business logic layer.

main.py  
- Handles HTTP requests  
- Validates input using Pydantic  

planner.py  
- Encapsulates business logic  
- Generates timeline and budget allocation  
- Implements rule-based message handling  

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

Request Body:

```json
{
  "message": "請給我預算建議",
  "budget": 100000
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