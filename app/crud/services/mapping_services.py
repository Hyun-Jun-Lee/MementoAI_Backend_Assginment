from datetime import date
from sqlalchemy.orm import Session

from crud.base import BaseService
from models import mapping_models
from crud.utilities import create_random_key


class UrlMappingService(BaseService):

    def create_mapping(self, db: Session, origin_url: str, expire_date: date = None):
        random_key = create_random_key(db=db, origin_url=origin_url)

        url_mapping = mapping_models.URLMapping(
            origin_url=origin_url, shorten_key=random_key, expire_date=expire_date
        )

        db.add(url_mapping)
        db.commit()
        return url_mapping

    def increase_view_count(self, db: Session, url_mapping: mapping_models.URLMapping):
        url_mapping.view_count += 1
        db.commit()
        db.refresh(url_mapping)

        return url_mapping


mapping_service = UrlMappingService(mapping_models.URLMapping)
