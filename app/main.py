from fastapi import FastAPI

from core.config import settings

app = FastAPI(
    title=settings.PJ_TITLE,
)
