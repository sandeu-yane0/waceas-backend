from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ── Auth
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin: dict

# ── User
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: str = "editor"

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    class Config: from_attributes = True

# ── Media
class MediaOut(BaseModel):
    id: int
    type: str
    category: str
    title: str
    description: Optional[str]
    url: str
    public_id: Optional[str]
    thumbnail: Optional[str]
    is_active: bool
    created_at: datetime
    class Config: from_attributes = True

class MediaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

# ── Article
class ArticleCreate(BaseModel):
    title_fr: str
    title_en: str
    title_es: Optional[str] = None
    content_fr: str
    content_en: str
    content_es: Optional[str] = None
    status: str = "draft"

class ArticleUpdate(BaseModel):
    title_fr: Optional[str] = None
    title_en: Optional[str] = None
    title_es: Optional[str] = None
    content_fr: Optional[str] = None
    content_en: Optional[str] = None
    content_es: Optional[str] = None
    status: Optional[str] = None

class ArticleOut(BaseModel):
    id: int
    title_fr: str
    title_en: str
    title_es: Optional[str]
    content_fr: str
    content_en: str
    content_es: Optional[str]
    cover_image: Optional[str]
    status: str
    published_at: Optional[datetime]
    created_at: datetime
    class Config: from_attributes = True

# ── Donation
class DonationCreate(BaseModel):
    donor_name: Optional[str] = None
    phone: str
    amount: float
    method: str
    reference: Optional[str] = None
    note: Optional[str] = None

class DonationStatusUpdate(BaseModel):
    status: str

class DonationOut(BaseModel):
    id: int
    donor_name: Optional[str]
    phone: str
    amount: float
    method: str
    status: str
    reference: Optional[str]
    note: Optional[str]
    created_at: datetime
    class Config: from_attributes = True

# ── Member
class MemberCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    type: str
    motivation: Optional[str] = None
    skills: Optional[str] = None

class MemberStatusUpdate(BaseModel):
    status: str

class MemberOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    type: str
    status: str
    motivation: Optional[str]
    skills: Optional[str]
    created_at: datetime
    class Config: from_attributes = True

# ── Message
class MessageCreate(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    content: str

class MessageOut(BaseModel):
    id: int
    name: str
    email: str
    subject: Optional[str]
    content: str
    is_read: bool
    created_at: datetime
    class Config: from_attributes = True
