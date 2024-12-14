from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.blacklist import is_token_revoked
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .services import UserService
from typing import List
from src.db.models import User

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)

        token = credentials.credentials

        token_data = decode_token(token)

        if await is_token_revoked(token_data["jti"]):
            raise HTTPException(status_code=403, detail="This token has been revoked.")

        self.verify_token_data(token_data)
        print(token_data)
        return token_data

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=403, detail="Refresh token used to access a resource."
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=403, detail="Access token used to create a new token."
            )


async def get_curr_user(
    token: HTTPAuthorizationCredentials = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
) -> User:
    email = token["user"]["email"]
    user = await user_service.retrieve(email, session)
    return user


class RoleCheker:
    def __init__(self, valid_roles: List[str]) -> None:
        self.valid_roles = valid_roles

    async def __call__(self, curr_user: User = Depends(get_curr_user)):
        if curr_user.role not in self.valid_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return True
