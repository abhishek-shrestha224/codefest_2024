from typing import List
from src.db.models import TripBase
from .services import TripService
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.locations.services import LocationService
from src.auth.services import UserService

trip_service = TripService()
trip_router = APIRouter()
location_service = LocationService()
user_service = UserService()


@trip_router.post("/create")
async def create(trip: TripBase, session: AsyncSession = Depends(get_session)):
    new_trip = await trip_service.create(trip, session)
    return new_trip


@trip_router.get("/")
async def show(session: AsyncSession = Depends(get_session)):
    trips = await trip_service.show(session)
    return trips


@trip_router.get("/retrieve/{id}")
async def retrieve(id: int, session: AsyncSession = Depends(get_session)):
    trip = await trip_service.retrieve(id, session)
    if not trip:
        raise HTTPException(status_code=404, detail="Not Found")
    return trip


@trip_router.patch("/update/{id}")
async def update(id: int, session: AsyncSession = Depends(get_session)):
    trip = await trip_service.retrieve(id, session)
    if not trip:
        raise HTTPException(status_code=404, detail="Not Found")
    updated_trip = await trip_service.update(
        id, TripBase(name=trip.name, active=not trip.active), session
    )
    if not updated_trip:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated_trip


@trip_router.delete("/delete/{id}")
async def delete(id: int, session: AsyncSession = Depends(get_session)):
    deleted_trip = await trip_service.delete(id, session)
    if not deleted_trip:
        raise HTTPException(status_code=404, detail="Not Found")
    return deleted_trip


@trip_router.post("/{trip_id}/assign_locations")
async def assign_locations(
    trip_id: int,
    location_ids: List[int],
    session: AsyncSession = Depends(get_session),
):
    return await trip_service.assign_locations_to_trip(trip_id, location_ids, session)


@trip_router.get("/{trip_id}/get_locations")
async def get_locations(
    trip_id: int,
    session: AsyncSession = Depends(get_session),
):
    locations = await trip_service.get_all_locations(trip_id, session)
    updated_locations = []

    for location in locations:
        updated_location = await location_service.retrieve(location, session)
        updated_locations.append(updated_location)

    return updated_locations


@trip_router.get("/{user_id}/track")
async def track(user_id: int, session: AsyncSession = Depends(get_session)):
    active_trip = await trip_service.is_trip_active(user_id, session)

    if not active_trip:
        return {"active": False, "message": "No active trip found"}

    locations = await trip_service.get_all_locations(active_trip.id, session)
    ordered_locations = []

    for location_id in locations:
        location = await location_service.retrieve(location_id, session)
        if location:
            ordered_locations.append(location)

    return {
        "active": True,
        "trip_data": {"trip": active_trip, "locations": ordered_locations},
    }
