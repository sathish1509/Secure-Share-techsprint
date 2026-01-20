import os
from pathlib import Path
from storage.interface import StorageInterface
from files.encryption import FileEncryption
from config.settings import settings

class LocalStorage(StorageInterface):
    """Local filesystem storage with encryption"""
    
    def __init__(self):
        self.storage_dir = settings.UPLOAD_DIR
        self.encryption = FileEncryption()
        
    def store_file(self, file_data: bytes, file_id: str) -> str:
        """Store encrypted file locally"""
        file_path = self.storage_dir / f"{file_id}.enc"
        encrypted_data = self.encryption.encrypt_file(file_data)
        
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
            
        return str(file_path)
    
    def retrieve_file(self, storage_path: str) -> bytes:
        """Retrieve and decrypt file"""
        with open(storage_path, 'rb') as f:
            encrypted_data = f.read()
        
        return self.encryption.decrypt_file(encrypted_data)
    
    def delete_file(self, storage_path: str) -> bool:
        """Delete file from local storage"""
        try:
            if os.path.exists(storage_path):
                os.remove(storage_path)
                return True
            return False
        except Exception:
            return False
    
    def file_exists(self, storage_path: str) -> bool:
        """Check if file exists locally"""
        return os.path.exists(storage_path)