from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from src.locations.services import LocationService
from src.auth.services import UserService
from .services import TripService

user_service = UserService()
trip_service = TripService()
location_service = LocationService()


async def is_trip_active(user_id: int, session: AsyncSession):
    user = await user_service.retrieve_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    loc = await user_service.get_location(user, session)
    if not loc:
        raise HTTPException(status_code=404, detail="User location not found")

    trips = await location_service.get_all_trip(loc.id, session)
    for trip in trips:
        if await trip_service.trip_active(trip.id, session):
            return trip

    return None
