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
    MS_ROUTES: dict[str, Any] = Tools.read_json(ms_routes)