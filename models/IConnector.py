from abc import ABC

from pydantic_settings import BaseSettings
from sqlalchemy import Engine
from sqlalchemy.orm import Session


class IConnector(ABC):
    __engine: Engine|None = None
    __session: Session|None = None

    # sql alchemy engine and main session will create here
    def __init__(self, settings: BaseSettings) -> None: ...

    # getter for engine
    def getEngine(self) -> Engine: ...

    # getter for session
    def getSession(self) -> Session: ...
