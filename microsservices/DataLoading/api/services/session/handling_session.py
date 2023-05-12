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

import threading
# |--------------------------------------------------------------------------------------------------------------------|

mongo: MongoClient = init_db()

class Session(object):
    def __init__(self) -> None:
        """
        Loading MongoDB database name list and Connection with Log MS
        """
        self.session: list[str] = []
        self.database_list: list[str] = mongo.list_database_names()        
        self.send_to_log = SendToLog()

    def log_report(self, log_data: str, id_: str) -> None:
        """
        Resume log message loading and send to LOG microservice
        Args:
            master (str): Higher key in LOG_REPORT_MSG .json
            log_data (str): lower key (log message data) in LOG_REPORT_MSG .json
            message_data (str): Handled message from Telegram API
        """
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG["mongodb"][log_data]
        threading.Thread(
            target=self.send_to_log.report,
            args=(
                log_schema[0], log_schema[1], id_
            )
        ).start()
    
    def get(self) -> list[str]:
        """
        Get a session list from database
        Returns:
            list[str]: list with session id's
        """
        for db in self.database_list:
            if db[0:5] == "AYLA_":
                self.session.append(db[5::])
                self.log_report("add_chat_id_in_session", db[5::])            
            else:
                self.log_report("no_identify_session", db)

        return self.session