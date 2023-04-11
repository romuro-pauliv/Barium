# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                              app.views.client.commands.commands.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import TelegramConfig
# |--------------------------------------------------------------------------------------------------------------------|

commands_json: dict[str, dict[str]] = TelegramConfig.COMMANDS

COMMANDS_LIST: dict[str, str] = commands_json["client_commands"]
ABOUT_COMMANDS: dict[str, str] = commands_json["about_commands"]["client_commands"]

