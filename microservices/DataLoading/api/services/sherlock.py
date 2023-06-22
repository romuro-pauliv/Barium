# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                           api.services.sherlock.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.database import MongoConnect
from api.connections.log import LogConnect

import datetime
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()
mongo_connect: MongoConnect = MongoConnect()

class Sherlock(object):
    def __init__(self) -> None:
        """
        Initialize Sherlock instance.
        """
        self.users: list[str] = []
        self.database_name: str = "SHERLOCK"

        self.collection_info: str = "info"
        self.collection_resources: str = "resources"
        
    def schema_to_targets(self) -> None:
        """
        Creates a document in MongoDB to store the targets already computed
        """
        if mongo_connect.get(self.database_name, self.collection_info, {"targets": {"$exists": True}}) is None:
            mongo_connect.post(self.database_name, self.collection_info, {"targets": []})
        
    def post_username_target(self, json: dict[str, Any]) -> None:
        """
        Puts the target data computed in the Sherlock service into the database
        Args:
            json (dict[str, Any]): Document that will be sent to the database | keys -> chat_id, client_username, 
                                   target_username, sherlock_data
        """
        date: datetime.datetime = datetime.datetime.utcnow()
        
        chat_id: str = json['chat_id']
        target_username: str = json["target_username"]
        sherlock_data: str = json["sherlock_data"]
        
        # Post
        resources_bson: dict[str, Any] = {
            "target": target_username,
            "date": date,
            "data": sherlock_data
        }
        info_bson: dict[str, Any] = {
            "target": target_username, "date": date,
            "searched_by": [{
                "chat_id": chat_id,
                "date": date
            }]
        }
        
        # Update
        filter: dict[str, Any] = {
            "targets": {
                "$exists": True
            }
        }
        update_targets: dict[str, Any] = {
            "$push": {
                "targets": target_username
            }
        }
        
        mongo_connect.post(self.database_name, self.collection_resources, resources_bson)
        mongo_connect.post(self.database_name, self.collection_info, info_bson)
        mongo_connect.put(self.database_name, self.collection_info, filter, update_targets)