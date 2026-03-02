from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

DATABASE_URL = "sqlite:///./wedding.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

from pydantic import BaseModel
class RegisterRequest(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(req: RegisterRequest):
    db = SessionLocal()
    hashed = pwd_context.hash(req.password)
    user = User(username=req.username, password=hashed)
    db.add(user)
    db.commit()
    return {"message": "註冊成功"}

class LoginRequest(BaseModel):
    username: str
    password: str


from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(req: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.username == req.username).first()

    if not user:
        return {"error": "使用者不存在"}

    if not pwd_context.verify(req.password, user.password):
        return {"error": "密碼錯誤"}

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

from pydantic import BaseModel

class SmartPlanRequest(BaseModel):
    style: str
    guests: int
    budget: int
    start_time: str

@app.post("/smart_generate")
def smart_generate(req: SmartPlanRequest):
    # 先用假資料模板，確保部署成功
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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fpdf import FPDF
from fastapi.responses import FileResponse
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- 資料格式 -----------
class TableRow(BaseModel):
    user: str
    assistant: str

class PDFRequest(BaseModel):
    ceremony: List[TableRow]
    banquet: List[TableRow]
    music: List[TableRow]
    budget: List[TableRow]


# ----------- PDF 樣式 -----------
class WeddingPDF(FPDF):

    def header(self):
        self.set_font("Arial", "I", 9)
        self.set_text_color(150)
        self.cell(0, 8, "Professional Wedding Planning System", align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 9)
        self.set_text_color(150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, title):
        self.set_font("Arial", "B", 16)
        self.set_text_color(214, 51, 132)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def table_header(self):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(255, 182, 193)
        self.cell(50, 8, "時間 / 項目", border=1, fill=True)
        self.cell(140, 8, "內容 / 說明", border=1, ln=True, fill=True)

    def table_row(self, left, right):
        self.set_font("Arial", "", 11)
        self.cell(50, 8, left, border=1)
        self.multi_cell(140, 8, right, border=1)


# ----------- 生成 PDF -----------
@app.post("/download_pdf")
def download_pdf(req: PDFRequest):

    pdf = WeddingPDF()
    pdf.add_page()

    # 封面
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(214, 51, 132)
    pdf.cell(0, 20, "婚禮完整規劃書", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 14)
    pdf.cell(0, 10, f"生成日期: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.add_page()

    # -------- 儀式 --------
    pdf.section_title("一、婚禮儀式流程")
    pdf.table_header()
    for row in req.ceremony:
        pdf.table_row(row.user, row.assistant)
    pdf.ln(10)

    # -------- 宴客 --------
    pdf.section_title("二、宴客流程")
    pdf.table_header()
    for row in req.banquet:
        pdf.table_row(row.user, row.assistant)
    pdf.ln(10)

    # -------- 音樂 --------
    pdf.section_title("三、音樂規劃")
    pdf.table_header()
    for row in req.music:
        pdf.table_row(row.user, row.assistant)
    pdf.ln(10)

    # -------- 預算 --------
    pdf.section_title("四、預算規劃")
    pdf.table_header()

    total = 0
    for row in req.budget:
        pdf.table_row(row.user, row.assistant)
        try:
            total += float(row.assistant)
        except:
            pass

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 10, f"總預算：NT$ {int(total):,}", ln=True)

    # -------- 輸出 --------
    filename = f"wedding_master_plan_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)

    return FileResponse(filename, media_type='application/pdf', filename=filename)
