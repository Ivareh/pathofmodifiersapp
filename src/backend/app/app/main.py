from __future__ import annotations
import fastapi as _fastapi
from typing import TYPE_CHECKING, List


import app.core.schemas.schemas as _schemas
import app.core.services.services as _services

import app.crud.base as _crud


import sqlalchemy.orm as _orm

app = _fastapi.FastAPI()


@app.get("/")
async def read_main():
    return {"message": "Welcome to Path of Modifiers API!"}


currencyCRUD = _crud.CRUDBase(schema=_schemas.Currency)


@app.post("/api/currency/", response_model=_schemas.Currency)
async def create_currency(
    currency: _schemas.CurrencyCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await currencyCRUD.create(db=db, obj_in=currency)


@app.get("/api/currency/{currencyId}", response_model=_schemas.Currency)
async def get_currency(
    currencyName: str, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    currency = await currencyCRUD.get(db=db, currencyName=currencyName)
    return currency


@app.get("/api/currency/", response_model=List[_schemas.Currency])
async def get_all_currency(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    all_currency = await currencyCRUD.get_all(db=db)
    return all_currency


@app.delete("/api/currency/{currencyName}")
async def delete_currency(
    currencyName: str, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    currency = await currencyCRUD.get(currencyName=currencyName, db=db)
    await currencyCRUD.remove(currency, db=db)

    return "currency deleted successfully"


@app.put("/api/currency/{currencyId}", response_model=_schemas.Currency)
async def update_currency(
    currencyId: str,
    currencyData: _schemas.CurrencyUpdate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    currency = await currencyCRUD.get(
        db=db,
        id=currencyId,
    )

    return await currencyCRUD.update(
        currencyData=currencyData, currency=currency, db=db
    )
