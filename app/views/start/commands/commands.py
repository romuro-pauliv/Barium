# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               app.views.start.commands.commands.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import TelegramConfig, Tools
# |--------------------------------------------------------------------------------------------------------------------|

COMMANDS_LIST: dict[str, str] = Tools.read_json(TelegramConfig.COMMANDS)["start_commands"]
ABOUT_COMMANDS: dict[str, dict] = Tools.read_json(TelegramConfig.COMMANDS)["about_commands"]["start_commands"]