from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageInterface(ABC):
    """Abstract storage interface for different storage backends"""
    
    @abstractmethod
    def store_file(self, file_data: bytes, file_id: str) -> str:
        """Store file and return storage path/identifier"""
        pass
    
    @abstractmethod
    def retrieve_file(self, storage_path: str) -> bytes:
        """Retrieve file data from storage"""
        pass
    
    @abstractmethod
    def delete_file(self, storage_path: str) -> bool:
        """Delete file from storage"""
        pass
    
    @abstractmethod
    def file_exists(self, storage_path: str) -> bool:
        """Check if file exists in storage"""
        pass