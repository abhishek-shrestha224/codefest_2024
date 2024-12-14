token_blacklist = {}


async def blacklist_token(jti: str) -> None:
    token_blacklist[jti] = {"value": ""}


async def is_token_revoked(jti: str) -> bool:
    token_data = token_blacklist.get(jti)
    return token_data is not None
