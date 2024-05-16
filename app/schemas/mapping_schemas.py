from pydantic import BaseModel, HttpUrl, Field
from datetime import date
from typing import Optional

from .base import CoreSchema


class UrlMappingBase(CoreSchema):
    origin_url: str
    shorten_key: str
    expire_date: Optional[date] = None
    view_count: Optional[int] = 0


class UrlMappingCreate(BaseModel):
    origin_url: str = Field(..., example="https://www.example_url.com/")
    expire_date: Optional[date] = None


class UrlMappingUpdate(BaseModel):
    expire_date: Optional[date] = None


class UrlMappingResponse(UrlMappingBase):
    pass
