from src.db.models import User, UserBase
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .utils import generate_hash


class UserService:
    async def retrieve_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        resource = await session.exec(statement)
        user = resource.first()
        return user

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.retrieve_by_email(email, session)
        return True if user else False

    async def create(self, user: UserBase, session: AsyncSession):
        password_hash = generate_hash(user.password)
        new_user = User(
            username=user.username,
            email=user.email,
            password=password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
