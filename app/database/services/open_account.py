# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                              app.database.services.open_account.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Import |-----------------------------------------------------------------------------------------------------------|
from database.connect import mongo_init
from pymongo import MongoClient
from typing import Union
import datetime

from cache.schema.internal_cache import Schema

from log.terminal.database.open_account.show import OpenAccountLog
from log.terminal.database.log.show import LogDBLog
from log.database.model import log
# |--------------------------------------------------------------------------------------------------------------------|


class MongoOpenAccount(object):
    def __init__(self) -> None:
        self.mongo: MongoClient = mongo_init
    
    def open_database(self, chat_id: str, username: str) -> None:
        database_name: str = f"AYLA_{chat_id}"
        OpenAccountLog.open_database(chat_id, database_name)
        
        self.mongo[database_name]["/LOG"].insert_one(self.log(chat_id, username, "open account"))
        LogDBLog.show(chat_id, database_name, "/LOG", "open account")
        self.mongo.AYLA_LOG.MAINLOG.insert_one(self.log(chat_id, username, "open account"))
        LogDBLog.show(chat_id, "AYLA_LOG", "MAINLOG", "open account")
        
    def open_wallet_list(self, chat_id: str, username: str, wallet_name: str, amount: str, wallet_obs: str) -> None:
        database_name: str = f"AYLA_{chat_id}"
        
        self.mongo[database_name]["/WALLETS"].insert_one(
            {
                "datetime": datetime.datetime.utcnow(),
                "wallet": wallet_name,
                "amount": amount,
                "obs": wallet_obs
            }
        )
        OpenAccountLog.open_wallet_list(chat_id, database_name)
        
        self.mongo[database_name]["/LOG"].insert_one(self.log(chat_id, username, "open wallet list"))
        LogDBLog.show(chat_id, database_name, "/LOG", "open wallet list")
        self.mongo.AYLA_LOG.MAINLOG.insert_one(self.log(chat_id, username, "open wallet list"))
        LogDBLog.show(chat_id, "AYLA_LOG", "MAINLOG", "open wallet list")
    
    def open_wallet_collection(self, chat_id: str, username: str, wallet_name: str) -> None:
        database_name: str = f"AYLA_{chat_id}"
        
        self.mongo[database_name][wallet_name].insert_one(
            {"datetime": datetime.datetime.utcnow(), "log": f"hello, {wallet_name}"}
        )
        OpenAccountLog.open_wallet_collection(chat_id, database_name, wallet_name)
        
        self.mongo[database_name]["/LOG"].insert_one(self.log(chat_id, username, f"open wallet {wallet_name}"))
        LogDBLog.show(chat_id, database_name, "/LOG", f"open wallet {wallet_name}")
        self.mongo.AYLA_LOG.MAINLOG.insert_one(self.log(chat_id, username, f"open wallet {wallet_name}"))
        LogDBLog.show(chat_id, "AYLA_LOG", "MAINLOG", f"open wallet {wallet_name}")
    
    def init_account(self, message: dict[str, str], in_cache: dict[str, Union[str, float]]) -> None:
        chat_id: str = message["chat_id"]
        username: str = message["username"]
        
        wallet_name: str = in_cache[Schema.InternalCache.OPEN_ACCOUNT[0]]
        amount: float = in_cache[Schema.InternalCache.OPEN_ACCOUNT[1]]
        obs: str = in_cache[Schema.InternalCache.OPEN_ACCOUNT[2]]
        
        self.open_database(chat_id, username)
        self.open_wallet_list(chat_id, username, wallet_name, amount, obs)
        self.open_wallet_collection(chat_id, username, wallet_name)