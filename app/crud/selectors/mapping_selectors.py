from datetime import datetime
from sqlalchemy.orm import Session

from exception.exceptions import ExpiredException
from models import mapping_models
from crud.base import BaseSelector


class UrlMappingSelector(BaseSelector):

    def get_url_by_key(self, db: Session, key: str):
        return db.query(self.model).filter(self.model.shorten_key == key).first()

    def get_url_mapping(self, db: Session, url_mapping: mapping_models.URLMapping):

        if url_mapping.expire_date and url_mapping.expire_date < datetime.now().date():
            raise ExpiredException

        return url_mapping


mapping_selector = UrlMappingSelector(mapping_models.URLMapping)
