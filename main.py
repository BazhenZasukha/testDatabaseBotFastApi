from fastapi import FastAPI
from sqlalchemy import Engine

from configs import settings
from models import DatabaseConnector, DatabaseConnectorInterface, create


app = FastAPI()
databaseConnector: DatabaseConnectorInterface = DatabaseConnector(settings)

# getting current DB session and creating all tables
mainDatabaseEngine: Engine = databaseConnector.getEngine()
create(mainDatabaseEngine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
