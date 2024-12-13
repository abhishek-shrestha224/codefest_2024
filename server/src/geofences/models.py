from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from typing import List, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.auth.models import User
    from src.routes.models import Route


class GeofenceBase(SQLModel):
    landmark: str
    lat: int
    lon: int
    radius: float


class Geofence(GeofenceBase, table=True):
    id: int = Field(primary_key=True, default=None)
    route_id: Optional[int] = Field(foreign_key="route.id", default=None)
    route: Optional["Route"] = Relationship(back_populates="geofences")
    users: List["User"] = Relationship(
        back_populates="geofence", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
