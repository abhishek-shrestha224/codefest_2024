from fastapi.security import HTTPAuthorizationCredentials
from src.auth.dependencies import AccessTokenBearer, RoleCheker
from src.db.models import LocationBase
from .services import LocationService
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session

location_service = LocationService()
location_router = APIRouter()
admin_role = Depends(RoleCheker(["admin"]))
security = AccessTokenBearer()


@location_router.post("/create", dependencies=[admin_role])
async def create_location(
    location: LocationBase,
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    new_location = await location_service.create(location, session)
    return new_location


@location_router.get("/", dependencies=[admin_role])
async def show_location(
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    locations = await location_service.show(session)
    return locations


@location_router.get("/retrieve/{id}", dependencies=[admin_role])
async def retrieve_location(
    id: int,
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    location = await location_service.retrieve(id, session)
    if not location:
        raise HTTPException(status_code=404, detail="Not Found")
    return location


@location_router.patch("/update/{id}", dependencies=[admin_role])
async def update_location(
    id: int,
    new_location: LocationBase,
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    updated_location = await location_service.update(id, new_location, session)
    if not updated_location:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated_location


@location_router.delete("/delete/{id}", dependencies=[admin_role])
async def delete_location(
    id: int,
    session: AsyncSession = Depends(get_session),
    _: HTTPAuthorizationCredentials = Depends(security),
):
    deleted_location = await location_service.delete(id, session)
    if not deleted_location:
        raise HTTPException(status_code=404, detail="Not Found")
    return deleted_location
