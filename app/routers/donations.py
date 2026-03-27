from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import csv, io
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.donation import Donation
from app.schemas import DonationCreate, DonationOut, DonationStatusUpdate

router = APIRouter(prefix="/api/donations", tags=["Donations"])

@router.post("/", response_model=DonationOut)
def record(data: DonationCreate, db: Session = Depends(get_db)):
    d = Donation(**data.model_dump()); db.add(d); db.commit(); db.refresh(d); return d

@router.get("/", response_model=list[DonationOut])
def list_all(status: Optional[str] = None, method: Optional[str] = None,
             skip: int = Query(0, ge=0), limit: int = Query(50, le=200),
             db: Session = Depends(get_db), _=Depends(get_current_admin)):
    q = db.query(Donation)
    if status: q = q.filter(Donation.status == status)
    if method: q = q.filter(Donation.method == method)
    return q.order_by(Donation.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/stats")
def stats(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    total     = db.query(func.count(Donation.id)).scalar()
    completed = db.query(func.count(Donation.id)).filter(Donation.status == "completed").scalar()
    total_amt = db.query(func.sum(Donation.amount)).filter(Donation.status == "completed").scalar() or 0
    by_method = db.query(Donation.method, func.sum(Donation.amount)).filter(Donation.status == "completed").group_by(Donation.method).all()
    return {"total_donations": total, "completed": completed,
            "total_amount_xaf": round(total_amt, 0), "by_method": {m: round(a or 0, 0) for m, a in by_method}}

@router.patch("/{donation_id}", response_model=DonationOut)
def update_status(donation_id: int, data: DonationStatusUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    d = db.query(Donation).filter(Donation.id == donation_id).first()
    if not d: raise HTTPException(404, detail="Don introuvable")
    d.status = data.status; db.commit(); db.refresh(d); return d

@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    donations = db.query(Donation).order_by(Donation.created_at.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Nom", "Téléphone", "Montant (XAF)", "Méthode", "Statut", "Référence", "Date"])
    for d in donations:
        writer.writerow([d.id, d.donor_name or "Anonyme", d.phone, d.amount, d.method, d.status, d.reference or "", d.created_at.strftime("%d/%m/%Y %H:%M")])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=dons_waceas.csv"})
