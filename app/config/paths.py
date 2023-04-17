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
from log.terminal.paths import PathsLog
# |--------------------------------------------------------------------------------------------------------------------|

class Tools:
    @staticmethod
    def read_json(path_: PosixPath) -> dict[str, Any]:
        PathsLog.show(path_)
        with open(path_, 'r+') as file:
            data: dict[str, Any] = json.load(file)
            file.close(), PathsLog.close()
            
        return data

class TelegramConfig:
    commands_path: PosixPath = Path("app", "json", "commands", "commands.json")
    api_path: PosixPath = Path("app", "json", "api", "telegram.json")
    
    COMMANDS: dict[str, Any] = Tools.read_json(commands_path)
    API: dict[str, Any] = Tools.read_json(api_path)

class TelegramMessages:
    class Start:
        start_path: PosixPath = Path("app", "json", "messages", "start", "start.json")
        help_path: PosixPath = Path("app", "json", "messages", "start", "help.json")
        open_account_path: PosixPath = Path("app", "json", "messages", "start", "open_account.json")
        
        START: dict[str, Any] = Tools.read_json(start_path)
        HELP: dict[str, Any] = Tools.read_json(help_path)
        OPEN_ACCOUNT: dict[str, Any] = Tools.read_json(open_account_path)
    
    class Client:
        start_path: PosixPath = Path("app", "json", "messages", "client", "start.json")
        help_path: PosixPath = Path("app", "json", "messages", "client", "help.json")
        add_wallet_path: PosixPath = Path("app", "json", "messages", "client", "add_wallet.json")
        
        START: dict[str, Any] = Tools.read_json(start_path)
        HELP: dict[str, Any] = Tools.read_json(help_path)
        ADD_WALLET: dict[str, Any] = Tools.read_json(add_wallet_path)
    
    class Error:
        error_path: PosixPath = Path("app", "json", "errors", "responses.json")
        
        ERROR: dict[str, Any] = Tools.read_json(error_path)