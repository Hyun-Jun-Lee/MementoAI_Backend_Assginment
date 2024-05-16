import secrets
import hashlib
from datetime import date
from sqlalchemy.orm import Session

from models import mapping_models
from crud.selectors import mapping_selectors


def generate_url_hash(origin_url: str) -> str:
    return hashlib.sha256(origin_url.encode()).hexdigest()


def generate_random_key():
    return secrets.token_urlsafe(5)


def create_random_key(db: Session, origin_url: str) -> str:
    url_hash = generate_url_hash(origin_url)[:5]
    random_key = generate_random_key()
    short_key = f"{random_key}_{url_hash}"

    while mapping_selectors.get_url_by_key(db, short_key):
        random_key = generate_random_key()
        short_key = f"{random_key}_{url_hash}"

    return short_key


def create_mapping(db: Session, origin_url: str, expire_date: date = None):
    random_key = create_random_key(db=db, origin_url=origin_url)

    url_mapping = mapping_models.URLMapping(
        origin_url=origin_url, shorten_key=random_key, expire_date=expire_date
    )

    db.add(url_mapping)
    db.commit()
    return url_mapping
