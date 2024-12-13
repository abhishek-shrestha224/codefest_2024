from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from typing import List, Optional


class UserLogin(SQLModel):
    email: str
    password: str = Field(exclude=True)


class UserBase(UserLogin):
    username: str = Field(unique=True, max_length=16)
    first_name: str
    last_name: str
    address: str
    role: str = Field(default="user")
    geofence_id: int = Field(foreign_key="geofence.id", default=None)


class User(UserBase, table=True):
    id: int = Field(primary_key=True, default=None)
    geofence: "Geofence" = Relationship(back_populates="users")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class GeofenceBase(SQLModel):
    landmark: str
    lat: int
    lon: int
    radius: float


class Geofence(GeofenceBase, table=True):
    id: int = Field(primary_key=True, default=None)
    trip_id: Optional[int] = Field(foreign_key="trip.id", default=None)
    trip: Optional["Trip"] = Relationship(back_populates="geofences")
    users: List["User"] = Relationship(
        back_populates="geofence", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TripBase(SQLModel):
    name: str
    active: bool = Field(default=False)


class Trip(TripBase, table=True):
    id: int = Field(primary_key=True, default=None)
    geofences: List["Geofence"] = Relationship(
        back_populates="trip", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
