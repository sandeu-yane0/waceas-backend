from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.message import Message
from app.schemas import MessageCreate, MessageOut

router = APIRouter(prefix="/api/messages", tags=["Messages"])

@router.post("/", response_model=MessageOut)
def send(data: MessageCreate, db: Session = Depends(get_db)):
    msg = Message(**data.model_dump()); db.add(msg); db.commit(); db.refresh(msg); return msg

@router.get("/", response_model=list[MessageOut])
def list_all(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return db.query(Message).order_by(Message.created_at.desc()).all()

@router.patch("/{message_id}/read", response_model=MessageOut)
def mark_read(message_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg: raise HTTPException(404, detail="Message introuvable")
    msg.is_read = True; db.commit(); db.refresh(msg); return msg

@router.delete("/{message_id}")
def delete(message_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg: raise HTTPException(404, detail="Message introuvable")
    db.delete(msg); db.commit(); return {"message": "Supprimé"}
