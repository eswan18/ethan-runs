from datetime import date
from uuid import UUID

from pydantic import BaseModel


class ActivityBase(BaseModel):
    date_submitted: date
    workout_date: date
    avg_speed_in_mi_per_h: float
    max_speed_in_mi_per_h: float
    avg_heart_rate: int | None
    steps: int | None
    calories_burned_in_kcal: int
    distance_in_mi: float
    workout_time_in_seconds: int
    avg_pace_in_min_per_mi: float
    max_pace_in_min_per_mi: float
    activity_type: str
    notes: str
    source: str | None
    link: str


class ActivityCreate(ActivityBase):
    ...


class Activity(ActivityBase):

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    id: UUID
    pw_hash: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
