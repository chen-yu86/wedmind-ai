from sqlalchemy import Column, Integer, String
from database import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    reply = Column(String, nullable=False)