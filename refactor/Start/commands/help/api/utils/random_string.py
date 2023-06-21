# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         api.utils.random_string.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from random import randint
from typing import Union
# |--------------------------------------------------------------------------------------------------------------------|


def random_str_from_list(str_list: list[str]) -> Union[str, list[str]]:
    """
    When passing a list with elements, returns one element at random
    Args:
        str_list (list[str]): List containing elements

    Returns:
        Union[str, list[str]]: Random element from the element list
    """
    index: int = randint(0, len(str_list)-1)
    return str_list[index]