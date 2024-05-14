from pydantic import BaseModel, HttpUrl, Field
from datetime import date
from typing import Optional

from .base import CoreSchema


class UrlMappingBase(CoreSchema):
    origin_url: HttpUrl
    short_url: str
    expire_date: Optional[date] = None
    view_count: Optional[int] = 0


class UrlMappinngCreate(BaseModel):
    origin_url: HttpUrl = Field(..., example="https://www.example_url.com/")
    expire_date: Optional[date] = None


class UrlMappingResponse(UrlMappingBase):
    pass
