# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                          app.database.functions.get.wallet_list.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Import |-----------------------------------------------------------------------------------------------------------|
from database.connect import mongo_init
from pymongo import MongoClient
from typing import Union
# |--------------------------------------------------------------------------------------------------------------------|


def get_wallet_list(chat_id: str) -> None:
    database_name: str = f"AYLA_{chat_id}"
    