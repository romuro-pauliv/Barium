# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   api.services.data_from_client.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.database import MongoConnect
from typing import Union, Any
# |--------------------------------------------------------------------------------------------------------------------|

mongo_connect: MongoConnect = MongoConnect()

class DataFromClient(object):
    def __init__(self) -> None:
        """
        Initialize DataFromClient instance.
        """
        self.database_name: str = "barium"
        self.collection_name: str = "clients"
    
    def schema(self) -> None:
        """
        Create the database schema to receive the chat_ids from the clients.
        """
        chat_id_from_clients: dict[str, list[str]] = mongo_connect.get(
            self.database_name, self.collection_name, {"chat_id_from_clients": {'$exists': True}}
        )
        if chat_id_from_clients is None:
            mongo_connect.post(self.database_name, self.collection_name, {"chat_id_from_clients": []})
        
    def post(self, data: dict[str, Union[str, bool, int]]) -> None:
        """
        POST the client data in the database and updates the list of chat_ids of active clients.
        Args:
            data (dict[str, Union[str, bool, int]]): Client data
        """
        chat_id: str = data['id']
        
        filter: dict[str, dict[str, bool]] = {
            "chat_id_from_clients": {
                "$exists": True
            }
        }
        
        update_chat_id_from_clients: dict[str, dict[str, dict[str, bool]]] = {
            "$push": {"chat_id_from_clients": chat_id}
        }
        
        mongo_connect.post(self.database_name, self.collection_name, data)
        mongo_connect.put(self.database_name, self.collection_name, filter, update_chat_id_from_clients)
        
        
    def get(self) -> list[int]:
        """
        Requests from the database the list of active chat_ids in the database.

        Returns:
            list[int]: List with chat_ids
        """
        response: dict[str, list[str]] = mongo_connect.get(
            self.database_name, self.collection_name, {"chat_id_from_clients": {'$exists': True}}
        )
        
        return response['chat_id_from_clients']