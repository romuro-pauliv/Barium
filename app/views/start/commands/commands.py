# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               app.views.start.commands.commands.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import TelegramConfig, Tools
# |--------------------------------------------------------------------------------------------------------------------|

commands_json: dict[str, dict[str]] = Tools.read_json(TelegramConfig.COMMANDS)

COMMANDS_LIST: dict[str, str] = commands_json["start_commands"]
ABOUT_COMMANDS: dict[str, dict] = commands_json["about_commands"]["start_commands"]