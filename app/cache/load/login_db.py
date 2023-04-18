# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         app.cache.load.login_db.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from cache.redis_connect import Cache
from database.connect import mongo_init

from log.terminal.cache.redis.login_cached import LoginCachedLog
# |--------------------------------------------------------------------------------------------------------------------|


def loading_user_in_cache() -> None:
    database_list: list[str] = mongo_init.list_database_names()
    chat_id_list: list[str] = []
    for db in database_list:
        LoginCachedLog.read(db)
        if db[0:5] == "AYLA_":
            chat_id_list.append(db[5::])
            LoginCachedLog.active()
        else:
            LoginCachedLog.false()
    
    for chat_id in chat_id_list:
        Cache.TalkMode.log_in_branch.mset({chat_id: "active"})
        LoginCachedLog.add_in_cache(chat_id)