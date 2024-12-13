from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from typing import List


class LocationBase(SQLModel):
    lat: float
    lon: float
    radius_km: float
    name: str
    trip_id: int = Field(foreign_key="trip.id", default=None)
    bbox_id: int = Field(foreign_key="bbox.id", default=None)


class Location(LocationBase, table=True):
    id: int = Field(primary_key=True, default=None)
    trip: "Trip" = Relationship(back_populates="locations")
    BBox: "BBox" = Relationship(back_populates="locations")
    users: List["User"] = Relationship(
        back_populates="location", sa_relationship_kwargs={"lazy": "selectin"}
    )


class UserBase(SQLModel):
    email: str
    first_name: str
    last_name: str
    address: str
    location_id: int = Field(foreign_key="location.id", default=None)
    role: str = Field(default="user")


class User(UserBase, table=True):
    id: int = Field(primary_key=True, default=None)
    location: "Location" = Relationship(back_populates="users")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class BBoxBase(SQLModel):
    area_name: str
    lon1: float
    lat1: float
    lon2: float
    lat2: float
    trip_id: int = Field(foreign_key="trip.id", default=None)


class BBox(BBoxBase, table=True):
    id: int = Field(primary_key=True, default=None)
    trip: "Trip" = Relationship(back_populates="bboxes")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TripBase(SQLModel):
    name: str


class Trip(TripBase, table=True):
    id: int = Field(primary_key=True, default=None)
    bboxes: List["BBox"] = Relationship(
        back_populates="trip", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)