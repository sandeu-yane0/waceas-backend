from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.media import Media
from app.models.article import Article
from app.models.donation import Donation
from app.models.member import Member
from app.models.message import Message

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return {
        "total_media":      db.query(func.count(Media.id)).scalar(),
        "total_articles":   db.query(func.count(Article.id)).scalar(),
        "total_donations":  db.query(func.count(Donation.id)).scalar(),
        "total_amount_xaf": round(db.query(func.sum(Donation.amount)).filter(Donation.status == "completed").scalar() or 0, 0),
        "pending_members":  db.query(func.count(Member.id)).filter(Member.status == "pending").scalar(),
        "unread_messages":  db.query(func.count(Message.id)).filter(Message.is_read == False).scalar(),
        "recent_donations": [{"id": d.id, "donor": d.donor_name or "Anonyme", "amount": d.amount, "method": d.method, "status": d.status, "date": d.created_at.isoformat()} for d in db.query(Donation).order_by(Donation.created_at.desc()).limit(5).all()],
        "recent_members":   [{"id": m.id, "name": m.full_name, "type": m.type, "status": m.status, "date": m.created_at.isoformat()} for m in db.query(Member).order_by(Member.created_at.desc()).limit(5).all()],
    }
