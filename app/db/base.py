from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative


@as_declarative()
class ModelBase:
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_time = Column(DateTime, default=func.now(), nullable=True)
    modified_time = Column(DateTime, default=None, onupdate=func.now(), nullable=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
