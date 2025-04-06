from fastapi import APIRouter

from .setting import v1settings
from configs import settings
from models import DatabaseConnector, DatabaseConnectorInterface, LineModel
from models.crud import CrudManager, CrudInterface
from .schemas.line import LineSchema

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


@router.get('/create')
def create(lineData: LineSchema):
    newLine = LineModel(
        summ=lineData.summ,
        description=lineData.description,
        created_at=datetime.datetime.now(),
        created_by = lineData.created_by
    )
    crudManager.create(newLine)

    return {
        "message": "OK",
        "result": newLine.id
    }