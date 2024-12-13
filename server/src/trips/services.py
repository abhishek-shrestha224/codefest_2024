from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from src.db.models import Trip, TripBase, Location
from typing import List


class TripService:
    async def show(self, session: AsyncSession):
        statement = select(Trip).order_by(desc(Trip.id))
        resource = await session.exec(statement)
        trips = resource.all()
        return trips if trips else []

    async def retrieve(self, trip_id: int, session: AsyncSession):
        statement = select(Trip).where(Trip.id == trip_id)
        resource = await session.exec(statement)
        trip = resource.first()
        return trip if trip else None

    async def create(self, trip_data: TripBase, session: AsyncSession):
        trip = Trip(name=trip_data.name)
        session.add(trip)
        await session.commit()
        session.refresh(trip)
        return trip

    async def update(self, trip_id: int, trip_data: TripBase, session: AsyncSession):
        trip_to_update = await self.retrieve(trip_id, session)
        if trip_to_update is None:
            return None
        update_data = trip_data.model_dump()
        for k, v in update_data.items():
            setattr(trip_to_update, k, v)
        trip_to_update.updated_at = datetime.now()
        await session.commit()
        return trip_to_update

    async def delete(self, trip_id: int, session: AsyncSession):
        trip_to_delete = await self.retrieve(trip_id, session)
        if trip_to_delete is None:
            return None
        await session.delete(trip_to_delete)
        await session.commit()
        return trip_to_delete

    async def get_all_locations(
        self, trip_id: int, session: AsyncSession
    ) -> List[Location]:
        statement = select(Location).where(Location.trip_id == trip_id)
        resource = await session.exec(statement)
        locations = resource.all()
        return locations if locations else []
