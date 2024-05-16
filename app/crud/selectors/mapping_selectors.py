from datetime import datetime
from sqlalchemy.orm import Session

from models import mapping_models
from exception.exceptions import ExpiredException


def get_url_by_key(db: Session, key: str):
    return (
        db.query(mapping_models.URLMapping)
        .filter(mapping_models.URLMapping.shorten_key == key)
        .first()
    )


def get_url_mapping(db: Session, url_mapping: mapping_models.URLMapping):

    if url_mapping.expire_date and url_mapping.expire_date < datetime.now().date():
        db.delete(url_mapping)
        db.commit()
        raise ExpiredException

    url_mapping.view_count += 1
    db.commit()

    return url_mapping
