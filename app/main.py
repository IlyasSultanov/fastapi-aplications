"""
Main module for the application.

This module provides the FastAPI application and its lifespan.
"""

from contextlib import asynccontextmanager
from logging import getLogger
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

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

    yield

    # Shutdown logic
    logger.info("Application shutdown initiated")


main_app = FastAPI(lifespan=lifespan)  # type: ignore


@main_app.get("/")
async def start() -> Dict[str, str]:
    return {"hello": "world"}


main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:main_app",
        host="0.0.0.0",
        port=settings.app_port,
        reload=settings.app_reload,  # type: ignore
        reload_dirs=["main_app"],
    )
