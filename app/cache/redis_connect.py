# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         app.cache.redis_connect.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from redis import Redis, client
# |--------------------------------------------------------------------------------------------------------------------|


class Cache:
    class TalkMode:
        open_account_branch: client.Redis = Redis("127.0.0.1", "6379", db=0)
        
        log_in_branch: client.Redis = Redis("127.0.0.1", "6379", db=1)
        new_wallet_branch: client.Redis = Redis("127.0.0.1", "6379", db=2)
        
    class DataOtimization:
        data_report: client.Redis = Redis("127.0.0.1", "6379", db=3)