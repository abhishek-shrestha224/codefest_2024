from server.src.db.models import TripBase
from .services import TripService
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session

trip_service = TripService()
trip_router = APIRouter()


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
async def update(
    id: int, new_trip: TripBase, session: AsyncSession = Depends(get_session)
):
    updated_trip = await trip_service.update(id, new_trip, session)
    if not updated_trip:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated_trip


@trip_router.delete("/delete/{id}")
async def delete(id: int, session: AsyncSession = Depends(get_session)):
    deleted_trip = await trip_service.delete(id, session)
    if not deleted_trip:
        raise HTTPException(status_code=404, detail="Not Found")
    return deleted_trip
