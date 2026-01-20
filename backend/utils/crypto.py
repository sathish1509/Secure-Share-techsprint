import secrets
import hashlib
from datetime import datetime, timedelta

def generate_secure_token(length: int = 32) -> str:
    """Generate cryptographically secure random token"""
    return secrets.token_urlsafe(length)

def hash_content(content: bytes) -> str:
    """Generate SHA-256 hash of content"""
    return hashlib.sha256(content).hexdigest()

def generate_share_token() -> str:
    """Generate secure sharing token"""
    return generate_secure_token(16)

def is_token_expired(created_at: datetime, expires_hours: int) -> bool:
    """Check if token has expired"""
    if expires_hours is None:
        return False
    
    expiry_time = created_at + timedelta(hours=expires_hours)
    return datetime.utcnow() > expiry_time