# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                          app.database.functions.get.wallet_list.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Import |-----------------------------------------------------------------------------------------------------------|
from database.connect import mongo_init
from pymongo import cursor
# |--------------------------------------------------------------------------------------------------------------------|

def get_wallet_list(chat_id: str) -> list[str]:
    database_name: str = f"AYLA_{chat_id}"
    documents: cursor.Cursor = mongo_init[database_name]["/WALLETS"].find({})

    wallet_list: list[str] = []
    
    for doc in documents:
        wallet_list.append(doc["wallet"])
    
    return wallet_list