from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from auth.models import UserCreate, UserLogin, UserResponse, Token
from auth.service import create_user, authenticate_user, create_access_token, get_user_by_email
from auth.dependencies import get_current_user

router = APIRouter()

@router.post("/signup", response_model=dict)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    db_user = create_user(db, user)
    
    # Create token
    access_token = create_access_token(data={"sub": db_user.email})
    
    return {
        "success": True,
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "isVerified": db_user.is_verified,
            "storageQuota": db_user.storage_quota,
            "createdAt": db_user.created_at.isoformat()
        },
        "token": access_token
    }

@router.post("/login", response_model=dict)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "success": True,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "isVerified": user.is_verified,
            "storageQuota": user.storage_quota,
            "createdAt": user.created_at.isoformat()
        },
        "token": access_token
    }

@router.get("/me", response_model=dict)
def get_current_user_info(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "isVerified": current_user.is_verified,
        "storageQuota": current_user.storage_quota,
        "createdAt": current_user.created_at.isoformat()
    }