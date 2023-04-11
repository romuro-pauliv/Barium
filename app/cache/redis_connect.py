# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         app.cache.redis_connect.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from redis import Redis, client
from dotenv import load_dotenv
load_dotenv()
import os
# |--------------------------------------------------------------------------------------------------------------------|


class Cache:
    class TalkMode:
        HOST: str = str(os.getenv("REDIS_HOST"))
        PORT: str = int(os.getenv("REDIS_PORT"))
        
        open_account_branch: client.Redis = Redis(HOST, PORT, db=0)
        
        log_in_branch: client.Redis = Redis(HOST, PORT, db=1)
        add_wallet_branch: client.Redis = Redis(HOST, PORT, db=2)
        
    class DataOtimization:
        HOST: str = str(os.getenv("REDIS_HOST"))
        PORT: str = int(os.getenv("REDIS_PORT"))

        data_report: client.Redis = Redis(HOST, PORT, db=3)