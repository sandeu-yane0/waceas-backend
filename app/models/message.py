from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"
    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(200), nullable=False)
    email      = Column(String(200), nullable=False)
    subject    = Column(String(300), nullable=True)
    content    = Column(Text, nullable=False)
    is_read    = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
