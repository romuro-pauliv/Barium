# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     app.resources.data_provider.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pathlib import Path, PosixPath
from typing import Any
import json
# |--------------------------------------------------------------------------------------------------------------------|

class JsonReader(object):
    def __init__(self, *directory: str) -> None:
        self.directory: tuple[str] = directory
    
    def read_json(self, path_: PosixPath) -> dict[str, Any]:
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
    
    def file_data(self, filename: str) -> dict[str, Any]:
        """
        Retrieve the JSON data from a file.

        Args:
            filename (str): The name of the file to read.

        Returns: dict[str, Any]: The JSON data loaded from the file.
        """
        directory_file: PosixPath = Path(*self.directory, filename)
        return self.read_json(directory_file)