"""Main FastAPI application entry point."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.db.connection import close_db, init_db
from src.api.routes import todos


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title="Todo API",
    description="A REST API for managing todo items with CRUD operations",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(todos.router, prefix=settings.API_V1_PREFIX)


@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Returns the health status of the API.",
)
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "message": "Todo API is running"}


@app.get(
    "/",
    tags=["root"],
    summary="API root",
    description="Returns API information.",
)
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "name": "Todo API",
        "version": "1.0.0",
        "docs": "/docs",
    }
