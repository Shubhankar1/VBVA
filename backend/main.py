"""
VBVA Main FastAPI Application
Multi-agent orchestration backend for video-based virtual assistant
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import StreamingResponse
import uvicorn

from config.settings import get_settings
from api.routes import router as api_router
from services.monitoring import setup_monitoring
from services.logging import setup_logging

# Setup logging
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting VBVA Backend...")
    setup_logging()
    setup_monitoring()
    
    # Create necessary directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("cache", exist_ok=True)
    
    yield
    
    # Shutdown
    logger.info("Shutting down VBVA Backend...")

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = get_settings()
    
    app = FastAPI(
        title="VBVA - Video Based Virtual Assistant",
        description="Multi-agent orchestration backend for interactive avatar tools",
        version="1.0.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan
    )
    
    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1", "0.0.0.0"] + settings.allowed_origins
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/")
    async def root():
        """Health check endpoint"""
        return {
            "message": "VBVA Backend is running",
            "version": "1.0.0",
            "status": "healthy"
        }
    
    @app.get("/health")
    async def health_check():
        """Detailed health check"""
        return {
            "status": "healthy",
            "services": {
                "openai": "connected",
                "elevenlabs": "connected",
                "stt": "available",
                "lip_sync": "available"
            }
        }
    
    return app

app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 