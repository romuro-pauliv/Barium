# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          api.connections.sender.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from typing import Union, Callable

from api.errors.send_to_telegram import system_down_message
# |--------------------------------------------------------------------------------------------------------------------|


def connect_with_sender(
    route: dict[str, str],
    post_json: dict[str, str],
    chat_id: str,
    log_report_function: Callable[[str, str, str], None]
) -> None:
    """
    Establishes a connection with Sender microservice
    Args:
        route (dict[str, str]): Route data [HOST, PORT, PATH, ENDPOINT]
        post_json (dict[str, str]): json to post in Sender (see Sender Microservice documentation)
        chat_id (str): chat_id from chat
        log_report_function (Callable[[str, str, str], None]): Log function with connection as LOG microservice
    """
    try:
        requests.post(
            f"{route['HOST']}:{route['PORT']}{route['PATH']}{route['ENDPOINT']}",json=post_json)
        log_report_function("connections", "sent_completed", chat_id)
    except requests.exceptions.ConnectionError:
        log_report_function("connections", "sent_failed", chat_id)
        system_down_message(chat_id)
        log_report_function("telegram_api", "error_message", chat_id)