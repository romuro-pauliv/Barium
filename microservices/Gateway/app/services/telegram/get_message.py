# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               app.services.telegram.get_message.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from connections.telegram import TelegramRequests

from typing import Union, Any
# |--------------------------------------------------------------------------------------------------------------------|


class Core(TelegramRequests):
    def __init__(self) -> None:
        super().__init__()
        self.endpoints: dict[str, str] = self.route["endpoints"]
        self.update_id: int = 0
        self.cache: dict[str, dict[str, Any]] = {"last_message": {}}
        
        self.client_data: list[int] = []
        
    def last_message(self) -> Union[dict[str, dict[str, Union[str, list]]], None]:
        """
        Request the latest update from Telegram API and manipulate the data to
        return 'None' which the update is the same as the previous update
        Returns:
            Union[dict[str, dict[str, Union[str, list]]], None]: Return the last update from Telegram API
        """
        
        # request from  telegram API
        response: Union[dict[str, Any], None] = self.make_request(
            "GET", self.endpoints['updates'], {"offset": self.update_id}
        )
        
        if response != None:
            updates: dict[str, Any] = response["result"]
        
            # Var definition
            chat_ids: list[str] = []
            last_msg: dict[str, Union[str, list[str, bool]]] = {}
            new_messages: dict[str, dict[str, Any]] = {}
        
            for update in updates:
                self.update_id: int = int(update["update_id"])
            
                if "message" in [keys for keys in update.keys()]:
                    data: dict[str, str] = update["message"]
                
                    # extract data from api response
                    chat_id: str = data["chat"]["id"]
                    username: str = data["chat"]["first_name"]
                    date: str = data["date"]

                    # | Send client data to data loading |-------------------------------------------------------------|
                    if chat_id not in self.client_data:
                        pass
                    # |------------------------------------------------------------------------------------------------|
                    
                    # if user send a image, video, gif, etc. -> list[str, bool]
                    try:
                        text: str = data["text"]
                    except KeyError:
                        text: list[str, bool] = ["BIN", True]
                
                    # Build json message
                    if chat_id in chat_ids:
                        if last_msg[chat_id]["date"] < date:
                            last_msg[chat_id] = {"username": username, "date": date, "text": text}
                    else:
                        chat_ids.append(chat_id)
                        last_msg[chat_id] = {"username": username, "date": date, "text": text}
        
            # Build msg packet
            chat_id_in_cache: list[str] = [_id for _id in last_msg.keys()]
            for _id in chat_id_in_cache:
                try:
                    old_message: dict[str, str] = self.cache["last_message"][_id]
                    if old_message != last_msg[_id] and old_message["date"] < last_msg[_id]["date"]:
                        self.cache["last_message"][_id] = last_msg[_id]
                        new_messages[_id] = last_msg[_id]
            
                except KeyError:
                    self.cache["last_message"][_id] = last_msg[_id]
                    new_messages[_id] = last_msg[_id]
        
            return new_messages if new_messages else None
        return None