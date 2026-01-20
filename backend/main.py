from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, Base
from config.settings import settings
from auth.routes import router as auth_router
from files.routes import router as files_router
from storage.routes import router as storage_router
from middleware.cors import add_cors_middleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SecureShare Backend",
    description="Privacy-first file sharing with encryption",
    version="1.0.0"
)

# Add CORS middleware
add_cors_middleware(app)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(files_router, prefix="/files", tags=["Files"])
app.include_router(storage_router, prefix="/storage", tags=["Storage"])

@app.get("/")
def health_check():
    return {
        "status": "SecureShare backend running",
        "version": "1.0.0",
        "features": ["JWT Auth", "AES Encryption", "File Upload", "Secure Download"]
    }
