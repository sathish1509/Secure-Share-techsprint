from enum import Enum

class FileRole(str, Enum):
    OWNER = "owner"
    VIEWER = "viewer" 
    ANALYZER = "analyzer"

class ShareType(str, Enum):
    PRIVATE = "private"
    PUBLIC_LINK = "public_link"
    SPECIFIC_USER = "specific_user"