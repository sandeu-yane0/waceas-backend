from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class MediaType(str, enum.Enum):
    photo = "photo"
    video = "video"

class MediaCategory(str, enum.Enum):
    evenement = "evenement"
    seminaire = "seminaire"
    terrain   = "terrain"
    formation = "formation"
    autre     = "autre"

class Media(Base):
    __tablename__ = "media"
    id           = Column(Integer, primary_key=True, index=True)
    type         = Column(Enum(MediaType), nullable=False)
    category     = Column(Enum(MediaCategory), default=MediaCategory.autre)
    title        = Column(String(200), nullable=False)
    description  = Column(Text, nullable=True)
    url          = Column(String(500), nullable=False)      # URL Cloudinary ou YouTube
    public_id    = Column(String(300), nullable=True)       # Cloudinary public_id pour suppression
    thumbnail    = Column(String(500), nullable=True)
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())
