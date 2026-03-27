from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class ArticleStatus(str, enum.Enum):
    draft     = "draft"
    published = "published"

class Article(Base):
    __tablename__ = "articles"
    id           = Column(Integer, primary_key=True, index=True)
    title_fr     = Column(String(300), nullable=False)
    title_en     = Column(String(300), nullable=False)
    title_es     = Column(String(300), nullable=True)
    content_fr   = Column(Text, nullable=False)
    content_en   = Column(Text, nullable=False)
    content_es   = Column(Text, nullable=True)
    cover_image  = Column(String(500), nullable=True)       # URL Cloudinary
    cover_public_id = Column(String(300), nullable=True)    # Cloudinary public_id
    status       = Column(Enum(ArticleStatus), default=ArticleStatus.draft)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())
