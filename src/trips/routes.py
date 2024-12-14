from typing import List

from fastapi.security import HTTPAuthorizationCredentials
from src.auth.dependencies import AccessTokenBearer, RoleCheker
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
admin_role = Depends(RoleCheker(["admin"]))
security = AccessTokenBearer()


@trip_router.post("/create", dependencies=[admin_role])
async def create_trip(
    trip: TripBase,
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    new_trip = await trip_service.create(trip, session)
    return new_trip


@trip_router.get("/", dependencies=[admin_role])
async def show_trip(
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    trips = await trip_service.show(session)
    return trips


@trip_router.get("/retrieve/{id}", dependencies=[admin_role])
async def retrieve_trip(
    id: int,
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    trip = await trip_service.retrieve(id, session)
    if not trip:
        raise HTTPException(status_code=404, detail="Not Found")
    return trip


@trip_router.patch("/update/{id}", dependencies=[admin_role])
async def update_trip(
    id: int,
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    trip = await trip_service.retrieve(id, session)
    if not trip:
        raise HTTPException(status_code=404, detail="Not Found")
    updated_trip = await trip_service.update(
        id, TripBase(name=trip.name, active=not trip.active), session
    )
    if not updated_trip:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated_trip


@trip_router.delete("/delete/{id}", dependencies=[admin_role])
async def delete_trip(
    id: int,
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    deleted_trip = await trip_service.delete(id, session)
    if not deleted_trip:
        raise HTTPException(status_code=404, detail="Not Found")
    return deleted_trip


@trip_router.post("/{trip_id}/assign_locations", dependencies=[admin_role])
async def assign_locations(
    trip_id: int,
    location_ids: List[int],
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    return await trip_service.assign_locations_to_trip(trip_id, location_ids, session)


@trip_router.get("/{trip_id}/get_locations", dependencies=[admin_role])
async def get_locations(
    trip_id: int,
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    locations = await trip_service.get_all_locations(trip_id, session)
    updated_locations = []

    for location in locations:
        updated_location = await location_service.retrieve(location, session)
        updated_locations.append(updated_location)

    return updated_locations


@trip_router.get("/track")
async def track(
    session: AsyncSession = Depends(get_session),
    cred: HTTPAuthorizationCredentials = Depends(security),
):
    email = cred["user"]["email"]
    active_trip = await trip_service.is_trip_active(email, session)

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
