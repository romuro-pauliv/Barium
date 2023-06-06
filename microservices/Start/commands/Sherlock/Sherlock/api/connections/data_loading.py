# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                    api.connections.data_loading.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from typing import Union, Callable

from api.errors.send_to_telegram import system_down_message
# |--------------------------------------------------------------------------------------------------------------------|


class DataLoading(object):
    def send_cache(
        route: dict[str, str],
        post_json: dict[str, str],
        chat_id: str,
        log_report_function: Callable[[str, str, str], None]
    ) -> bool:
        try:
            requests.post(
                url=f"{route['HOST']}:{route['PORT']}{route['PATH1']['path']}{route['PATH1']['endpoints']['home']}", json=post_json
            )
            log_report_function("connections", "sent_to_cache_completed", chat_id)
            return True
        except requests.exceptions.ConnectionError:
            log_report_function("connections", "sent_to_cache_failed", chat_id)
            system_down_message(chat_id)
            log_report_function("telegram_api", "error_message", chat_id)
            return False
    
    def delete_cache(
        route: dict[str, str],
        post_json: dict[str, str],
        chat_id: str,
        log_report_function: Callable[[str, str, str], None]
    ) -> bool:
        try:
            requests.delete(
                url=f"{route['HOST']}:{route['PORT']}{route['PATH1']['path']}{route['PATH1']['endpoints']['home']}", json=post_json
            )
            log_report_function("connections", "delete_cache_completed", chat_id)
            return True
        except requests.exceptions.ConnectionError:
            log_report_function("connections", "delete_cache_failed", chat_id)
            system_down_message(chat_id)
            log_report_function("telegram_api", "error_message", chat_id)
            return False