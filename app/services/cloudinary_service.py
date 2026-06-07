# app/services/cloudinary_service.py
import cloudinary
import cloudinary.uploader
from app.core.config import settings

def init_cloudinary():
    if settings.CLOUDINARY_URL:
        cloudinary.config(cloudinary_url=settings.CLOUDINARY_URL, secure=True)
    else:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )

def upload_image(file_bytes: bytes, folder: str = "waceas", public_id: str = None) -> dict:
    init_cloudinary()
    if not settings.CLOUDINARY_URL and (not settings.CLOUDINARY_CLOUD_NAME or not settings.CLOUDINARY_API_KEY):
        from fastapi import HTTPException
        raise HTTPException(500, detail="Cloudinary non configuré. Ajoutez CLOUDINARY_URL dans Render.")
    options = {
        "folder": folder,
        "resource_type": "image",
    }
    if public_id:
        options["public_id"] = public_id
    try:
        result = cloudinary.uploader.upload(file_bytes, **options)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(500, detail=f"Erreur Cloudinary : {str(e)}")
    return {
        "url": result["secure_url"],
        "public_id": result["public_id"]
    }

def delete_image(public_id: str) -> bool:
    """Supprime une image de Cloudinary par son public_id."""
    init_cloudinary()
    result = cloudinary.uploader.destroy(public_id)
    return result.get("result") == "ok"

def upload_from_upload_file(upload_file, folder: str = "waceas") -> dict:
    """Helper pour FastAPI UploadFile."""
    file_bytes = upload_file.file.read()
    return upload_image(file_bytes, folder=folder)
