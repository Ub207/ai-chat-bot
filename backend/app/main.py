from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import engine, Base
from app.routers import auth, todos


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Cleanup if needed
    await engine.dispose()


app = FastAPI(
    title="Todo API",
    description="A production-ready Todo API with authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(todos.router, prefix="/api/todos", tags=["Todos"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Todo API is running"}


@app.get("/")
async def root():
    return {
        "name": "Todo Full Stack API",
        "version": "1.0.0",
        "docs": "/docs",
    }
