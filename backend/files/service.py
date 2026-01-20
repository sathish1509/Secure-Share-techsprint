import hashlib
import os
from typing import Dict, Any
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from files.models import FileMetadata
from files.encryption import FileEncryption
from config.settings import settings

# Allowed MIME types matching frontend
ALLOWED_MIME_TYPES = {
    'image/jpeg': {'ext': 'jpg', 'category': 'Image'},
    'image/png': {'ext': 'png', 'category': 'Image'},
    'image/gif': {'ext': 'gif', 'category': 'Image'},
    'application/pdf': {'ext': 'pdf', 'category': 'Document'},
    'text/plain': {'ext': 'txt', 'category': 'Document'},
    'application/msword': {'ext': 'doc', 'category': 'Document'},
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': {'ext': 'docx', 'category': 'Document'},
    'application/vnd.ms-excel': {'ext': 'xls', 'category': 'Spreadsheet'},
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': {'ext': 'xlsx', 'category': 'Spreadsheet'},
    'application/zip': {'ext': 'zip', 'category': 'Archive'},
    'video/mp4': {'ext': 'mp4', 'category': 'Video'},
    'audio/mpeg': {'ext': 'mp3', 'category': 'Audio'}
}

def validate_file(file: UploadFile) -> Dict[str, Any]:
    """Validate file type and size"""
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file.content_type}' not allowed"
        )
    
    # Read file to check size
    file_data = file.file.read()
    file.file.seek(0)  # Reset file pointer
    
    if len(file_data) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size ({settings.MAX_FILE_SIZE} bytes)"
        )
    
    return {
        'data': file_data,
        'size': len(file_data),
        'category': ALLOWED_MIME_TYPES[file.content_type]['category']
    }

def generate_content_hash(file_data: bytes) -> str:
    """Generate IPFS-style content hash"""
    sha256_hash = hashlib.sha256(file_data).hexdigest()
    # IPFS-style hash: Qm + first 44 chars of hash
    return f"Qm{sha256_hash[:44]}"

def generate_ai_label(filename: str, category: str) -> str:
    """Generate AI label based on filename and category"""
    filename_lower = filename.lower()
    
    # Specific patterns
    if 'report' in filename_lower:
        return '📊 Financial Report'
    if 'presentation' in filename_lower:
        return '🎯 Presentation'
    if 'contract' in filename_lower:
        return '📋 Contract/Agreement'
    if 'invoice' in filename_lower:
        return '💰 Invoice'
    if 'resume' in filename_lower or 'cv' in filename_lower:
        return '👔 Resume/CV'
    if 'backup' in filename_lower:
        return '💾 Backup Data'
    if 'screenshot' in filename_lower:
        return '📸 Screenshot'
    
    # Category-based labels
    label_map = {
        'Image': ['Photo', 'Graphic', 'Visual Content'],
        'Document': ['Text Document', 'Report', 'Written Content'],
        'Spreadsheet': ['Data Table', 'Financial Report', 'Analytics'],
        'Archive': ['Compressed Files', 'Backup Bundle'],
        'Video': ['Video Media', 'Recording'],
        'Audio': ['Audio Recording', 'Music']
    }
    
    import random
    category_labels = label_map.get(category, ['File'])
    return random.choice(category_labels)

def save_encrypted_file(file_data: bytes, filename: str, user_id: int) -> str:
    """Save file with encryption"""
    # Generate unique filename
    content_hash = generate_content_hash(file_data)
    encrypted_filename = f"{user_id}_{content_hash}_{filename}"
    encrypted_path = settings.UPLOAD_DIR / encrypted_filename
    
    # Encrypt and save
    encryption = FileEncryption()
    encryption.encrypt_file_to_disk(file_data, str(encrypted_path))
    
    return str(encrypted_path)

def get_user_files(db: Session, user_id: int):
    """Get all files for a user"""
    return db.query(FileMetadata).filter(FileMetadata.owner_id == user_id).all()

def get_file_by_id(db: Session, file_id: int, user_id: int):
    """Get specific file owned by user"""
    return db.query(FileMetadata).filter(
        FileMetadata.id == file_id,
        FileMetadata.owner_id == user_id
    ).first()

def delete_file(db: Session, file_id: int, user_id: int) -> bool:
    """Delete file and its encrypted data"""
    file_record = get_file_by_id(db, file_id, user_id)
    if not file_record:
        return False
    
    # Delete encrypted file from disk
    try:
        if os.path.exists(file_record.encrypted_path):
            os.remove(file_record.encrypted_path)
    except Exception:
        pass  # Continue even if file deletion fails
    
    # Delete from database
    db.delete(file_record)
    db.commit()
    return True