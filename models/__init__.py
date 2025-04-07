from .IConnector import IConnector
from .models import Connector, createAll, Line


# its what another programmer can import
DatabaseConnectorInterface = IConnector
DatabaseConnector = Connector
create = createAll
LineModel = Line