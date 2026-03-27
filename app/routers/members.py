from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.member import Member
from app.schemas import MemberCreate, MemberOut, MemberStatusUpdate

router = APIRouter(prefix="/api/members", tags=["Members"])

@router.post("/", response_model=MemberOut)
def apply(data: MemberCreate, db: Session = Depends(get_db)):
    m = Member(**data.model_dump()); db.add(m); db.commit(); db.refresh(m); return m

@router.get("/", response_model=list[MemberOut])
def list_all(status: Optional[str] = None, type: Optional[str] = None,
             skip: int = Query(0, ge=0), limit: int = Query(50, le=200),
             db: Session = Depends(get_db), _=Depends(get_current_admin)):
    q = db.query(Member)
    if status: q = q.filter(Member.status == status)
    if type:   q = q.filter(Member.type == type)
    return q.order_by(Member.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/{member_id}", response_model=MemberOut)
def get_one(member_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    m = db.query(Member).filter(Member.id == member_id).first()
    if not m: raise HTTPException(404, detail="Membre introuvable")
    return m

@router.patch("/{member_id}", response_model=MemberOut)
def update_status(member_id: int, data: MemberStatusUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    m = db.query(Member).filter(Member.id == member_id).first()
    if not m: raise HTTPException(404, detail="Membre introuvable")
    m.status = data.status; db.commit(); db.refresh(m); return m

@router.delete("/{member_id}")
def delete(member_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    m = db.query(Member).filter(Member.id == member_id).first()
    if not m: raise HTTPException(404, detail="Membre introuvable")
    db.delete(m); db.commit(); return {"message": "Membre supprimé"}
