from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ListCreateSchemaType = TypeVar("ListCreateSchemaType", bound=List[BaseModel])
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ListUpdateSchemaType = TypeVar("ListUpdateSchemaType", bound=List[BaseModel])


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if db_obj is None:
            raise HTTPException(
                status_code=404, detail=f"Object in {type(self.model)} not found"
            )
        return db_obj
    
    def get_all(self, db: Session) -> List[ModelType]:
        db_all_obj = db.query(self.model).all()
        if db_all_obj is None:
            raise HTTPException(
                status_code=404, detail=f"All objects in {type(self.model)} not found"
            )
        return db_all_obj

    def create(
        self, db: Session, *, obj_in: Union[CreateSchemaType, ListCreateSchemaType]
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, ListUpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # update_data = obj_in.dict(exclude_unset=True)
            update_data = obj_in.model_dump()
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        if obj is None:
            raise HTTPException(
                status_code=404, detail=f"Object in {type(self.model)} not found"
            )
        db.delete(obj)
        db.commit()
        return obj
