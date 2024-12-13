from fastapi import APIRouter, HTTPException, Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from .models import Geofence, GeofenceBase
from .services import GeofenceService
from src.auth.services import UserService
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer

geofences_router = APIRouter()
geofence_service = GeofenceService()
security = AccessTokenBearer()
user_service = UserService()


@geofences_router.get("/", response_model=List[Geofence])
async def show(
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> list:
    geofences = await geofence_service.show(session)
    return geofences


@geofences_router.post("/create", status_code=201, response_model=Geofence)
async def create(
    geofence_data: GeofenceBase,
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    user_email = credentials.get("user")["email"]
    user = await user_service.retrieve_by_email(user_email, session)
    new_geofence = await geofence_service.create(geofence_data, user, session)
    return new_geofence


@geofences_router.get("/retrieve/{id}", response_model=Geofence)
async def retrieve(
    id: str,
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    geofence = await geofence_service.retrieve(id, session)
    if geofence:
        print(credentials)
        return geofence
    else:
        raise HTTPException(
            status_code=404, detail=f"Geofence with id {id} not found!!!"
        )


@geofences_router.patch("/update/{id}", response_model=Geofence)
async def update(
    id: str,
    geofence_data: GeofenceBase,
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    updated_geofence = await geofence_service.update(id, geofence_data, session)
    if updated_geofence:
        return updated_geofence
    else:
        raise HTTPException(
            status_code=404, detail=f"Geofence with id {id} not found!!!"
        )


@geofences_router.delete("/delete/{id}", status_code=200)
async def delete(
    id: str,
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    deleted_geofence = await geofence_service.delete(id, session)
    if deleted_geofence:
        return deleted_geofence
    else:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found!!!")
