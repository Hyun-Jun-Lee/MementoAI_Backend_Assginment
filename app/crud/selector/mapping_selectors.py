from datetime import datetime
from sqlalchemy.orm import Session

from app.models import mapping_models as url_model
from exception.exceptions import ExpiredException


def get_url_by_key(db: Session, key: str):
    return (
        db.query(url_model.URLMapping)
        .filter(url_model.URLMapping.shorten_key == key)
        .first()
    )


def get_url_mapping(db: Session, key: str):
    url_mapping = get_url_by_key(db=db, key=key)

    if not url_mapping:
        raise ValueError

    if url_mapping.expire_date and url_mapping.expire_date < datetime.now():
        raise ExpiredException

    url_mapping.view_count += 1
    db.commit()

    return url_mapping
