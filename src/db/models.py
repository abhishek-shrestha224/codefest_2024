from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from typing import List


# Base model for the user
class UserBase(SQLModel):
    email: str = Field(unique=True)
    first_name: str
    last_name: str
    address: str
    location_id: int = Field(foreign_key="location.id", default=None)
    role: str = Field(default="user")


# User model with a primary key and relationships
class User(UserBase, table=True):
    id: int = Field(primary_key=True, default=None)
    location: "Location" = Relationship(back_populates="users")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# Base model for location
class LocationBase(SQLModel):
    lat: float
    lon: float
    radius_km: float
    name: str


# Location model with a primary key and relationships
class Location(LocationBase, table=True):
    id: int = Field(primary_key=True, default=None)
    users: List["User"] = Relationship(
        back_populates="location", sa_relationship_kwargs={"lazy": "selectin"}
    )
    trips: List["TripLoc"] = Relationship(
        back_populates="location", sa_relationship_kwargs={"lazy": "selectin"}
    )


# Base model for trip
class TripBase(SQLModel):
    name: str
    active: bool = Field(default=False)


class Trip(TripBase, table=True):
    id: int = Field(primary_key=True, default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    trip_locations: List["TripLoc"] = Relationship(
        back_populates="trip", sa_relationship_kwargs={"lazy": "selectin"}
    )


class TripLoc(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    trip_id: int = Field(foreign_key="trip.id")
    location_id: int = Field(foreign_key="location.id")
    order: int
    trip: "Trip" = Relationship(back_populates="trip_locations")
    location: "Location" = Relationship(back_populates="trips")
