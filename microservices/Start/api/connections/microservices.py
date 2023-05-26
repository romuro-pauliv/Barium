# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   api.connections.microservices.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from typing import Callable

from api.error.send_to_telegram import system_down_message
# |--------------------------------------------------------------------------------------------------------------------|


def direct_to_ms(
    microservice_route_data: dict[str, dict[str, str]],
    command: str,
    message: dict[str, str | list],
    info_log: list[Callable[[str, str, str], None]],
    error_msg_to_telegram: Callable[[str], None]
) -> None:
    """
    Stablishes a connection with the specific microservice.
    [Will connect to the LOG and Telegram API if the connection
     to the microservice throws an exception]

    Args:
        microservice_route_data (dict[str, dict[str, str]]): json from ms_routes.sjon [sub_services key]
        command (str): A command in Message from Telegram API
        message (dict[str, str  |  list]): Message from Telegram API
        info_log (list[Callable[[str, str, str], None]]): list content two log function ([0] Sucess, [1] Failed)
        error_msg_to_telegram (Callable[[str], None]): Function that estabilishes connection with 
                                                       Telegram API in exceptions cases
    """
    complete_connection_log: Callable[[str, str, str], None] = info_log[0]
    failed_connection_log: Callable[[str, str, str], None] = info_log[1]
    
    microservice_route: dict[str, str] = microservice_route_data[command]
    HOST: str = microservice_route["HOST"]
    PORT: str = microservice_route["PORT"]
    PATH: str = microservice_route["PATH1"]["path"]
    ENDPOINT: str = microservice_route["PATH1"]["endpoints"]["home"]
    
    try:
        requests.post(f"{HOST}:{PORT}{PATH}{ENDPOINT}", json=message)
        complete_connection_log(HOST, PORT, message["chat_id"])
    except requests.exceptions.ConnectionError:
        system_down_message(message["chat_id"])
        error_msg_to_telegram(message["chat_id"])
        failed_connection_log(HOST, PORT, message["chat_id"])