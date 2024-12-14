from src.auth.utils import generate_hash
from src.db.models import User, UserBase, Location
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime


class UserService:
    async def retrieve(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        resource = await session.exec(statement)
        user = resource.first()
        return user

    async def retrieve_by_id(self, id: id, session: AsyncSession):
        statement = select(User).where(User.id == id)
        resource = await session.exec(statement)
        user = resource.first()
        return user

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.retrieve(email, session)
        return True if user else False

    async def create(self, user: UserBase, session: AsyncSession):
        password_hash = generate_hash(user.password)
        new_user = User(
            email=user.email,
            password=password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            address=user.address,
            location_id=user.location_id,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def update(self, user_id: str, user_data: UserBase, session: AsyncSession):
        user_to_update = await self.retrieve(user_id, session)
        if user_to_update is None:
            return None
        update_data = user_data.model_dump()
        for k, v in update_data.items():
            setattr(user_to_update, k, v)
        user_to_update.updated_at = datetime.now()
        await session.commit()
        return user_to_update

    async def delete(self, user_id: str, session: AsyncSession):
        user_to_delete = await self.retrieve(user_id, session)
        if user_to_delete is None:
            return None
        await session.delete(user_to_delete)
        await session.commit()
        return user_to_delete

    async def get_location(self, user: User, session: AsyncSession) -> Location:
        statement = select(Location).where(Location.id == user.location_id)
        resource = await session.exec(statement)
        location = resource.first()
        return location if location else None
