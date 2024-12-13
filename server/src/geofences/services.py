from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from .models import Geofence, GeofenceBase
from src.auth.models import User


class GeofenceService:
    async def show(self, session: AsyncSession):
        statement = select(Geofence).order_by(desc(Geofence.id))
        resource = await session.exec(statement)
        return resource.all()

    async def retrieve(self, geofence_id: str, session: AsyncSession):
        statement = select(Geofence).where(Geofence.id == geofence_id)
        resource = await session.exec(statement)
        geofence = resource.first()
        return geofence if geofence else None

    async def create(
        self, geofence_data: GeofenceBase, user: User, session: AsyncSession
    ):
        geofence_data = Geofence(
            title=geofence_data.title,
            author=geofence_data.author,
            publisher=geofence_data.publisher,
            published_date=geofence_data.published_date,
            page_count=geofence_data.page_count,
            language=geofence_data.language,
            user=user,
        )
        session.add(geofence_data)
        await session.commit()
        session.refresh(geofence_data)
        return geofence_data

    async def update(
        self, geofence_id: str, geofence_data: GeofenceBase, session: AsyncSession
    ):
        geofence_to_update = await self.retrieve(geofence_id, session)
        if geofence_to_update is None:
            return None
        update_data = geofence_data.model_dump()
        for k, v in update_data.items():
            setattr(geofence_to_update, k, v)
        geofence_to_update.updated_at = datetime.now()
        await session.commit()
        return geofence_to_update

    async def delete(self, geofence_id: str, session: AsyncSession):
        geofence_to_delete = await self.retrieve(geofence_id, session)
        if geofence_to_delete is None:
            return None
        await session.delete(geofence_to_delete)
        await session.commit()
        return geofence_to_delete.model_dump()
