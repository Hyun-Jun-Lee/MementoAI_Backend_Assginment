from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db

router = APIRouter()


@router.post("/shorten")
def create_short_key():
    pass


@router.get("/{shorten_key}")
def get_origin_url():
    pass
