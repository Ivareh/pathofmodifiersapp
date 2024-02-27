from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Union

from app.api.deps import get_db

from app.crud import CRUD_stash

import app.core.schemas as schemas

from sqlalchemy.orm import Session


router = APIRouter()


@router.get(
    "/{stashId}",
    response_model=Union[schemas.Stash, List[schemas.Stash]],
)
async def get_stash(stashId: str, db: Session = Depends(get_db)):
    """
    Get stash by "stashId".
    """
    stash_map = {"stashId": stashId}
    stash = await CRUD_stash.get(db=db, filter=stash_map)

    return stash


@router.get("/", response_model=Union[schemas.Stash, List[schemas.Stash]])
async def get_all_stashes(db: Session = Depends(get_db)):
    """
    Get all stashes.
    """
    all_stashes = await CRUD_stash.get(db=db)

    return all_stashes


@router.post(
    "/",
    response_model=Union[schemas.StashCreate, List[schemas.StashCreate]],
)
async def create_stash(
    stash: Union[schemas.StashCreate, List[schemas.StashCreate]],
    db: Session = Depends(get_db),
):
    """
    Create a new stash.
    """
    return await CRUD_stash.create(db=db, obj_in=stash)


@router.put("/{stashId}", response_model=schemas.Stash)
async def update_stash(
    stashId: str,
    stash_update: schemas.StashUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a stash by "stashId".
    """
    stash_map = {"stashId": stashId}
    stash = await CRUD_stash.get(
        db=db,
        filter=stash_map,
    )

    return await CRUD_stash.update(db_obj=stash, obj_in=stash_update, db=db)


@router.delete("/{stashId}", response_model=str)
async def delete_stash(stashId: str, db: Session = Depends(get_db)):
    """
    Delete a stash by "stashId".
    """
    stash_map = {"stashId": stashId}
    await CRUD_stash.remove(db=db, filter=stash_map)

    return f"Stash with mapping ({stash_map}) deleted successfully"