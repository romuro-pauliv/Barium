# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                           api.services.sherlock.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.database import MongoConnect
from api.connections.log import LogConnect
from api.connections.cache import CacheConnect, CacheDB

from api.threads.executable import Threads

from api.resources.data import MESSAGES2CLIENT

import datetime
from typing import Any, Union
# |--------------------------------------------------------------------------------------------------------------------|

threads: Threads = Threads()
log_connect: LogConnect = LogConnect()
mongo_connect: MongoConnect = MongoConnect()
cache_connect: CacheConnect = CacheConnect(CacheDB.db1)

class Sherlock(object):
    def __init__(self) -> None:
        """
        Initialize Sherlock instance.
        """
        self.targets_list: list[str] = []
        self.database_name: str = "SHERLOCK"

        self.collection_info: str = "info"
        self.collection_resources: str = "resources"
        
    def schema_to_targets(self) -> None:
        """
        Creates a document in MongoDB to store the targets already computed
        """
        username_list: dict[str, list[str]] = mongo_connect.get(
            self.database_name, self.collection_info, {"targets": {"$exists": True}}
        )
        if username_list is None:
            mongo_connect.post(self.database_name, self.collection_info, {"targets": []})
            return None
        
        self.targets_list: list[str] = username_list['targets']
    
    def sherlock_data2str(self, data: dict[str, str]) -> str:
        """
        converts data coming from the sherlock service (target data) into string.
        Args:
            data (dict[str, str]): Data from sherlock {site: uri}

        Returns:
            str: String formatted to be sent to the Sender service
        """
        str_value: str = ""
        msg_number: int = 0
        
        for key, item in data.items():
            str_value += str("🌐 " + key + "\n" + "🔗 " + item + "\n\n")
            msg_number += 1
            
            if msg_number == len(data):
                str_value += MESSAGES2CLIENT["finish_completed"][0]
        
        return str_value
    
    def update_searched_by(self, chat_id: str, target: str) -> None:
        """
        Updates the database that the target was searched for the chat_id specified in the function arguments.
        Args:
            chat_id (str): Client's chat_id
            target (str): Target informed by the client
        """
        new_search: dict[str, str] = {"chat_id": chat_id, "date": datetime.datetime.utcnow()}
        filter: dict[str, str] = {"target": target}
        update: dict[str, str] = {"$push": {"searched_by": new_search}}
        
        mongo_connect.put(self.database_name, self.collection_info, filter, update)
        
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
        sherlock_data: dict[str, str] = json["sherlock_data"]
        
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
        
        # Post in database |-------------------------------------------------------------------------------------------|
        mongo_connect.post(self.database_name, self.collection_resources, resources_bson)
        mongo_connect.post(self.database_name, self.collection_info, info_bson)
        mongo_connect.put(self.database_name, self.collection_info, filter, update_targets)
        
        # Post in cache | ---------------------------------------------------------------------------------------------|
        cache_connect.post(target_username, self.sherlock_data2str(sherlock_data))
        
        # | Post in instance |-----------------------------------------------------------------------------------------|
        self.targets_list.append(target_username)
        
    def get_target(self, json: dict[str, Any]) -> dict[str, Union[str, bool]]:
        """
        Returns the target if it is in the database. The function follows the following flow: cache -> database
        Args:
            json (dict[str, Any]): Data coming from the sherlock service | keys: chat_id, target

        Returns:
            dict[str, Union[str, bool]]: Target data and research situation
        """
        target: str = json['target']
        chat_id: str = json["chat_id"]
        
        # Cache try
        get_cache: Union[bool, str] = cache_connect.get(target)
        if get_cache != False:
            threads.start_thread(self.update_searched_by, chat_id, target)
            return {"result": True, "data": get_cache}
        
        # Database try
        if target in self.targets_list:
            db_result: Union[None, dict[str, Any]] = mongo_connect.get(
                self.database_name, self.collection_resources, {"target": target}
            )
            threads.start_thread(self.update_searched_by, chat_id, target)
            
            data2str: str = self.sherlock_data2str(db_result['data'])
            
            cache_connect.post(target, data2str)
            return {"result": True, "data": data2str}
        
        return {"result": False, "data": None}