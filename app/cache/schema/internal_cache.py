
class Schema:
    class InternalCache:
        OPEN_ACCOUNT: list[str] = ["wallet_name", "amount", "obs"]
        NEW_WALLET: list[str] = ["wallet_name", "amount", "obs"]
        