# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                 api.services.command_recognizer.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.config.paths import MicrosservicesAPI
from api.connections.send_log import SendToLog
# |--------------------------------------------------------------------------------------------------------------------|


class Driver(object):
    def __init__(self) -> None:
        self.sub_services_conn: dict[str, dict] = MicrosservicesAPI.MS_ROUTES["sub_services"]
        self.sub_services_conn_name: list[str] = [i for i in self.sub_services_conn.keys()]

        self.commands: dict[str, str] = MicrosservicesAPI.COMMANDS
        
    def direct_to(self, message: dict[str, str | list]) -> None:
        for service_name in self.sub_services_conn_name:
            if message["text"] == self.commands[service_name]:
                print(
                    self.sub_services_conn[service_name]["HOST"],
                    self.sub_services_conn[service_name]["PORT"],
                    self.sub_services_conn[service_name]["DIR"],
                )
                return None