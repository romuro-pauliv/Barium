# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              api.resources.data.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.resources.data_provider import JsonReader
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

json_reader: JsonReader = JsonReader("api", "json")

# FILES |--------------------------------------------------------------------------------------------------------------|
TELEGRAM_API: dict[str, Any] = json_reader.file_data("telegram_api.json")
ERROR_TELEGRAM_MESSAGE: dict[str, Any] = json_reader.file_data("error_telegram_message.json")

SERVICES_ROUTES: dict[str, Any] = json_reader.file_data("services_routes.json")

LOG_REPORT: dict[str, Any] = json_reader.file_data("log_report.json")

WHO_AM_I: dict[str, Any] = json_reader.file_data("whoami.json")

COMMANDS: dict[str, Any] = json_reader.file_data("commands.json")
# |--------------------------------------------------------------------------------------------------------------------|