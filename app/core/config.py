from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./waceas.db"
    SECRET_KEY: str = "dev-secret-key-changez-en-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    FIRST_ADMIN_EMAIL: str = "admin@waceas.com"
    FIRST_ADMIN_PASSWORD: str = "WaceasAdmin2026!"
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    # CORS — inclut tous les environnements possibles
    ALLOWED_ORIGINS: str = "https://waceas.com,https://waceas.com/admin,http://localhost:3001,http://localhost:3000,http://localhost:5173,http://127.0.0.1:3001,http://127.0.0.1:5173"

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        # Ignorer les espaces autour des valeurs
        env_file_encoding = "utf-8"

settings = Settings()
