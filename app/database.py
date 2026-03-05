from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine("sqlite:///wedmind.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

class WeddingRecord(Base):
    __tablename__ = "wedding_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    record_type = Column(String(50))  # 'timeline' 或 'budget'
    content = Column(Text)            # 存 JSON 字串

# 初始化資料庫
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
