from sqlalchemy.orm import Session
from abc import ABC

from .models import *


class CrudInterface(ABC):
    __session: Session|None = None

    def __init__(self): ...

    def getAll(self): pass

    def get(self, *args, **kwargs): ... # read
    def create(self, *args, isCommit=True, **kwargs): ...
    def update(self, *args, isCommit=True, **kwargs): ...
    def delete(self, *args, isCommit=True, **kwargs): ...



class CrudManager(CrudInterface):
    def __init__(self, session: Session):
        self.__session = session

    def getAll(self, model):
        return self.__session.query(model).all()

    def create(self, object, isCommit=True, **kwargs):
        self.__session.add(object)
        if isCommit: self.__session.commit()

    def get(self, *args, **kwargs): ... # read
    def update(self, *args, isCommit=True, **kwargs): ...
    def delete(self, *args, isCommit=True, **kwargs): ...