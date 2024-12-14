from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from src.db.models import Trip, TripBase, Location, TripLoc
from typing import List
from src.locations.services import LocationService
from src.auth.services import UserService

user_service = UserService()
location_service = LocationService()


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
        statement = (
            select(TripLoc.location_id)
            .where(TripLoc.trip_id == trip_id)
            .order_by(TripLoc.order)
        )

        result = await session.exec(statement)
        trip_locations = result.all()
        return trip_locations

    async def assign_locations_to_trip(
        self, trip_id: int, location_ids: List[int], session: AsyncSession
    ):
        statement = select(Trip).where(Trip.id == trip_id)
        result = await session.exec(statement)
        trip = result.first()

        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")

        for index, location_id in enumerate(location_ids):
            statement = select(Location).where(Location.id == location_id)
            result = await session.exec(statement)
            location = result.first()

            if not location:
                raise HTTPException(
                    status_code=404, detail=f"Location with ID {location_id} not found"
                )

            statement = (
                select(TripLoc)
                .where(TripLoc.trip_id == trip_id)
                .where(TripLoc.location_id == location_id)
            )
            result = await session.exec(statement)
            trip_location = result.first()

            if trip_location:
                trip_location.order = index
                session.add(trip_location)
            else:
                new_trip_location = TripLoc(
                    trip_id=trip_id, location_id=location_id, order=index
                )
                session.add(new_trip_location)

        await session.commit()
        return {"message": "Locations assigned to the trip successfully"}

    async def trip_active(self, trip_id: int, session: AsyncSession):
        trip = await self.retrieve(trip_id, session)
        if trip is None:
            return None
        return trip.active

    async def is_trip_active(self, email: str, session: AsyncSession):
        user = await user_service.retrieve(email, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        loc = await user_service.get_location(user, session)
        if not loc:
            raise HTTPException(status_code=404, detail="User location not found")

        trips = await location_service.get_all_trip(loc.id, session)
        for trip in trips:
            if await self.trip_active(trip.id, session):
                return trip

        return None
