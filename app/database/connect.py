# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                            app.database.connect.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

from log.terminal.database.connect import DBConnectLog
# |--------------------------------------------------------------------------------------------------------------------|

mongo_init: MongoClient = MongoClient(os.getenv("MONGO"))
DBConnectLog.show(os.getenv("MONGO"))