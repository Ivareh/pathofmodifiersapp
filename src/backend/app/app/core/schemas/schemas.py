import datetime as _dt
from typing import Optional
import pydantic as _pydantic
from pydantic import Json


class _BaseCurrency(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    currencyId: int
    currencyName: str
    valueInChaos: float
    iconUrl: str


class Currency(_BaseCurrency):
    createdAt: Optional[_dt.datetime]

    class Config:
        from_attributes = True


class CreateCurrency(_BaseCurrency):
    pass


class _BaseItemBaseType(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    baseType: str
    category: str
    subCategory: Json


class ItemBaseType(_BaseItemBaseType):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        from_attributes = True


class CreateItemBaseType(_BaseItemBaseType):
    pass


class _BaseItem(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    itemId: int
    gameItemId: str
    stashId: str
    name: Optional[str]
    iconUrl: Optional[str]
    league: str
    typeLine: str
    baseType: str
    rarity: str
    identified: bool
    itemLevel: int
    forumNote: Optional[str]
    currencyAmount: Optional[float]
    currencyName: Optional[str]
    corrupted: Optional[bool]
    delve: Optional[bool]
    fractured: Optional[bool]
    synthesized: Optional[bool]
    replica: Optional[bool]
    elder: Optional[bool]
    shaper: Optional[bool]
    influences: Optional[Json]
    searing: Optional[bool]
    tangled: Optional[bool]
    isRelic: Optional[bool]
    prefixes: Optional[int]
    suffixes: Optional[int]
    foilVariation: Optional[int]
    inventoryId: Optional[str]


class Item(_BaseItem):
    createdAt: Optional[_dt.datetime]

    class Config:
        from_attributes = True


class CreateItem(_BaseItem):
    pass


class _BaseModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    modifierId: int
    position: int
    minRoll: float
    maxRoll: float
    textRoll: str
    static: Optional[bool]
    effect: str
    regex: Optional[str]
    implicit: Optional[bool]
    explicit: Optional[bool]
    delve: Optional[bool]
    fractured: Optional[bool]
    synthesized: Optional[bool]
    corrupted: Optional[bool]
    enchanted: Optional[bool]
    veiled: Optional[bool]


class Modifier(_BaseModifier):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        from_attributes = True


class CreateModifier(_BaseModifier):
    pass


class _BaseItemModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    itemId: int
    gameItemId: str
    modifierId: int
    position: int
    range: float


class ItemModifier(_BaseItemModifier):

    class Config:
        from_attributes = True


class CreateItemModifier(_BaseItemModifier):
    pass


class _BaseStash(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    stashId: str
    accountName: str
    public: bool
    league: str


class Stash(_BaseStash):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        from_attributes = True


class CreateStash(_BaseStash):
    pass


class _BaseAccount(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    accountName: str
    isBanned: Optional[bool]


class Account(_BaseAccount):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        from_attributes = True


class CreateAccount(_BaseAccount):
    pass
