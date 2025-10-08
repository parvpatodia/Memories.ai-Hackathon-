from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TrackedObjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Object name")
    alias: str = Field(..., min_length=1, max_length=500, description="Object description/aliases")

class TrackedObject(BaseModel):
    id: int
    name: str
    alias: str
    last_seen_timestamp: Optional[int] = None
    location_phrase: Optional[str] = None
    video_no: Optional[str] = None
    confidence: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=200)

class SearchResult(BaseModel):
    found: bool
    location: Optional[str] = None
    timestamp: Optional[int] = None
    video_no: Optional[str] = None
    confidence: Optional[float] = None
    message: Optional[str] = None
    object_info: Optional[TrackedObject] = None

class UploadResponse(BaseModel):
    success: bool
    video_no: str
    message: str
    file_name: str
    file_size: int

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class ProcessingStatus(str, Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"