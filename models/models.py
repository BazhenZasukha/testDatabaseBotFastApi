from pydantic_settings import BaseSettings
from sqlalchemy import (
    create_engine, Engine, Column,
    Integer, ForeignKey, String,
    Float, DateTime
)
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

from .IConnector import IConnector


# only one real connector to database
# this obj will make every changes
# in database via engine
Base = declarative_base()


class Line(Base):
    __tablename__ = 'lines'
    id = Column(Integer, primary_key=True)

    summ = Column(Float, nullable=False)
    summ2usd = Column(Float, nullable=False)
    currency = Column(Float, nullable=False)
    description = Column(String(1000))
    created_at = Column(DateTime(), default=datetime.now)
    created_by = Column(String(100)) # telegram`s id



# need to create connection to database and
# make sure that its only one connection here
# ! Singleton
class Connector(IConnector):
    __obj = None
    __engine: Engine|None = None
    __session: Session|None = None

    def __new__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = object.__new__(cls)

        return cls.__obj

    def __init__(self, settings: BaseSettings):
        self.__url = settings.database_url
        self.__echo = settings.database_echo

        self.__engine = create_engine(
            self.__url, echo=self.__echo
        )
        self.__session = Session(self.__engine, future=True)

    def getEngine(self) -> Engine: return self.__engine
    def getSession(self) -> Session: return self.__session




def createAll(engine: Engine):
    Base.metadata.create_all(engine)