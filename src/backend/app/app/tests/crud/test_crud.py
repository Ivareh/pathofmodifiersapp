import math
import pytest
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    Callable,
    Tuple,
)

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pydantic import BaseModel, TypeAdapter
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from app.crud.base import (
    CRUDBase,
    ModelType,
    SchemaType,
    CreateSchemaType,
    UpdateSchemaType,
)
from app.core.models.database import Base, engine


class TestCRUD:
    # def __init__(
    #     self, crud_instance: CRUDBase, object_generator_func: Callable[[], Dict]
    # ) -> None:
    #     self.crud_instance = crud_instance
    #     self.schema = crud_instance.schema
    #     self.object_generator_func = object_generator_func

    #     self.db = None

    # def setup_class(self):
    #     """
    #     Only used to get rid of IDE errors
    #     """
    #     Base.metadata.create_all(engine)
    #     self.db = Session()

    #     self.crud_instance: CRUDBase
    #     self.schema: SchemaType
    #     self.object_generator_func: Callable[[], Dict]

    # def teardown_class(self):
    #     self.db.rollback()
    #     self.db.close()

    @pytest.mark.asyncio
    async def _create_object(
        self,
        db,
        crud_instance,
        object_generator_func,
        *,
        # count: Optional[int] = None,
        main_key: Optional[str] = "",
        main_key_value: Optional[Any] = None,
    ) -> Tuple[Dict, CreateSchemaType, ModelType]:
        object_dict = object_generator_func()
        # createType: Type[CreateSchemaType] = CreateSchemaType

        if (
            main_key != "" and main_key_value is None
        ):  # If main_key is not None, then we need to get the value of the main_key
            main_key_value = object_dict[main_key]

        print("MAIN KEY VALUE CREATE: ", main_key_value)
        print("MAIN KEY CREATE: ", main_key)
        if (
            main_key_value is not None and main_key
        ):  # If main_key_value is not None, then we need to add it to the object_dict
            object_dict[main_key] = main_key_value

        object_in = crud_instance.create_schema(
            **object_dict
        )  # Map object_dict to the create_schema

        object_out = await crud_instance.create(
            db=db, obj_in=object_in
        )  # Create the object in the database

        # if main_key is not None:
        #     all_keys = [key.name for key in inspect(ModelType).primary_key]
        #     secondary_keys = [key for key in all_keys if key != main_key]
        #     for field in object_dict:

        # for field in object_keys:
        # print("OBJECT DICT: ", object_dict)
        # print("OBJECT OUT: ", object_out)
        print("HEYHEY", main_key_value)
        if main_key_value is not None:
            return object_dict, object_out, main_key_value
        else:
            return object_dict, object_out
        # return object_dict, object_in, object_out

    @pytest.mark.asyncio
    async def _test_object(
        self,
        object: Union[ModelType, List[ModelType]],
        compare_object: Optional[Union[Dict, List[Dict]]],
    ) -> None:
        assert object

        if compare_object is not None:
            if isinstance(object, List) and isinstance(compare_object, List):
                for obj, compare_obj in zip(object, compare_object):
                    await self._test_object(obj, compare_obj)

            else:
                assert not isinstance(object, List)
                assert isinstance(compare_object, Dict)
                for field in compare_object:
                    if isinstance(compare_object[field], float):
                        assert math.isclose(
                            compare_object[field], getattr(object, field), rel_tol=1e-3
                        )
                        continue
                    assert field in inspect(object).attrs
                    assert compare_object[field] == getattr(object, field)

    # async def test_get_main_key(self, db: Session, main_key: str) -> None:
    #     # object_dict, object_in, object_out = await self._create_object(db)
    #     object_dict, object_out = await self._create_object(db)

    #     object_map = {main_key: getattr(object_out, main_key)}
    #     stored_get_object = await self.crud_instance.get(db=db, filter=object_map)
    #     await self._test_object(stored_get_object, object_dict)

    @pytest.mark.asyncio
    async def test_get(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Dict],
    ) -> None:
        # object_dict, object_in, object_out = await self._create_object(
        #     db, crud_instance, object_generator_func
        # )
        object_dict, object_out = await self._create_object(
            db, crud_instance, object_generator_func
        )
        # object_dict = self.object_generator_func()
        # object_in = self.schema(**object_dict)
        # object_out = await crud_instance.create(db=db, obj_in=object_in)

        object_map = {
            key.name: getattr(object_out, key.name)
            for key in object_out.__table__.primary_key
        }
        print("OBJECT MAP: ", object_map)

        stored_get_object = await crud_instance.get(db=db, filter=object_map)

        await self._test_object(stored_get_object, object_dict)

    @pytest.mark.asyncio
    async def test_create(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Dict],
    ) -> None:
        object_dict, object_out = await self._create_object(
            db, crud_instance, object_generator_func
        )
        await self._test_object(object_out, object_dict)

    @pytest.mark.asyncio
    async def test_create_multiple(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Dict],
        main_key: Optional[str],
        count: int = 5,
    ) -> None:
        initial_object_count = len(await crud_instance.get(db))
        # object_dict, object_in, object_out = await self._create_object(
        #     db, crud_instance, object_generator_func, count=count, main_key=main_key
        # )

        multiple_object_dict = []
        multiple_object_out = []

        if main_key != "":
            main_object_dict, main_object_out, main_key_value = (
                await self._create_object(
                    db, crud_instance, object_generator_func, main_key=main_key
                )
            )  # Get the main_key_value to use for the rest of the objects
            multiple_object_dict.append(main_object_dict)
            multiple_object_out.append(main_object_out)
            main_key_object_count = 3
            for _ in range(
                main_key_object_count
            ):  # Invoke the main_key_value 3 times to test if it works for 3 objects with same main_key_value
                object_dict, object_out, new_main_key_value = await self._create_object(
                    db,
                    crud_instance,
                    object_generator_func,
                    main_key=main_key,
                    main_key_value=main_key_value,
                )
                multiple_object_dict.append(object_dict)
                multiple_object_out.append(object_out)

        for _ in range(count):
            object_dict, object_out = await self._create_object(
                db, crud_instance, object_generator_func
            )
            multiple_object_dict.append(object_dict)
            multiple_object_out.append(object_out)
        final_object_count = len(await crud_instance.get(db))
        if main_key != "":
            assert (
                final_object_count
                == initial_object_count + count + main_key_object_count + 1
            )  # +1 for the main_key_object
        else:
            assert final_object_count == initial_object_count + count
        await self._test_object(multiple_object_out, multiple_object_dict)
