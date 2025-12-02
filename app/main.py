"""
Main module for the application.

This module provides the FastAPI application and its lifespan.
"""

from contextlib import asynccontextmanager
from logging import getLogger
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.core.config import settings
from app.database.base_class import BaseModel as DBBaseModel
from app.database.db import async_engine

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Modern lifespan context manager for FastAPI application events.

    Handles startup and shutdown events using the recommended approach
    instead of deprecated @app.on_event decorators.
    """
    # Startup logic
    logger.info(  # type: ignore
        "Application startup initiated",
    )

    logger.info("Application startup completed")
    async with async_engine.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.create_all)

    yield

    # Shutdown logic
    logger.info("Application shutdown initiated")


main_app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description=settings.description,
    lifespan=lifespan,  # type: ignore[arg-type]
)


@main_app.get("/")
async def start() -> Dict[str, int]:
    return {"health check": 200}


main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_app.include_router(auth_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:main_app",
        host="0.0.0.0",
        port=settings.app_port,
        reload=settings.app_reload,
        reload_dirs=["main_app"],
    )
