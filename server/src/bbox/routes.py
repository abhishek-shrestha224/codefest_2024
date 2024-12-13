from fastapi import APIRouter, HTTPException, Depends

from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.db.models import BBox, BBoxBase
from .services import BBoxService
from src.db.main import get_session


bbox_router = APIRouter()
bbox_service = BBoxService()


@bbox_router.post("/create", status_code=201, response_model=BBox)
async def create(
    bBox_data: BBoxBase,
    session: AsyncSession = Depends(get_session),
) -> dict:
    new_bbox = await bbox_service.create(bBox_data, session)
    return new_bbox


@bbox_router.get("/", response_model=List[BBox])
async def show(
    session: AsyncSession = Depends(get_session),
) -> list:
    bBoxs = await bbox_service.show(session)
    return bBoxs


@bbox_router.get("/retrieve/{id}", response_model=BBox)
async def retrieve(
    id: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    bbox = await bbox_service.retrieve(id, session)
    if bbox:
        return bbox
    else:
        raise HTTPException(status_code=404, detail=f"BBox with id {id} not found!!!")


@bbox_router.patch("/update/{id}", response_model=BBox)
async def update(
    id: str,
    bBox_data: BBoxBase,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_bbox = await bbox_service.update(id, bBox_data, session)
    if updated_bbox:
        return updated_bbox
    else:
        raise HTTPException(status_code=404, detail=f"BBox with id {id} not found!!!")


@bbox_router.delete("/delete/{id}", status_code=200)
async def delete(
    id: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    deleted_bbox = await bbox_service.delete(id, session)
    if deleted_bbox:
        return deleted_bbox
    else:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found!!!")
