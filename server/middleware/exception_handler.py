import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to catch all unhandled exceptions and return consistent HTTP 500 responses."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        try:
            # Process the request normally
            response = await call_next(request)
            return response
            
        except Exception as exc:
            # Log the exception with request details
            logger.error(
                f"Unhandled exception in {request.method} {request.url.path}: {str(exc)}",
                exc_info=True,
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "client_ip": request.client.host if request.client else "unknown"
                }
            )
            
            # Return a generic HTTP 500 response
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "error_type": "internal_error"
                }
            )
