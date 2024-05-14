from fastapi import APIRouter

from .short_urls import router as short_router

v1_router = APIRouter()

v1_router.include_router(short_router, tags=["shorter"])
