# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         app.cache.load.login_db.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from cache.redis_connect import Cache
from database.connect import mongo_init
# |--------------------------------------------------------------------------------------------------------------------|


def loading_user_in_cache() -> None:
    database_list: list[str] = mongo_init.list_database_names()
    chat_id_list: list[str] = []
    for db in database_list:
        if db[0:5] == "AYLA_":
            chat_id_list.append(db[5::])
    
    for chat_id in chat_id_list:
        Cache.TalkMode.log_in_branch.mset({chat_id: "active"})