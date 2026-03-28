from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
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

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            existing = db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first()
            if not existing:
                db.add(User(
                    email=settings.FIRST_ADMIN_EMAIL,
                    full_name="Super Admin WACEAS",
                    password_hash=hash_password(settings.FIRST_ADMIN_PASSWORD),
                    role=UserRole.superadmin,
                    is_active=True
                ))
                db.commit()
                print(f"✅ Admin créé : {settings.FIRST_ADMIN_EMAIL}")
            else:
                print(f"ℹ️  Admin existant : {settings.FIRST_ADMIN_EMAIL}")
        finally:
            db.close()
    except Exception as e:
        print(f"⚠️  Erreur init DB (non bloquante) : {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="WACEAS API",
    description="Backend WACEAS — Women And Child Empowerment Association",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS — accepte toutes les origines pour le dashboard admin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permissif — le JWT protège les routes sensibles
    allow_credentials=False,  # Doit être False quand allow_origins=["*"]
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
