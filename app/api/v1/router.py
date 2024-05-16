from fastapi import APIRouter

from .url_mapping import router as mapping_router

v1_router = APIRouter()

v1_router.include_router(mapping_router, tags=["shorter"])
