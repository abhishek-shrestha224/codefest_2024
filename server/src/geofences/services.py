from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from src.db.models import Geofence, GeofenceBase


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

    async def create(self, geofence_data: GeofenceBase, session: AsyncSession):
        geofence = Geofence(
            landmark=geofence_data.landmark,
            lat=geofence_data.lat,
            lon=geofence_data.lon,
            radius=geofence_data.radius,
        )
        session.add(geofence)
        await session.commit()
        session.refresh(geofence)
        return geofence

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
