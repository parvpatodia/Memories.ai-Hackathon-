from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from services.memories_api import memories_api
from models import UploadResponse
import os
from typing import List
import mimetypes

router = APIRouter(prefix="/api", tags=["upload"])

# Allowed video file types
ALLOWED_VIDEO_TYPES = [
    'video/mp4', 'video/avi', 'video/mov', 'video/quicktime',
    'video/wmv', 'video/flv', 'video/webm', 'video/mkv'
]

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def validate_video_file(file: UploadFile) -> None:
    """Validate uploaded video file"""
    
    # Check file type
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        # Also check by file extension as backup
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Supported formats: MP4, AVI, MOV, WMV, FLV, WebM, MKV"
            )
    
    # Check file size
    if file.size and file.size > MAX_FILE_SIZE:
        size_mb = file.size / (1024 * 1024)
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size_mb:.1f}MB). Maximum allowed size is 50MB."
        )
    
    # Check filename
    if not file.filename or len(file.filename.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )

@router.post("/upload", response_model=UploadResponse)
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a video file to Memories.ai for processing
    
    - **file**: Video file (MP4, AVI, MOV, etc.) - Max 50MB
    
    Returns upload confirmation with video ID for future operations
    """
    
    try:
        # Validate the uploaded file
        validate_video_file(file)
        
        # Get file info before upload (file.size might be None after reading)
        file_size = file.size or 0
        file_name = file.filename
        
        # Upload to Memories.ai
        result = await memories_api.upload_video(file)
        
        return UploadResponse(
            success=True,
            video_no=result["video_no"],
            message=result["message"],
            file_name=file_name,
            file_size=file_size
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Unexpected upload error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during upload"
        )

@router.get("/upload/status/{video_no}")
async def get_upload_status(video_no: str):
    """
    Get processing status for an uploaded video
    
    - **video_no**: Video ID returned from upload endpoint
    """
    # In a real implementation, you'd check Memories.ai API for status
    # For now, return mock status based on video ID pattern
    
    if video_no.startswith("mock_"):
        return {
            "video_no": video_no,
            "status": "completed",
            "message": "Video processed successfully (mock)",
            "processed_at": "2025-10-07T12:00:00Z"
        }
    else:
        return {
            "video_no": video_no,
            "status": "processing", 
            "message": "Video is being processed by AI",
            "estimated_completion": "2-5 minutes"
        }

# Health check for upload service
@router.get("/upload/health")
async def upload_health_check():
    """Health check for upload service"""
    return {
        "service": "upload",
        "status": "healthy",
        "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024),
        "allowed_types": ALLOWED_VIDEO_TYPES
    }
