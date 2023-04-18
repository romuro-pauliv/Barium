# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                          app.database.functions.post.add_wallet.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Import |-----------------------------------------------------------------------------------------------------------|
from database.connect import mongo_init
from typing import Union
import datetime
from cache.schema.internal_cache import Schema
from log.database.model import log

from log.terminal.cache.internal.methods import InternalCacheLog
from log.terminal.database.log.show import LogDBLog
from log.terminal.database.methods import MongoLog
# |--------------------------------------------------------------------------------------------------------------------|

def post_add_wallet(chat_id: str, username: str, cache_data: dict[str, str]) -> None:
    database_name: str = f"AYLA_{chat_id}"
    
    wallet_name: str = cache_data[Schema.InternalCache.NEW_WALLET[0]]
    amount: str = cache_data[Schema.InternalCache.NEW_WALLET[1]]
    obs: str = cache_data[Schema.InternalCache.NEW_WALLET[2]]
    
    InternalCacheLog.get(chat_id, "AddWalletChat", cache_data)

    mongo_init[database_name]["/WALLETS"].insert_one(
        {
            "datetime": datetime.datetime.utcnow(),
            "wallet": wallet_name,
            "amount": amount,
            "obs": obs
        }
    )
    MongoLog.post(chat_id, database_name, "/WALLETS", "add_wallet")
    
    mongo_init[database_name]["/LOG"].insert_one(log(chat_id, username, f"add wallet {wallet_name} in wallet list"))
    LogDBLog.show(chat_id, database_name, "/LOG", f"add wallet {wallet_name} in wallet list")
    
    mongo_init.AYLA_LOG.MAINLOG.insert_one(log(chat_id, username, f"add wallet {wallet_name} in wallet list"))
    LogDBLog.show(chat_id, "AYLA_LOG", "MAINLOG", f"add wallet {wallet_name} in wallet list")
    
    mongo_init[database_name][wallet_name].insert_one(
        {"datetime": datetime.datetime.utcnow(), "log": f"hello, {wallet_name}"}
    )
    MongoLog.post(chat_id, database_name, wallet_name, "add_wallet")
    
    mongo_init[database_name]["/LOG"].insert_one(log(chat_id, username, f"open wallet {wallet_name}"))
    LogDBLog.show(chat_id, database_name, "/LOG", f"open wallet {wallet_name}")
    
    mongo_init.AYLA_LOG.MAINLOG.insert_one(log(chat_id, username, f"open wallet {wallet_name}"))
    LogDBLog.show(chat_id, "AYLA_LOG", "MAINLOG", f"open wallet {wallet_name}")