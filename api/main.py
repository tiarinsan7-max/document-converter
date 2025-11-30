"""
FastAPI Main Application
Document Converter REST API
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import time
from config.settings import settings
from utils.logger import get_logger
from utils.errors import ConverterError
from .routes import router

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"- Status: {response.status_code} - Time: {process_time:.2f}s"
    )
    
    # Add custom header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Global exception handler
@app.exception_handler(ConverterError)
async def converter_error_handler(request: Request, exc: ConverterError):
    """Handle converter errors"""
    logger.error(f"Converter error: {exc}")
    return JSONResponse(
        status_code=400,
        content=exc.to_dict()
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "details": str(exc)
        }
    )


# Include routers
app.include_router(router, prefix="/api/v1", tags=["conversion"])


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"API documentation available at: /docs")
    logger.info(f"Supported formats: {', '.join(['pdf', 'docx', 'xlsx', 'csv', 'json', 'txt'])}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down application")
    
    # Cleanup temporary files
    from utils.file_handler import FileHandler
    handler = FileHandler()
    handler.cleanup_temp_files(max_age_hours=0)


# Root endpoint
@app.get("/")
async def root():
    """API root"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "status": "running",
        "docs": "/docs",
        "api": "/api/v1"
    }


# Health check
@app.get("/health")
async def health():
    """Simple health check"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
