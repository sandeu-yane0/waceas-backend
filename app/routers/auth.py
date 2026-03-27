from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_current_admin, hash_password
from app.models.user import User
from app.schemas import LoginRequest, TokenResponse, UserCreate, UserOut

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email, User.is_active == True).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    user.last_login = datetime.utcnow()
    db.commit()
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer",
            "admin": {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role}}

@router.get("/me", response_model=UserOut)
def get_me(current_user=Depends(get_current_admin)):
    return current_user

@router.post("/admins", response_model=UserOut)
def create_admin(data: UserCreate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Réservé au super administrateur")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    user = User(email=data.email, full_name=data.full_name, password_hash=hash_password(data.password), role=data.role)
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.get("/admins", response_model=list[UserOut])
def list_admins(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Réservé au super administrateur")
    return db.query(User).all()
