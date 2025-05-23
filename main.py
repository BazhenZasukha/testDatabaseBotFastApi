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


async def startFastApiServer():
    # uvicorn.run("main:app", host=settings.api_host, port=settings.api_port, reload=False)
    config = uvicorn.Config(app=app, host=settings.api_host, port=settings.api_port, log_level="info", reload=False)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        startTelegramBot(settings), startFastApiServer()
    )

if __name__ == '__main__':
    #threading.Thread(target=asyncio.run, args=(startTelegramBot(settings),), daemon=True).start()
    #uvicorn.run("main:app", host=settings.api_host, port=settings.api_port, reload=False)
    asyncio.run(main())
    
