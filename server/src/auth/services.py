from src.db.models import User, UserBase
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


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
        new_user = User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            location_id=user.location_id,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
