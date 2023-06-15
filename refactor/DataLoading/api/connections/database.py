# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         api.connection.database.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pymongo import MongoClient
from api.connections.log import LogConnect

from api.threads.executable import Threads

from dotenv import load_dotenv
import os
# |--------------------------------------------------------------------------------------------------------------------|
load_dotenv()

log_connect: LogConnect = LogConnect()
threads: Threads = Threads()

class MongoConnect(object):
    def __init__(self) -> None:
        """
        Initialize MongoConnect Instance. Establishes a connection to the MongoDB
        """
        self.uri: str = os.getenv("MONGO")
        self.connect: MongoClient = MongoClient(self.uri)
        log_connect.report("SOCKET", self.uri, "info", "INTERNAL", True)
    
    def list_database_names(self) -> list[str]:
        """
        Get database names from MongoDB. Generates logs
        Returns:
            list[str]: database names
        """
        database_names: list[str] = self.connect.list_database_names()
        threads.start_thread(log_connect.report, "GET", self.uri, "info", "INTERNAL", True, "Database Names")
        return database_names
    