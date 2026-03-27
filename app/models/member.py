from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class MemberType(str, enum.Enum):
    individual   = "individual"
    organization = "organization"
    intern       = "intern"
    volunteer    = "volunteer"

class MemberStatus(str, enum.Enum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected"

class Member(Base):
    __tablename__ = "members"
    id         = Column(Integer, primary_key=True, index=True)
    full_name  = Column(String(200), nullable=False)
    email      = Column(String(200), nullable=False)
    phone      = Column(String(20), nullable=True)
    type       = Column(Enum(MemberType), nullable=False)
    status     = Column(Enum(MemberStatus), default=MemberStatus.pending)
    motivation = Column(Text, nullable=True)
    skills     = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
