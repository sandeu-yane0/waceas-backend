from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Text
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class DonationMethod(str, enum.Enum):
    orange_money = "orange_money"
    mtn_momo     = "mtn_momo"
    autre        = "autre"

class DonationStatus(str, enum.Enum):
    pending   = "pending"
    completed = "completed"
    failed    = "failed"

class Donation(Base):
    __tablename__ = "donations"
    id          = Column(Integer, primary_key=True, index=True)
    donor_name  = Column(String(200), nullable=True)
    phone       = Column(String(20), nullable=False)
    amount      = Column(Float, nullable=False)
    method      = Column(Enum(DonationMethod), nullable=False)
    status      = Column(Enum(DonationStatus), default=DonationStatus.pending)
    reference   = Column(String(100), nullable=True)
    note        = Column(Text, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
