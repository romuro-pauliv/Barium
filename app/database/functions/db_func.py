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


class POST:
    @staticmethod
    def add_wallet(chat_id: str, username: str, cache_data: dict[str, str]) -> None:
        from database.functions.post.add_wallet import post_add_wallet
        return post_add_wallet(chat_id, username, cache_data)