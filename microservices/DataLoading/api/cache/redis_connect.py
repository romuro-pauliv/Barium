# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         api.cache.redis_connect.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from redis import Redis, client
from dotenv import load_dotenv
import os
# |--------------------------------------------------------------------------------------------------------------------|

load_dotenv()
HOST: str = os.getenv("REDIS_HOST")
PORT: str = os.getenv("REDIS_PORT")

class Cache:
    class TalkMode:
            db0_cache: client.Redis = Redis(HOST, PORT, db=0)