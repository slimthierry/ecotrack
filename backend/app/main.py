from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.loggers import setup_logging
from app.routes import app_router
from app.config.database import engine
from app.config.redis import close_redis
from app.models.base import Base
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    # Startup: create tables if they don't exist (dev convenience)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed achievements
    from app.config.database import async_session_factory
    from app.services.achievement_service import seed_achievements

    async with async_session_factory() as session:
        await seed_achievements(session)
        await session.commit()

    yield

    # Shutdown: close connections
    await engine.dispose()
    await close_redis()
app = FastAPI(
    title="EcoTrack API",
    description="Carbon footprint tracker with gamification. Track your activities, join challenges, and earn achievements.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(v1_router, prefix="/api/v1")
@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "ecotrack-api", "version": "1.0.0"}
