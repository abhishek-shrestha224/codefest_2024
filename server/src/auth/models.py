from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.geofences.models import Geofence


class UserLogin(SQLModel):
    email: str
    password: str = Field(exclude=True)


class UserBase(UserLogin):
    username: str = Field(unique=True, max_length=16)
    first_name: str
    last_name: str
    address: str
    role: str = Field(default="user")


class User(UserBase, table=True):
    id: int = Field(primary_key=True, default=None)
    geofence_id: Optional[int] = Field(foreign_key="geofence.id", default=None)
    geofence: "Geofence" = Relationship(back_populates="users")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
