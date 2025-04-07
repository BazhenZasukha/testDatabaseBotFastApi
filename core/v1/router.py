from locale import currency

from fastapi import APIRouter, Body

from .setting import v1settings
from configs import settings
from models import DatabaseConnector, DatabaseConnectorInterface, LineModel
from models.crud import CrudManager, CrudInterface
from .schemas.line import LineSchema
from .usd_parser import parseCurrency as parseUsdCurrency

import datetime


router = APIRouter(
    prefix=v1settings.prefix, tags=[v1settings.tags]
)

# connection to database
databaseConnector: DatabaseConnectorInterface = DatabaseConnector(settings)
crudManager: CrudInterface = CrudManager(
    databaseConnector.getSession()
)


@router.get('/')
def check():
    return {"message": "OK"}


# CRUD operations for database lines
@router.get('/getall')
def get_all():
    lines = crudManager.getAll(LineModel)

    response = {
        "message": "OK",
        "data": lines
    }

    return response


@router.post('/create')
def create(lineData: LineSchema = Body(embed=True)):
    _, uah_to_usd, currencyK = parseUsdCurrency()

    newLine = LineModel(
        summ=lineData.summ,
        summ2usd=lineData.summ * currencyK,
        currency=uah_to_usd,
        description=lineData.description,
        created_at=datetime.datetime.now(),
        created_by = lineData.created_by
    )
    crudManager.create(newLine)

    return {
        "message": "OK",
        "result": newLine.id
    }

@router.delete('/delete/<lineId:int>')
def delete(lineId: int):
    itemToDelete = crudManager.get(LineModel, lineId)
    crudManager.delete(itemToDelete)

    return {
        "message": "OK"
    }

@router.put('/update/<lineId:int>')
def update(lineId: int, updateInfo: dict = Body(embed=True)):
    _, uah_to_usd, currencyK = parseUsdCurrency()

    if 'summ' in updateInfo:
        updateInfo['summ2usd'] = updateInfo['summ'] * currencyK
    updateInfo['currency'] = uah_to_usd

    crudManager.update(LineModel, updateInfo, id=lineId)

    return {
        "message": "OK"
    }