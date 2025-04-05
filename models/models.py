


class Connector:
    __obj = None

    def __new__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = object.__new__(cls)

        return cls.__obj

    def __init__(self, connectorUrl: str):
        self.__url = connectorUrl


