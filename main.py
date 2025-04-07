import asyncio
import threading

import uvicorn
from fastapi import FastAPI
from sqlalchemy import Engine

from configs import settings
from models import DatabaseConnector, DatabaseConnectorInterface, create
from core import Router
from core.telegram_bot.tbot import startTelegramBot

app = FastAPI()
databaseConnector: DatabaseConnectorInterface = DatabaseConnector(settings)

# getting current DB session and creating all tables
mainDatabaseEngine: Engine = databaseConnector.getEngine()
create(mainDatabaseEngine)


# connecting main router
app.include_router(Router)

if __name__ == '__main__':
    threading.Thread(target=asyncio.run, args=(startTelegramBot(settings.telegram_bot_token),), daemon=True).start()
    uvicorn.run("main:app", host=settings.api_host, port=settings.api_port, reload=False)