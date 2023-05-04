# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                    api.database.mongodb_connect.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pymongo import MongoClient
from api.connections.send_log import SendToLog
from api.config.paths import LogSchema

from dotenv import load_dotenv
import os
# |--------------------------------------------------------------------------------------------------------------------|

load_dotenv()

def init_db() -> MongoClient:
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG["mongodb"]["init_connection"]
    SendToLog().report(log_schema[0], log_schema[1], log_schema[2])
    
    mongo: MongoClient = MongoClient(os.getenv("MONGO"))
    
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG["mongodb"]["connection_completed"]
    SendToLog().report(log_schema[0], log_schema[1], log_schema[2])
    return mongo