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

def log_report(log_data: str) -> None:
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG['mongodb'][log_data]
    SendToLog().report(log_schema[0], log_schema[1], log_schema[2])

def init_db() -> MongoClient:
    log_report("init_connection")
    mongo: MongoClient = MongoClient(os.getenv("MONGO"))
    log_report("connection_completed")
    return mongo