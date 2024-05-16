from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.mapping_schemas import (
    UrlMappingCreate,
    UrlMappingResponse,
    UrlMappingUpdate,
)
from exception.exceptions import ExpiredException
from crud import mapping_selector, mapping_service

router = APIRouter()


@router.get("/shortens", response_model=List[UrlMappingResponse])
def get_all_mappings(db: Session = Depends(get_db)):
    """
    모든 Url Mapping 객체 확인
    """
    url_mappings = mapping_selector.get_multi(db=db)

    return url_mappings


@router.patch("/shorten/{shorten_key}", response_model=UrlMappingResponse)
def update_mapping(
    shorten_key: str, update_in: UrlMappingUpdate, db: Session = Depends(get_db)
):
    """
    주어진 shorten_key에 해당하는 URL 매핑의 만료일을 업데이트

    - Parameters:
        - shorten_key (str): 업데이트하고자 하는 URL 매핑의 shorten_key.
        - update_in : 업데이트할 정보를 담고 있는 Pydantic 모델(expire_date)

    - Raises:
        - 단축 Key에 해당하는 URL이 없을 경우 404 에러 반환

    - Returns:
        - UrlMappingResponse: 원본 URL, 단축 Key, 만료 날짜, 조회수를 포함하는 응답 모델
    """

    check_url_mapping = mapping_selector.get_url_by_key(db=db, key=shorten_key)

    if not check_url_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL Not Found"
        )

    updated_url_mapping = mapping_service.update(
        db=db, db_obj=check_url_mapping, obj_in=update_in
    )

    return updated_url_mapping


@router.post("/shorten", response_model=UrlMappingResponse)
def create_short_key(url_in: UrlMappingCreate, db: Session = Depends(get_db)):
    """
    원본 URL 받아서 UrlMapping 객체 생성 및 단축 Key를 반환

    - Parameters:
        - url_in : 원본 URL 및 만료 기간

    - Returns:
        - UrlMappingResponse: 원본 URL, 단축 Key, 만료 날짜, 조회수를 포함하는 응답 모델
    """
    url_mapping = mapping_service.create_mapping(
        db=db, origin_url=url_in.origin_url, expire_date=url_in.expire_date
    )

    return url_mapping


@router.get("/{shorten_key}", response_model=UrlMappingResponse)
def get_origin_url(shorten_key: str, db: Session = Depends(get_db)):
    """
    단축 Key를 받아서 원본 URL로 리다이렉트
    해당 UrlMapping 객체 조회수 증가

    - Parameters:
        - shorten_key : 단축 Key

    - Raises:
        - 단축 Key에 해당하는 URL이 없을 경우 404
        - 유효기간이 만료된 경우 404

    - Returns:
        - UrlMappingResponse: 원본 URL, 단축 Key, 만료 날짜, 조회수를 포함하는 응답 모델
    """
    check_url_mapping = mapping_selector.get_url_by_key(db=db, key=shorten_key)
    if not check_url_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL Not Found"
        )

    try:
        url_mapping = mapping_selector.get_url_mapping(
            db=db, url_mapping=check_url_mapping
        )
        mapping_service.increase_view_count(db=db, url_mapping=url_mapping)
    except ExpiredException:
        mapping_service.delete(db=db, id=check_url_mapping.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL has expired"
        )

    headers = {"Cache-Control": "no-cache, no-store, pragma: no-cache"}
    return RedirectResponse(
        url=url_mapping.origin_url,
        headers=headers,
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )


@router.get("/stats/{shorten_key}", response_model=UrlMappingResponse)
def get_view_count(shorten_key: str, db: Session = Depends(get_db)):
    """
    단축 Key 받아서 해당 key의 조회 수 확인

    - Parameters:
        - shorten_key : 단축 Key

    - Raises:
        - 단축 Key에 해당하는 URL이 없을 경우 404 에러 반환

    - Returns:
        - UrlMappingResponse: 원본 URL, 단축 URL, 만료 날짜, 조회수를 포함하는 응답 모델
    """

    url_mapping = mapping_selector.get_url_by_key(db=db, key=shorten_key)

    if not url_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL Not Found"
        )

    return url_mapping
