from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from src.db.models import LocationBase, Trip, TripLoc, User, Location
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

    async def get_all_users(
        self, location_id: int, session: AsyncSession
    ) -> List[User]:
        statement = select(User).where(User.location_id == location_id)
        resource = await session.exec(statement)
        users = resource.all()
        return users if users else []

    async def get_all_trip(self, location_id: int, session: AsyncSession) -> List[User]:
        result = await session.exec(
            select(Trip)
            .join(TripLoc, Trip.id == TripLoc.trip_id)
            .where(TripLoc.location_id == location_id)
        )
        trips = result.all()
        return trips
