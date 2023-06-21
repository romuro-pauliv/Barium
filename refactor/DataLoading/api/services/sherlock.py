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
        self.users: list[str] = []
        self.database_name: str = "SHERLOCK"
        
    def post_username_target(self, json: dict[str, Any]) -> None:
        date: datetime.datetime = datetime.datetime.utcnow()
        
        self.collection_resources: str = "resources"
        self.collection_info: str = "info"
        
        chat_id: str = json['chat_id']
        client_username: str = json["client_username"]
        target_username: str = json["target_username"]
        sherlock_data: str = json["sherlock_data"]
        
        # | Resources POST |-------------------------------------------------------------------------------------------|
        resources_bson: dict[str, Any] = {
            "target": target_username, "date": date, "data": sherlock_data
        }
        mongo_connect.post(self.database_name, self.collection_resources, resources_bson)
        log_connect.report("POST", mongo_connect.uri, "info", "INTERNAL", True, "SHERLOCK_RESOURCES")
        # |------------------------------------------------------------------------------------------------------------|
        
        # | Info POST |------------------------------------------------------------------------------------------------|
        info_bson: dict[str, Any] = {
            "target": target_username, "date": date,
            "searched_by": [{"username": client_username, "chat_id": chat_id, "date": date}]
        }
        mongo_connect.post(self.database_name, self.collection_info, info_bson)
        log_connect.report("POST", mongo_connect.uri, "info", "INTERNAL", True, "SHERLOCK_RESOURCES")
        # |------------------------------------------------------------------------------------------------------------|