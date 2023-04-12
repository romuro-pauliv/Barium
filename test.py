from pymongo import MongoClient, cursor

id_: str = "5815426488"

db: MongoClient = MongoClient("mongodb://localhost:27017/")


def get_wallet_list(chat_id: str) -> list[str]:
    database_name: str = f"AYLA_{chat_id}"
    documents: cursor.Cursor = db[database_name]["/WALLETS"].find({})

    wallet_list: list[str] = []
    
    for doc in documents:
        wallet_list.append(doc["wallet"])
    
    return wallet_list