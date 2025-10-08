from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
import uvicorn
from dotenv import load_dotenv
import os

# Import routers and utilities
from routers import upload, objects, search, admin
from utils.error_handler import ErrorHandler

load_dotenv()

app = FastAPI(
    title="Object Finder API",
    description="AI-powered object location service using Memories.ai",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add exception handlers
app.add_exception_handler(HTTPException, ErrorHandler.http_exception_handler)
app.add_exception_handler(RequestValidationError, ErrorHandler.validation_exception_handler)
app.add_exception_handler(Exception, ErrorHandler.general_exception_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(objects.router)
app.include_router(search.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {
        "message": "Object Finder API is running!",
        "docs": "Visit /docs for API documentation",
        "health": "Visit /health for health check",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        from database import db
        await db.get_tracked_objects()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "service": "object-finder-api",
        "version": "1.0.0",
        "database": db_status,
        "endpoints": {
            "upload": "/api/upload",
            "objects": "/api/objects",
            "search": "/api/search",
            "health": "/health",
            "docs": "/docs"
        },
        "timestamp": "2025-10-13T12:00:00Z"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
