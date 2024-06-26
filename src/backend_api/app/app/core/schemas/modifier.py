import datetime as _dt
from typing import List, Optional, Union
import pydantic as _pydantic


# Shared modifier props
class _BaseModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    position: int
    minRoll: Optional[float] = None
    maxRoll: Optional[float] = None
    textRolls: Optional[str] = None
    static: Optional[bool] = None
    effect: str
    regex: Optional[str] = None
    implicit: Optional[bool] = None
    explicit: Optional[bool] = None
    delve: Optional[bool] = None
    fractured: Optional[bool] = None
    synthesized: Optional[bool] = None
    unique: Optional[bool] = None
    corrupted: Optional[bool] = None
    enchanted: Optional[bool] = None
    veiled: Optional[bool] = None


class GroupedModifierByEffect(_pydantic.BaseModel):
    modifierId: List[int]
    position: List[int]
    minRoll: List[Union[float, None]]
    maxRoll: List[Union[float, None]]
    textRolls: List[Union[str, None]]
    effect: str
    static: List[Union[bool, None]]


# Properties to receive on modifier creation
class ModifierCreate(_BaseModifier):
    modifierId: Optional[int] = None


# Properties to receive on update
class ModifierUpdate(_BaseModifier):
    pass


# Properties shared by models stored in DB
class ModifierInDBBase(_BaseModifier):
    modifierId: int
    createdAt: _dt.datetime
    updatedAt: Optional[_dt.datetime] = None


# Properties to return to client
class Modifier(ModifierInDBBase):
    pass


# Properties stored in DB
class ModifierInDB(ModifierInDBBase):
    pass
