import secrets
import hashlib
from sqlalchemy.orm import Session

from crud import mapping_selector


def generate_url_hash(origin_url: str) -> str:
    return hashlib.sha256(origin_url.encode()).hexdigest()


def generate_random_key():
    return secrets.token_urlsafe(5)


def create_random_key(db: Session, origin_url: str) -> str:
    url_hash = generate_url_hash(origin_url)[:5]
    random_key = generate_random_key()
    short_key = f"{random_key}_{url_hash}"

    while mapping_selector.get_url_by_key(db, short_key):
        random_key = generate_random_key()
        short_key = f"{random_key}_{url_hash}"

    return short_key
