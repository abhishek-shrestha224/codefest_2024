from server.src.db.models import LocationBase
from .services import LocationService
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session

location_service = LocationService()
location_router = APIRouter()


@location_router.post("/create")
async def create(location: LocationBase, session: AsyncSession = Depends(get_session)):
    new_location = await location_service.create(location, session)
    return new_location


@location_router.get("/")
async def show(session: AsyncSession = Depends(get_session)):
    locations = await location_service.show(session)
    return locations


@location_router.get("/retrieve/{id}")
async def retrieve(id: int, session: AsyncSession = Depends(get_session)):
    location = await location_service.retrieve(id, session)
    if not location:
        raise HTTPException(status_code=404, detail="Not Found")
    return location


@location_router.patch("/update/{id}")
async def update(
    id: int, new_location: LocationBase, session: AsyncSession = Depends(get_session)
):
    updated_location = await location_service.update(id, new_location, session)
    if not updated_location:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated_location


@location_router.delete("/delete/{id}")
async def delete(id: int, session: AsyncSession = Depends(get_session)):
    deleted_location = await location_service.delete(id, session)
    if not deleted_location:
        raise HTTPException(status_code=404, detail="Not Found")
    return deleted_location
