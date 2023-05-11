# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     api.errors.send_to_telegram.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.config.paths import ErrorMessages
from api.api.api_request import TelegramApiRequest
# |--------------------------------------------------------------------------------------------------------------------|

def system_down_message(chat_id: str) -> None:
    TelegramApiRequest().send_message(chat_id, ErrorMessages.ERROR_MESSAGE["message"])