# app/services/cloudinary_service.py
import cloudinary
import cloudinary.uploader
from app.core.config import settings

def init_cloudinary():
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )

def upload_image(file_bytes: bytes, folder: str = "waceas", public_id: str = None) -> dict:
    """
    Upload une image sur Cloudinary.
    Retourne: { 'url': str, 'public_id': str }
    """
    init_cloudinary()
    options = {
        "folder": folder,
        "resource_type": "image",
        "transformation": [{"quality": "auto", "fetch_format": "auto"}]
    }
    if public_id:
        options["public_id"] = public_id

    result = cloudinary.uploader.upload(file_bytes, **options)
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
