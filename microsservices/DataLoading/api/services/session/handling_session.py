# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                           api.services.session.handling_session.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.database.mongodb_connect import init_db
from pymongo import MongoClient
from api.connections.send_log import SendToLog
from api.config.paths import LogSchema
# |--------------------------------------------------------------------------------------------------------------------|

mongo: MongoClient = init_db()
LogSchema.LOG_REPORT_MSG["mongodb"]["add_chat_id_in_session"]

class Session(object):
    def __init__(self) -> None:
        self.session: list[str] = []
        self.database_list: list[str] = mongo.list_database_names()
        
        self.send_to_log = SendToLog()
        self.add_session: list[str] = LogSchema.LOG_REPORT_MSG["mongodb"]["add_chat_id_in_session"]
        self.no_identify_session: list[str] = LogSchema.LOG_REPORT_MSG["mongodb"]["no_identify_session"]

    def get(self) -> list[str]:
        for db in self.database_list:
            if db[0:5] == "AYLA_":
                self.session.append(db[5::])
                self.send_to_log.report(self.add_session[0], self.add_session[1], db[5::])
            else:
                self.send_to_log.report(self.no_identify_session[0], self.no_identify_session[1], db)
        
        return self.session