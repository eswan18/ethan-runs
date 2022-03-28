import uuid

from sqlalchemy import Column, Date, Integer, Float, Text, text
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class Activity(Base):
    __tablename__ = 'activity_fact'

    id = Column(Integer, primary_key=True)
    date_submitted = Column(Date)
    workout_date = Column(Date)
    avg_speed_in_mi_per_h = Column(Float)
    max_speed_in_mi_per_h = Column(Float)
    avg_heart_rate = Column(Integer)
    steps = Column(Integer)
    calories_burned_in_kcal = Column(Integer)
    distance_in_mi = Column(Float)
    workout_time_in_seconds = Column(Integer)
    avg_pace_in_min_per_mi = Column(Float)
    max_pace_in_min_per_mi = Column(Float)
    activity_type = Column(Text)
    notes = Column(Text)
    source = Column(Text)
    link = Column(Text)


class User(Base):
    __tablename__ = 'users'

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: str = Column(Text, unique=True, nullable=False)
    email: str = Column(Text, unique=True, nullable=False)
    pw_hash: str = Column(Text, nullable=False)
