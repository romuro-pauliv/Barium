# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                  app.database.functions.db_func.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|


class GET:
    @staticmethod
    def wallet_list(chat_id: str) -> list[str]:
        from database.functions.get.wallet_list import get_wallet_list
        return get_wallet_list(chat_id)