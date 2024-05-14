from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.urls import UrlMappinngCreate, UrlMappingResponse

router = APIRouter()


@router.post("/shorten", response_model=UrlMappingResponse)
def create_short_key(url_in: UrlMappinngCreate, db=Depends(get_db)):
    """
    원본 URL 받아서 단축 URL을 반환

    - Parameters:
        - url_in : 원본 URL 및 만료 기간

    - Returns:
        - UrlMappingResponse: 원본 URL, 단축 URL, 만료 날짜, 조회수를 포함하는 응답 모델
    """
    pass


@router.get("/{shorten_key}", response_model=UrlMappingResponse)
def get_origin_url(shorten_key: str, db=Depends(get_db)):
    """
    단축 URL을 받아서 원본 URL 반환

    - Parameters:
        - shorten_key : 단축 url 키

    - Returns:
        - UrlMappingResponse: 원본 URL, 단축 URL, 만료 날짜, 조회수를 포함하는 응답 모델
    """

    pass
