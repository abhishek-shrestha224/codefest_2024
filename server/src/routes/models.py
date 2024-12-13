from sqlmodel import SQLModel, Field, Relationship
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.geofences.models import Geofence


class RouteBase(SQLModel):
    name: str
    active: bool = Field(default=False)


class Route(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    geofences: List["Geofence"] = Relationship(
        back_populates="route", sa_relationship_kwargs={"lazy": "selectin"}
    )
