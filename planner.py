class WeddingPlanner:

    def __init__(self, budget: int = 100000):
        if budget <= 0:
            raise ValueError("Budget must be positive")
        self.budget = budget

    def generate_timeline(self):
        return [
            {"step": "迎賓", "duration": 1},
            {"step": "儀式", "duration": 2},
            {"step": "午宴", "duration": 2},
            {"step": "送客", "duration": 1}
        ]

    def generate_budget(self):
        return {
            "場地": int(self.budget * 0.4),
            "餐飲": int(self.budget * 0.3),
            "攝影": int(self.budget * 0.15),
            "佈置": int(self.budget * 0.15)
        }

    def handle_message(self, message: str):
        if not message:
            return {"reply": "請輸入訊息"}

        msg = message.lower()

        if any(k in msg for k in ["流程", "安排", "順序"]):
            return {
                "reply": "已生成婚禮流程圖表",
                "timeline": self.generate_timeline()
            }

        if any(k in msg for k in ["預算", "費用"]):
            return {
                "reply": "已生成預算圓餅圖",
                "budget": self.generate_budget()
            }

        return {"reply": "您好，請詢問流程或預算規劃"}