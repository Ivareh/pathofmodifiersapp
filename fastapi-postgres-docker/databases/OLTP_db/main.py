from __future__ import annotations
import fastapi as _fastapi
from typing import TYPE_CHECKING, List
import sqlalchemy.orm as _orm

import schemas as _schemas
import services as _services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = _fastapi.FastAPI()

@app.post("/api/currencys/", response_model=_schemas.Currency)
async def create_currency(
    currency: _schemas.CreateCurrency, 
    db: _orm.Session = _fastapi.Depends(_services.get_db)
    ):
    return await _services.create_currency(currency=currency, db=db)

@app.get("/api/currencys/", response_model=List[_schemas.Currency])
async def get_currencys(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_all_currencys(db=db)

@app.get("/api/currencys/{currency_id}", response_model=_schemas.Currency)
async def get_currency(
    currency_id: int, db: "Session" = _fastapi.Depends(_services.get_db)
    ):
    currency = await _services.get_currency(currency_id=currency_id, db=db)
    if currency is None:
        raise _fastapi.HTTPException(status_code=404, detail="currency not found")
    return currency

@app.delete("/api/currencys/{currency_id}")
async def delete_currency(currency_id: int, db: "Session" = _fastapi.Depends(_services.get_db)):
    currency = await _services.get_currency(currency_id=currency_id, db=db)
    if currency is None:
        raise _fastapi.HTTPException(status_code=404, detail="currency not found")
    await _services.delete_currency(currency, db=db) 

    return "currency deleted successfully"

@app.put("/api/currencys/{currency_id}", response_model=_schemas.Currency)
async def update_currency(
    currency_id: int, 
    currency_data: _schemas.CreateCurrency, 
    db: "Session" = _fastapi.Depends(_services.get_db)
    ):
    currency = await _services.get_currency(currency_id=currency_id, db=db)
    if currency is None:
        raise _fastapi.HTTPException(status_code=404, detail="currency not found")
        
    return await _services.update_currency(
        currency_data = currency_data, currency=currency, db=db
        )
