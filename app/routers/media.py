from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.media import Media
from app.schemas import MediaOut, MediaUpdate
from app.services.cloudinary_service import upload_from_upload_file, delete_image

router = APIRouter(prefix="/api/media", tags=["Media"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

# ── Public
@router.get("/", response_model=list[MediaOut])
def get_media(type: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Media).filter(Media.is_active == True)
    if type:     q = q.filter(Media.type == type)
    if category: q = q.filter(Media.category == category)
    return q.order_by(Media.created_at.desc()).all()

# ── Admin: tous
@router.get("/admin/all", response_model=list[MediaOut])
def get_all(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return db.query(Media).order_by(Media.created_at.desc()).all()

# ── Admin: upload photo → Cloudinary
@router.post("/upload/photo", response_model=MediaOut)
async def upload_photo(
    title: str = Form(...),
    category: str = Form("autre"),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(get_current_admin)
):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(400, detail="Format non supporté. Utilisez JPEG, PNG ou WebP.")
    
    # Upload vers Cloudinary
    result = upload_from_upload_file(file, folder="waceas/media")
    
    media = Media(
        type="photo", category=category, title=title,
        description=description, url=result["url"], public_id=result["public_id"]
    )
    db.add(media); db.commit(); db.refresh(media)
    return media

# ── Admin: ajouter vidéo YouTube
@router.post("/add/video", response_model=MediaOut)
def add_video(
    title: str = Form(...),
    category: str = Form("autre"),
    description: Optional[str] = Form(None),
    youtube_url: str = Form(...),
    thumbnail: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    _=Depends(get_current_admin)
):
    media = Media(type="video", category=category, title=title,
                  description=description, url=youtube_url, thumbnail=thumbnail)
    db.add(media); db.commit(); db.refresh(media)
    return media

# ── Admin: modifier
@router.patch("/{media_id}", response_model=MediaOut)
def update_media(media_id: int, data: MediaUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media: raise HTTPException(404, detail="Média introuvable")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(media, k, v)
    db.commit(); db.refresh(media)
    return media

# ── Admin: supprimer (+ Cloudinary)
@router.delete("/{media_id}")
def delete_media(media_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media: raise HTTPException(404, detail="Média introuvable")
    # Supprimer de Cloudinary si c'est une photo
    if media.public_id:
        delete_image(media.public_id)
    db.delete(media); db.commit()
    return {"message": "Média supprimé"}
