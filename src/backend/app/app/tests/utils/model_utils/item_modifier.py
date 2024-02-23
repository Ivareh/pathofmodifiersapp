from typing import List

from sqlalchemy import func
from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import ItemModifier
from app.core.schemas.item_modifier import ItemModifierCreate
from backend.app.app.tests.utils.utils import random_lower_string
from backend.app.app.tests.utils.utils import random_int


async def create_random_item_modifier(db: Session) -> ItemModifier:
    itemId = random_int()
    gameItemId = random_lower_string()
    modifierId = random_int()
    position = random_int()
    range_value = random_int()

    item_modifier = ItemModifierCreate(
        itemId=itemId,
        gameItemId=gameItemId,
        modifierId=modifierId,
        position=position,
        range=range_value,
    )

    return await crud.CRUD_itemModifier.create(db, obj_in=item_modifier)

def create_random_item_modifier_list(db: Session, count: int = 10) -> List[ItemModifier]:
    return [create_random_item_modifier(db) for _ in range(count)]


async def get_random_item_modifier(session: Session) -> ItemModifier:
    random_item_modifier = session.query(ItemModifier).order_by(func.random()).first()

    if random_item_modifier:
        print(
            f"Found already existing item_modifier. random_item_modifier.itemId: {random_item_modifier.itemId}"
        )
    else:
        random_item_modifier = create_random_item_modifier(session)
    return random_item_modifier