from sqlalchemy import Column, String, Integer, DATE


from db.base import ModelBase


class URLMapping(ModelBase):
    __tablename__ = "url_mapping"

    origin_url = Column(String, unique=True)
    shorten_key = Column(String, unique=True)
    view_count = Column(Integer, default=0)
    expire_date = Column(DATE, nullable=True)
