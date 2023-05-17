# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                api.config.paths.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pathlib import Path, PosixPath
from typing import Any
import json
# |--------------------------------------------------------------------------------------------------------------------|


class Tools:
    @staticmethod
    def read_json(path_: PosixPath) -> dict[str, Any]:
        """
        Read a .json file
        Args:
            path_ (PosixPath): file path
        Returns:
            dict[str, Any]: Json data in dict format
        """
        with open(path_, "r+") as file:
            data: dict[str, Any] = json.load(file)
            file.close()
        
        return data


class MicrosservicesAPI:
    ms_routes: PosixPath = Path("api", "json", "ms_routes.json")
    who_am_i: PosixPath = Path("api", "json", "whoami.json")
    
    MS_ROUTES: dict[str, Any] = Tools.read_json(ms_routes)
    WHO_AM_I: dict[str, str] = Tools.read_json(who_am_i)
    
class LogSchema:
    log_report_msg: PosixPath = Path("api", "json", "log_report.json")
    LOG_REPORT_MSG: dict[str, Any] = Tools.read_json(log_report_msg)

class TelegramConfig:
    telegram_api_data: PosixPath = Path("api", "json", "telegram_api.json")
    TELEGRAM_API_DATA: dict[str, Any] = Tools.read_json(telegram_api_data)

class ErrorMessages:
    error_message: PosixPath = Path("api", "json", "error_message.json")
    ERROR_MESSAGE: dict[str, Any] = Tools.read_json(error_message)