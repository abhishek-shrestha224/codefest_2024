from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from src.db.models import BBox, BBoxBase, Trip


class BBoxService:
    async def show(self, session: AsyncSession):
        statement = select(BBox).order_by(desc(BBox.id))
        resource = await session.exec(statement)
        return resource.all()

    async def retrieve(self, bbox_id: int, session: AsyncSession):
        statement = select(BBox).where(BBox.id == bbox_id)
        resource = await session.exec(statement)
        bbox = resource.first()
        return bbox if bbox else None

    async def create(self, bbox_data: BBoxBase, session: AsyncSession):
        bbox = BBox(
            area_name=bbox_data.area_name,
            lat1=bbox_data.lat1,
            lon1=bbox_data.lon1,
            lat2=bbox_data.lat2,
            lon2=bbox_data.lon2,
            trip_id=bbox_data.trip_id,
        )
        session.add(bbox)
        await session.commit()
        session.refresh(bbox)
        return bbox

    async def update(self, bbox_id: int, bbox_data: BBoxBase, session: AsyncSession):
        bbox_to_update = await self.retrieve(bbox_id, session)
        if bbox_to_update is None:
            return None
        update_data = bbox_data.model_dump()
        for k, v in update_data.items():
            setattr(bbox_to_update, k, v)
        bbox_to_update.updated_at = datetime.now()
        await session.commit()
        return bbox_to_update

    async def delete(self, bbox_id: int, session: AsyncSession):
        bbox_to_delete = await self.retrieve(bbox_id, session)
        if bbox_to_delete is None:
            return None
        await session.delete(bbox_to_delete)
        await session.commit()
        return bbox_to_delete

    async def get_trip(self, bbox_id: int, session: AsyncSession):
        bbox = await self.retrieve(bbox_id, session)
        statement = select(Trip).where(Trip.id == bbox.trip_id)
        resource = await session.exec(statement)
        trip = resource.first()
        return trip if trip else None
