from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.media import Media
from app.models.article import Article
from app.models.donation import Donation
from app.models.member import Member
from app.models.message import Message
from app.routers import auth, media, articles, donations, members, messages, dashboard

# Créer les tables
Base.metadata.create_all(bind=engine)

# Créer le premier admin
def create_first_admin():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first():
            db.add(User(
                email=settings.FIRST_ADMIN_EMAIL,
                full_name="Super Admin WACEAS",
                password_hash=hash_password(settings.FIRST_ADMIN_PASSWORD),
                role=UserRole.superadmin,
                is_active=True
            ))
            db.commit()
            print(f"✅ Admin créé : {settings.FIRST_ADMIN_EMAIL}")
    finally:
        db.close()

create_first_admin()

app = FastAPI(
    title="WACEAS API",
    description="Backend WACEAS — Women And Child Empowerment Association",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    create_first_admin()



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(media.router)
app.include_router(articles.router)
app.include_router(donations.router)
app.include_router(members.router)
app.include_router(messages.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "WACEAS API v1.0 — OK", "docs": "/api/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
