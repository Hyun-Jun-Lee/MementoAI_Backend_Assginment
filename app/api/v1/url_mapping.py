from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.mapping_schemas import UrlMappingCreate, UrlMappingResponse
from exception.exceptions import ExpiredException
from crud.services import mapping_services
from crud.selectors import mapping_selectors

router = APIRouter()


@router.post("/shorten", response_model=UrlMappingResponse)
def create_short_key(url_in: UrlMappingCreate, db=Depends(get_db)):
    """
    원본 URL 받아서 단축 Key를 반환

    - Parameters:
        - url_in : 원본 URL 및 만료 기간

    - Returns:
        - UrlMappingResponse: 원본 URL, 단축 Key, 만료 날짜, 조회수를 포함하는 응답 모델
    """
    url_mapping = mapping_services.create_mapping(
        db=db, origin_url=url_in.origin_url, expire_date=url_in.expire_date
    )

    return url_mapping


@router.get("/{shorten_key}", response_model=UrlMappingResponse)
def get_origin_url(shorten_key: str, db=Depends(get_db)):
    """
    단축 Key를 받아서 원본 URL 반환

    - Parameters:
        - shorten_key : 단축 Key

    - Returns:
        - UrlMappingResponse: 원본 URL, 단축 Key, 만료 날짜, 조회수를 포함하는 응답 모델
    """
    check_url_mapping = mapping_selectors.get_url_by_key(db=db, key=shorten_key)

    if not check_url_mapping:
        raise HTTPException(status_code=404, detail="URL Not Found")
    try:
        url_mapping = mapping_selectors.get_url_mapping(
            db=db, url_mapping=check_url_mapping
        )
        mapping_services.increase_view_count(db=db, url_mapping=url_mapping)
    except ExpiredException:
        raise HTTPException(status_code=404, detail="URL has expired")

    return RedirectResponse(url=url_mapping.origin_url, status_code=301)


@router.get("/stats/{shorten_key}", response_model=UrlMappingResponse)
def get_view_count(shorten_key: str, db=Depends(get_db)):
    """
    단축 Key 받아서 원본 URL 반환

    - Parameters:
        - shorten_key : 단축 Key

    - Returns:
        - UrlMappingResponse: 원본 URL, 단축 URL, 만료 날짜, 조회수를 포함하는 응답 모델
    """

    url_mapping = mapping_selectors.get_url_by_key(db=db, key=shorten_key)

    if not url_mapping:
        raise HTTPException(status_code=404, detail="URL Not Found")

    return url_mapping
