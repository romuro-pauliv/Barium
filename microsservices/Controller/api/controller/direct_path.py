# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      api.controller.direct_path.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.cache.redis_connect import Cache
# |--------------------------------------------------------------------------------------------------------------------|


def driver(message: str) -> None:
    if Cache.TalkMode.open_account_branch.get(message["chat_id"]):
        print("in cache")
    else:
        print("None")