# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   api.connections.microservices.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from typing import Callable
from api.errors.send_to_telegram import system_down_message
# |--------------------------------------------------------------------------------------------------------------------|


def post_in_microservices(
    route: dict[str, str],
    path_: str, endpoint: str,
    log_data: list[str, str],
    message: dict[str],
    log_report: Callable[[str, str, str], None]) -> None:
    """
    Send the message to specific microservice.

    Args:
        route (dict[str, str]): route in ms_routes.json
        log_data (list[str, str]): [0] sucessfully key in log_report.json and [1] failed key in log_report.json
        message (dict[str]): Message from Gateway
        log_report (Callable[[str, str, str], None]): log_report function [[master, log_data, message]]
    """
    try:
        requests.post(f"{route['HOST']}:{route['PORT']}{route[path_]['path']}{route[path_]['endpoints'][endpoint]}", json=message)
        log_report("connections", log_data[0], message)
    except requests.exceptions.ConnectionError:
        log_report("connections", log_data[1], message)
        system_down_message(message["chat_id"])
        log_report("telegram_api", "error_message", message)
