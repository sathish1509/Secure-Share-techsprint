from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from auth.dependencies import get_current_user
from files.models import FileMetadata, FileUploadResponse, FileListResponse
from files.service import (
    validate_file, generate_content_hash, generate_ai_label,
    save_encrypted_file, get_user_files, delete_file
)

router = APIRouter()

@router.post("/upload", response_model=dict)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Validate file
    validation_result = validate_file(file)
    file_data = validation_result['data']
    
    # Generate metadata
    content_hash = generate_content_hash(file_data)
    ai_label = generate_ai_label(file.filename, validation_result['category'])
    
    # Check for duplicates
    existing_file = db.query(FileMetadata).filter(
        FileMetadata.content_hash == content_hash,
        FileMetadata.owner_id == current_user.id
    ).first()
    
    if existing_file:
        raise HTTPException(
            status_code=400,
            detail="File already exists"
        )
    
    # Save encrypted file
    encrypted_path = save_encrypted_file(file_data, file.filename, current_user.id)
    
    # Save metadata to database
    file_record = FileMetadata(
        owner_id=current_user.id,
        name=file.filename,
        original_name=file.filename,
        size=validation_result['size'],
        mime_type=file.content_type,
        encrypted_path=encrypted_path,
        content_hash=content_hash,
        ai_label=ai_label
    )
    
    db.add(file_record)
    db.commit()
    db.refresh(file_record)
    
    return {
        "success": True,
        "file": {
            "id": file_record.id,
            "name": file_record.name,
            "size": file_record.size,
            "hash": file_record.content_hash,
            "aiLabel": file_record.ai_label,
            "uploadedAt": file_record.upload_date.isoformat(),
            "isPrivate": file_record.is_private
        }
    }

@router.get("/my", response_model=List[dict])
def get_my_files(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    files = get_user_files(db, current_user.id)
    return [
        {
            "id": f.id,
            "name": f.name,
            "size": f.size,
            "type": f.mime_type,
            "hash": f.content_hash,
            "aiLabel": f.ai_label,
            "uploadedAt": f.upload_date.isoformat(),
            "isPrivate": f.is_private
        }
        for f in files
    ]

@router.delete("/{file_id}")
def delete_user_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = delete_file(db, file_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    
    return {"success": True, "message": "File deleted successfully"}

@router.get("/shared")
def get_shared_files(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # TODO: Implement shared files logic
    return []