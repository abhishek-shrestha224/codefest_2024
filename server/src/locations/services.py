from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from src.db.models import LocationBase, User, Location, BBox, Trip
from typing import List


class LocationService:
    async def show(self, session: AsyncSession):
        statement = select(Location).order_by(desc(Location.id))
        resource = await session.exec(statement)
        locations = resource.all()
        return locations if locations else []

    async def retrieve(self, location_id: int, session: AsyncSession):
        statement = select(Location).where(Location.id == location_id)
        resource = await session.exec(statement)
        location = resource.first()
        return location if location else None

    async def create(self, location_data: LocationBase, session: AsyncSession):
        location = Location(
            lat=location_data.lat,
            lon=location_data.lon,
            radius_km=location_data.radius_km,
            name=location_data.name,
            trip_id=location_data.trip_id,
            bbox_id=location_data.bbox_id,
        )
        session.add(location)
        await session.commit()
        session.refresh(location)
        return location

    async def update(
        self, location_id: int, location_data: LocationBase, session: AsyncSession
    ):
        location_to_update = await self.retrieve(location_id, session)
        if location_to_update is None:
            return None
        update_data = location_data.model_dump()
        for k, v in update_data.items():
            setattr(location_to_update, k, v)
        location_to_update.updated_at = datetime.now()
        await session.commit()
        return location_to_update

    async def delete(self, location_id: int, session: AsyncSession):
        location_to_delete = await self.retrieve(location_id, session)
        if location_to_delete is None:
            return None
        await session.delete(location_to_delete)
        await session.commit()
        return location_to_delete

    async def get_trip(self, location_id: int, session: AsyncSession):
        location = await self.retrieve(location_id, session)
        statement = select(Trip).where(Trip.id == location.trip_id)
        resource = await session.exec(statement)
        trip = resource.first()
        return trip if trip else None

    async def get_bbox(self, location_id: int, session: AsyncSession):
        location = await self.retrieve(location_id, session)
        statement = select(BBox).where(BBox.id == location.bbox_id)
        resource = await session.exec(statement)
        bbox = resource.first()
        return bbox if bbox else None

    async def get_all_users(
        self, location_id: int, session: AsyncSession
    ) -> List[User]:
        statement = select(User).where(User.location_id == location_id)
        resource = await session.exec(statement)
        users = resource.all()
        return users if users else []
