from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from config.database import get_db
from auth.dependencies import get_current_user
from files.models import FileMetadata
from storage.local import LocalStorage
import io

router = APIRouter()
storage = LocalStorage()

@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Get file metadata
    file_record = db.query(FileMetadata).filter(
        FileMetadata.id == file_id,
        FileMetadata.owner_id == current_user.id
    ).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if file exists in storage
    if not storage.file_exists(file_record.encrypted_path):
        raise HTTPException(status_code=404, detail="File data not found")
    
    try:
        # Retrieve and decrypt file
        file_data = storage.retrieve_file(file_record.encrypted_path)
        
        # Create streaming response
        file_stream = io.BytesIO(file_data)
        
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type=file_record.mime_type,
            headers={
                "Content-Disposition": f"attachment; filename={file_record.original_name}"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving file")

@router.get("/preview/{file_id}")
def preview_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Similar to download but for inline preview
    file_record = db.query(FileMetadata).filter(
        FileMetadata.id == file_id,
        FileMetadata.owner_id == current_user.id
    ).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Only allow preview for certain file types
    previewable_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'text/plain']
    if file_record.mime_type not in previewable_types:
        raise HTTPException(status_code=400, detail="File type not previewable")
    
    try:
        file_data = storage.retrieve_file(file_record.encrypted_path)
        
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type=file_record.mime_type,
            headers={
                "Content-Disposition": f"inline; filename={file_record.original_name}"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving file")