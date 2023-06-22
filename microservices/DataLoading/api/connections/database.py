# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         api.connection.database.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pymongo import MongoClient
from api.connections.log import LogConnect

from typing import Union, Any
from dotenv import load_dotenv
import os
# |--------------------------------------------------------------------------------------------------------------------|
load_dotenv()

log_connect: LogConnect = LogConnect()

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
        log_connect.report("GET", self.uri, "info", "INTERNAL", True, "Database Names")
        return database_names
    
    def get(self, database: str, collection: str, filter: dict[str, Any]) -> Union[dict[str, Any], None]:
        """ 
        PUT a document in MongoDB
        
        Args:
            database (str): database name
            collection (str): collection name
            filter (dict[str, Any]): filter (document finder)
        
        Returns:
            Union[dict[str, Any], None]: Document from database
        """
        document: Union[dict[str, Any], None] = self.connect[database][collection].find_one(filter)
        log_connect.report("GET", self.uri, "info", "INTERNAL", True, f"[{database}][{collection}] - find_one")
        return document
    
    def post(self, database: str, collection: str, file: Union[dict[str, Any], list[dict[str, Any]]]) -> None:
        """
        POST by bson in MongoDB
        Args:
            database (str): Database Name
            collection (str): Collection Name
            file (Union[dict[str, Any], list[dict[str, Any]]]): Files
        """
        if isinstance(file, dict):
            self.connect[database][collection].insert_one(file)
            log_connect.report("POST", self.uri, "info", "INTERNAL", True, f"[{database}][{collection}] - insert_one")
        elif isinstance(file, list):
            self.connect[database][collection].insert_many(file)
            log_connect.report("POST", self.uri, "info", "INTERNAL", True, f"[{database}][{collection}] - insert_many")
    
    def put(self, database: str, collection: str, filter: dict[str, Any], update: dict[str, Any]) -> None:
        """
        PUT a document in MongoDB
        Args:
            database (str): database name
            collection (str): collection name
            filter (dict[str, Any]): filter (document finder)
            update (dict[str, Any]): update schema
        """
        self.connect[database][collection].update_one(filter, update)
        log_connect.report("PUT", self.uri, "info", "INTERNAL", True, f"[{database}][{collection}] - update")