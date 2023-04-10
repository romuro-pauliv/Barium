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
# |--------------------------------------------------------------------------------------------------------------------|

mongo_init: MongoClient = MongoClient(os.getenv("MONGO"))
    