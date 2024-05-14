from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.urls import UrlMappinngCreate, UrlMappingResponse

router = APIRouter()


@router.post("/shorten", response_model=UrlMappingResponse)
def create_short_key(url_in: UrlMappinngCreate, db=Depends(get_db)):
    pass


@router.get("/{shorten_key}", response_model=UrlMappingResponse)
def get_origin_url(shorten_key: str, db=Depends(get_db)):
    pass
