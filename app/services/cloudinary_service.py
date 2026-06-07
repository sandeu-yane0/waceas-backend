import cloudinary
import cloudinary.uploader
from app.core.config import settings


def _configure_unsigned():
    cloudinary.config(cloud_name=settings.CLOUDINARY_CLOUD_NAME, secure=True)


def upload_image(file_bytes: bytes, folder: str = "waceas", public_id: str = None) -> dict:
    if not settings.CLOUDINARY_CLOUD_NAME:
        from fastapi import HTTPException
        raise HTTPException(500, detail="CLOUDINARY_CLOUD_NAME manquant dans les variables d'environnement.")
    if not settings.CLOUDINARY_UPLOAD_PRESET:
        from fastapi import HTTPException
        raise HTTPException(500, detail="CLOUDINARY_UPLOAD_PRESET manquant dans les variables d'environnement.")
    _configure_unsigned()
    options = {"folder": folder}
    if public_id:
        options["public_id"] = public_id
    try:
        result = cloudinary.uploader.unsigned_upload(
            file_bytes,
            settings.CLOUDINARY_UPLOAD_PRESET,
            **options,
        )
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(500, detail=f"Erreur Cloudinary : {str(e)}")
    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
    }


def delete_image(public_id: str) -> bool:
    """Supprime de Cloudinary (non bloquant si les credentials manquent)."""
    try:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )
        result = cloudinary.uploader.destroy(public_id)
        return result.get("result") == "ok"
    except Exception as e:
        print(f"Suppression Cloudinary ignorée : {e}")
        return False


def upload_from_upload_file(upload_file, folder: str = "waceas") -> dict:
    file_bytes = upload_file.file.read()
    return upload_image(file_bytes, folder=folder)
