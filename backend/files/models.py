from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional
from config.database import Base

class FileMetadata(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    encrypted_path = Column(String, nullable=False)  # Path to encrypted file
    content_hash = Column(String, nullable=False, unique=True)  # IPFS-style hash
    ai_label = Column(String)
    is_private = Column(Boolean, default=True)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="files")
    shares = relationship("FileShare", back_populates="file")

class FileShare(Base):
    __tablename__ = "file_shares"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    shared_with_email = Column(String)  # Optional: specific user
    role = Column(String, default="viewer")  # owner, viewer, analyzer
    share_token = Column(String, unique=True)  # For public sharing
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    file = relationship("FileMetadata", back_populates="shares")

# Pydantic schemas
class FileUploadResponse(BaseModel):
    id: int
    name: str
    size: int
    hash: str
    ai_label: str
    uploaded_at: str
    is_private: bool

class FileListResponse(BaseModel):
    id: int
    name: str
    size: int
    mime_type: str
    hash: str
    ai_label: str
    upload_date: str
    is_private: bool

class FileShareCreate(BaseModel):
    file_id: int
    shared_with_email: Optional[str] = None
    role: str = "viewer"
    expires_hours: Optional[int] = None