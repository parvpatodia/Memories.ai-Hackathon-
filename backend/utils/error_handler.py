from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from datetime import datetime
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ErrorHandler:
    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions with detailed logging"""
        logger.warning(f"HTTP {exc.status_code}: {exc.detail} - Path: {request.url.path}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "status_code": exc.status_code,
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path)
            }
        )
    
    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors with user-friendly messages"""
        errors = []
        for error in exc.errors():
            field = " -> ".join([str(loc) for loc in error["loc"]])
            message = error["msg"]
            errors.append(f"{field}: {message}")
        
        error_message = "Invalid input data: " + "; ".join(errors)
        
        logger.warning(f"Validation error: {error_message} - Path: {request.url.path}")
        
        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "message": error_message,
                "status_code": 422,
                "timestamp": datetime.now().isoformat(),
                "details": exc.errors()
            }
        )
    
    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions"""
        error_id = f"err_{int(datetime.now().timestamp())}"
        
        logger.error(f"Unexpected error {error_id}: {str(exc)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "An unexpected error occurred. Please try again later.",
                "status_code": 500,
                "error_id": error_id,
                "timestamp": datetime.now().isoformat()
            }
        )

# Rate limiting helper
class RateLimiter:
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """Simple in-memory rate limiting"""
        now = datetime.now().timestamp()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key] 
            if now - req_time < window_seconds
        ]
        
        # Check if limit exceeded
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True

rate_limiter = RateLimiter()
