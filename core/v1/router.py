from fastapi import APIRouter

from .setting import v1settings
from configs import settings
from models import DatabaseConnector, DatabaseConnectorInterface
from models.crud import CrudManager, CrudInterface


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
    session

    response = {"message": "OK"}

    return response