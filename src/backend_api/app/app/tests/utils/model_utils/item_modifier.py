import asyncio
from typing import Dict, Tuple, Union, List, Optional
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import (
    ItemModifier,
    Stash,
    Account,
    ItemBaseType,
    Currency,
    Item,
    Modifier,
)
from app.core.schemas.item_modifier import ItemModifierCreate
from app.tests.utils.utils import random_float

from app.tests.utils.model_utils.item import generate_random_item
from app.tests.utils.model_utils.modifier import generate_random_modifier


async def create_random_item_modifier_dict(
    db: Session, retrieve_dependencies: Optional[bool] = False
) -> Union[
    Dict,
    Tuple[
        Dict,
        Optional[
            List[Union[Dict, Stash, Account, ItemBaseType, Currency, Item, Modifier]]
        ],
    ],
]:
    """Create a random item modifier dictionary.

    Args:
        db (Session): DB session.
        retrieve_dependencies (Optional[bool]): Whether to retrieve dependencies. Defaults to False.

    Returns:
        Union[ Dict, Tuple[ Dict, Optional[ List[Union[Dict, Stash, Account, ItemBaseType, Currency, Item, Modifier]] ], ], ]: \n
        Random item modifier dictionary or tuple with random item modifier dictionary and dependencies.
    """
    roll_value = random_float()

    # Set the dependencies
    if not retrieve_dependencies:
        item_dict, item = await generate_random_item(db)
    else:
        item_dict, item, deps = await generate_random_item(
            db, retrieve_dependencies=retrieve_dependencies
        )
    itemId = item.itemId
    modifier_dict, modifier = await generate_random_modifier(db)
    modifierId = modifier.modifierId
    position = modifier.position

    item_modifier_dict = {
        "itemId": itemId,
        "modifierId": modifierId,
        "position": position,
        "roll": roll_value,
    }
    if not retrieve_dependencies:
        return item_modifier_dict
    else: # Gather dependencies and return
        deps += [item_dict, item, modifier_dict, modifier]
        return item_modifier_dict, deps


async def generate_random_item_modifier(
    db: Session, retrieve_dependencies: Optional[bool] = False
) -> Tuple[
    Dict,
    ItemModifier,
    Optional[List[Union[Dict, Stash, Account, ItemBaseType, Currency, Item, Modifier]]],
]:
    """Generate a random item modifier.

    Args:
        db (Session): DB session.
        retrieve_dependencies (Optional[bool], optional): Whether to retrieve dependencies. Defaults to False.

    Returns:
        Tuple[ Dict, ItemModifier, Optional[List[Union[Dict, Stash, Account, ItemBaseType, Currency, Item, Modifier]]], ]: \n
        Random item modifier dictionary, ItemModifier db object and optional dependencies.
    """
    output = await create_random_item_modifier_dict(db, retrieve_dependencies)
    if not retrieve_dependencies:
        item_modifier_dict = output
    else:
        item_modifier_dict, deps = output
    item_modifier_create = ItemModifierCreate(**item_modifier_dict)
    item_modifier = await crud.CRUD_itemModifier.create(db, obj_in=item_modifier_create)

    if not retrieve_dependencies:
        return item_modifier_dict, item_modifier
    else:
        return item_modifier_dict, item_modifier, deps
