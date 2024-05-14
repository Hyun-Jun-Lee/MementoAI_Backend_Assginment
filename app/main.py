from fastapi import FastAPI

from core.config import settings
from api.v1.router import v1_router

app = FastAPI(
    title=settings.PJ_TITLE,
)

app.include_router(v1_router, prefix="/v1")
