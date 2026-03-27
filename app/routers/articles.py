from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.article import Article, ArticleStatus
from app.schemas import ArticleOut, ArticleCreate, ArticleUpdate
from app.services.cloudinary_service import upload_from_upload_file, delete_image

router = APIRouter(prefix="/api/articles", tags=["Articles"])

@router.get("/", response_model=list[ArticleOut])
def get_published(db: Session = Depends(get_db)):
    return db.query(Article).filter(Article.status == ArticleStatus.published).order_by(Article.published_at.desc()).all()

@router.get("/admin/all", response_model=list[ArticleOut])
def get_all(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return db.query(Article).order_by(Article.created_at.desc()).all()

@router.get("/{article_id}", response_model=ArticleOut)
def get_one(article_id: int, db: Session = Depends(get_db)):
    a = db.query(Article).filter(Article.id == article_id).first()
    if not a: raise HTTPException(404, detail="Article introuvable")
    return a

@router.post("/", response_model=ArticleOut)
def create(data: ArticleCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    article = Article(**data.model_dump())
    if data.status == "published":
        article.published_at = datetime.utcnow()
    db.add(article); db.commit(); db.refresh(article)
    return article

@router.post("/{article_id}/cover", response_model=ArticleOut)
async def upload_cover(article_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), _=Depends(get_current_admin)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article: raise HTTPException(404, detail="Article introuvable")
    # Supprimer l'ancienne image Cloudinary
    if article.cover_public_id:
        delete_image(article.cover_public_id)
    result = upload_from_upload_file(file, folder="waceas/articles")
    article.cover_image = result["url"]
    article.cover_public_id = result["public_id"]
    db.commit(); db.refresh(article)
    return article

@router.patch("/{article_id}", response_model=ArticleOut)
def update(article_id: int, data: ArticleUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article: raise HTTPException(404, detail="Article introuvable")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(article, k, v)
    if data.status == "published" and not article.published_at:
        article.published_at = datetime.utcnow()
    db.commit(); db.refresh(article)
    return article

@router.delete("/{article_id}")
def delete(article_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article: raise HTTPException(404, detail="Article introuvable")
    if article.cover_public_id:
        delete_image(article.cover_public_id)
    db.delete(article); db.commit()
    return {"message": "Article supprimé"}
