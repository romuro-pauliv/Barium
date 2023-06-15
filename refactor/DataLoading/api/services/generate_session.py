# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   api.services.generate_session.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.database import MongoConnect
from api.connections.log import LogConnect

from api.resources.data import WHO_AM_I

from api.threads.executable import Threads
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()
threads: Threads = Threads()

class GenerateSession(MongoConnect):
    def __init__(self) -> None:
        """
        Initializes GenerateSession Instance.
        """
        super().__init__()
        self.session: list[str] = []
        self.my_name: str = f"{WHO_AM_I['HOST']}:{WHO_AM_I['PORT']}"
    
    def get(self) -> list[str]:
        """
        Generates the client sessions based on the list of database names.
        Returns:
            list[str]: client session
        """
        database_names: list[str] = self.list_database_names()
        for db in database_names:
            if db[0:5] == "AYLA_":
                self.session.append(db[5::])
        
        threads.start_thread(log_connect.report, "GET", self.my_name, "info", "INTERNAL", True, "Generate Session")
        
        return self.session
        