# SecureShare Backend - FastAPI

Production-ready backend for SecureShare with JWT authentication, AES encryption, and modular architecture.

## 🚀 Quick Start

```bash
cd backend
python start.py
```

Server runs at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

## 📁 Architecture

```
backend/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Dependencies
├── config/
│   ├── settings.py        # Environment configuration
│   └── database.py        # SQLAlchemy setup
├── auth/
│   ├── models.py          # User models & schemas
│   ├── routes.py          # /auth endpoints
│   ├── service.py         # JWT & password logic
│   └── dependencies.py    # Auth middleware
├── files/
│   ├── models.py          # File metadata models
│   ├── routes.py          # /files endpoints
│   ├── service.py         # File validation & AI labels
│   └── encryption.py      # AES encryption
├── storage/
│   ├── interface.py       # Storage abstraction
│   ├── local.py           # Local filesystem storage
│   └── routes.py          # /storage download endpoints
├── permissions/
│   └── enums.py           # Role definitions
├── middleware/
│   └── cors.py            # CORS configuration
└── utils/
    └── crypto.py          # Encryption utilities
```

## 🔐 Security Features

- **JWT Authentication** - Secure token-based auth
- **AES File Encryption** - All files encrypted at rest
- **Password Hashing** - bcrypt for secure password storage
- **CORS Protection** - Configured for frontend origins
- **No Plaintext Storage** - Files always encrypted
- **Content-Addressed Storage** - IPFS-style hashing

## 📡 API Endpoints

### Authentication (`/auth`)

#### POST `/auth/signup`
```json
// Request
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "password123"
}

// Response
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "isVerified": true,
    "storageQuota": 10737418240,
    "createdAt": "2024-01-01T00:00:00"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### POST `/auth/login`
```json
// Request
{
  "email": "user@example.com",
  "password": "password123"
}

// Response (same as signup)
```

#### GET `/auth/me`
```json
// Headers: Authorization: Bearer <token>
// Response
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "isVerified": true,
  "storageQuota": 10737418240,
  "createdAt": "2024-01-01T00:00:00"
}
```

### Files (`/files`)

#### POST `/files/upload`
```json
// Form data: file (multipart/form-data)
// Headers: Authorization: Bearer <token>

// Response
{
  "success": true,
  "file": {
    "id": 1,
    "name": "document.pdf",
    "size": 1024000,
    "hash": "QmX1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s",
    "aiLabel": "📋 Document",
    "uploadedAt": "2024-01-01T00:00:00",
    "isPrivate": true
  }
}
```

#### GET `/files/my`
```json
// Headers: Authorization: Bearer <token>
// Response
[
  {
    "id": 1,
    "name": "document.pdf",
    "size": 1024000,
    "type": "application/pdf",
    "hash": "QmX1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s",
    "aiLabel": "📋 Document",
    "uploadedAt": "2024-01-01T00:00:00",
    "isPrivate": true
  }
]
```

#### DELETE `/files/{file_id}`
```json
// Headers: Authorization: Bearer <token>
// Response
{
  "success": true,
  "message": "File deleted successfully"
}
```

### Storage (`/storage`)

#### GET `/storage/download/{file_id}`
- Headers: `Authorization: Bearer <token>`
- Returns: Decrypted file stream
- Content-Disposition: attachment

#### GET `/storage/preview/{file_id}`
- Headers: `Authorization: Bearer <token>`
- Returns: Inline file preview (images, PDFs, text)
- Content-Disposition: inline

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# Security
SECRET_KEY=your-super-secret-jwt-key
ENCRYPTION_KEY=your-encryption-key

# Database
DATABASE_URL=sqlite:///./secureshare.db

# File Storage
MAX_FILE_SIZE=104857600  # 100MB

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Supported File Types

- **Images**: JPEG, PNG, GIF
- **Documents**: PDF, TXT, DOC, DOCX
- **Spreadsheets**: XLS, XLSX
- **Archives**: ZIP
- **Media**: MP4, MP3

Max file size: **100 MB**

## 🤖 AI Label Generation

Files are automatically labeled using intelligent pattern matching:

- **Filename patterns**: `report` → 📊 Financial Report
- **Content types**: `image/jpeg` → Photo, Graphic
- **Extensions**: `.pdf` → Text Document

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_verified BOOLEAN DEFAULT TRUE,
    storage_quota INTEGER DEFAULT 10737418240,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Files Table
```sql
CREATE TABLE files (
    id INTEGER PRIMARY KEY,
    owner_id INTEGER REFERENCES users(id),
    name VARCHAR NOT NULL,
    original_name VARCHAR NOT NULL,
    size INTEGER NOT NULL,
    mime_type VARCHAR NOT NULL,
    encrypted_path VARCHAR NOT NULL,
    content_hash VARCHAR UNIQUE NOT NULL,
    ai_label VARCHAR,
    is_private BOOLEAN DEFAULT TRUE,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Frontend Integration

Update your frontend services to use the backend:

```javascript
// authService.js
const API_BASE = 'http://localhost:8000';

export const login = async (credentials) => {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  return response.json();
};

// fileService.js
export const uploadFile = async (file, token) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE}/files/upload`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
  return response.json();
};
```

## 🚀 Deployment

### Development
```bash
python start.py
```

### Production
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔒 Security Considerations

### Production Checklist
- [ ] Change `SECRET_KEY` and `ENCRYPTION_KEY`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS/TLS
- [ ] Add rate limiting
- [ ] Implement file size quotas
- [ ] Add audit logging
- [ ] Use environment-specific CORS origins
- [ ] Add input sanitization
- [ ] Implement file virus scanning

### Current Security Features
✅ JWT token authentication
✅ Password hashing with bcrypt
✅ AES file encryption at rest
✅ CORS protection
✅ Input validation
✅ SQL injection protection (SQLAlchemy ORM)
✅ No plaintext file storage

## 🔄 Storage Abstraction

The storage layer is designed for easy replacement:

```python
# Current: Local encrypted storage
from storage.local import LocalStorage

# Future: IPFS integration
from storage.ipfs import IPFSStorage

# Future: AWS S3 with encryption
from storage.s3 import S3Storage
```

## 📊 Monitoring & Logging

Add these for production:

```python
import logging
from fastapi import Request
import time

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.3f}s")
    return response
```

## 🤝 Contributing

1. Follow the modular architecture
2. Add tests for new endpoints
3. Update API documentation
4. Ensure security best practices
5. Test with the React frontend

## 📄 License

MIT - Production ready for SecureShare hackathon and beyond.