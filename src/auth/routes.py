from fastapi import APIRouter, Depends, HTTPException
from src.db.models import User, UserBase
from .services import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession


auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/signup", response_model=User, status_code=200)
async def create_user_account(
    user: UserBase, session: AsyncSession = Depends(get_session)
):
    email = user.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=403, detail=f"User with email: {email} already exists"
        )
    new_user = await user_service.create(user, session)
    return new_user


@auth_router.get("/retrieve/{email}", response_model=User, status_code=200)
async def retrieve(email: str, session: AsyncSession = Depends(get_session)):
    user = await user_service.retrieve(email, session)
    if not user:
        raise HTTPException(
            status_code=403, detail=f"User with email: {email} already exists"
        )
    return user
