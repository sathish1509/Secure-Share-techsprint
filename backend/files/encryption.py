import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class FileEncryption:
    def __init__(self, password: bytes = None):
        if password is None:
            password = os.getenv("ENCRYPTION_KEY", "default-key-change-in-production").encode()
        
        # Derive key from password
        salt = b'secureshare_salt'  # In production, use random salt per file
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.cipher = Fernet(key)
    
    def encrypt_file(self, file_data: bytes) -> bytes:
        """Encrypt file data"""
        return self.cipher.encrypt(file_data)
    
    def decrypt_file(self, encrypted_data: bytes) -> bytes:
        """Decrypt file data"""
        return self.cipher.decrypt(encrypted_data)
    
    def encrypt_file_to_disk(self, file_data: bytes, output_path: str) -> str:
        """Encrypt and save file to disk"""
        encrypted_data = self.encrypt_file(file_data)
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)
        return output_path
    
    def decrypt_file_from_disk(self, encrypted_path: str) -> bytes:
        """Read and decrypt file from disk"""
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        return self.decrypt_file(encrypted_data)