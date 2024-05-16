from sqlalchemy.orm import Session
from typing import TypeVar, List

from db.base import ModelBase
from schemas.base import BaseModel

ModelType = TypeVar("ModelType", bound=ModelBase)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseSelector:
    def __init__(self, model: ModelType):
        self.model = model

    def get(self, db: Session, id: int) -> ModelType:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, skip: int = None, limit: int = None
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()


class BaseService:
    def __init__(self, model: ModelType):
        self.model = model

    def create(self, db: Session, obj_in: SchemaType) -> ModelType:
        obj_data = obj_in.model_dump() if hasattr(obj_in, "model_dump") else obj_in

        db_obj = self.model(**obj_data)

        db.add(db_obj)
        db.commit()

        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: SchemaType) -> ModelType:
        obj_data = (
            obj_in.model_dump(exclude_unset=True, exclude_none=True)
            if hasattr(obj_in, "model_dump")
            else obj_in
        )

        for field, value in obj_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
            db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        obj = db.query(self.model).filter(self.model.id == id).first()
        db.delete(obj)
        db.commit()
        return obj
