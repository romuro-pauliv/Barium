# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                app.config.paths.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pathlib import Path, PosixPath
from typing import Any
import json
# |--------------------------------------------------------------------------------------------------------------------|


class TelegramConfig:
    COMMANDS: PosixPath = Path("app", "json", "commands", "commands.json")
    API: PosixPath = Path("app", "json", "api", "telegram.json")


class TelegramMessages:
    class Start:
        START: PosixPath = Path("app", "json", "messages", "start", "start.json")
        HELP: PosixPath = Path("app", "json", "messages", "start", "help.json")
        OPEN_ACCOUNT: PosixPath = Path("app", "json", "messages", "start", "open_account.json")
    
    class Client:
        HELP: PosixPath = Path("app", "json", "messages", "client", "help.json")
        

class Tools:
    @staticmethod
    def read_json(path_: PosixPath) -> dict[str, Any]:
        print(path_)
        with open(path_, 'r+') as file:
            data: dict[str, Any] = json.load(file)
            file.close()
            
        return data