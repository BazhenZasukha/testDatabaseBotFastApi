from fastapi import FastAPI
from sqlalchemy import Engine

from configs import settings
from models import DatabaseConnector, DatabaseConnectorInterface, create
from core import Router

app = FastAPI()
databaseConnector: DatabaseConnectorInterface = DatabaseConnector(settings)

# getting current DB session and creating all tables
mainDatabaseEngine: Engine = databaseConnector.getEngine()
create(mainDatabaseEngine)


# connecting main router
app.include_router(Router)