import logging
import sys
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from presentation.routers.form_router import router as form_router
from presentation.routers.response_router import router as response_router
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
app = FastAPI(
    title="Flexible Multi-Language Feedback Form System",
    description="A clean architecture system for managing feedback forms with multi-language support.",
    version="1.0.0"
)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.warning(f"Value error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        }
    )
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if app.debug else "An error occurred"
        }
    )
app.include_router(form_router, prefix="/api/v1", tags=["forms"])
app.include_router(response_router, prefix="/api/v1", tags=["responses"])
@app.get("/")
def read_root():
    return {"message": "Welcome to the Feedback Form System API"}
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "feedback-form-system",
        "version": "1.0.0"
    }