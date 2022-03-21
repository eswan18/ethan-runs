import uuid

from sqlalchemy import Column, ForeignKey, Integer, Float, String, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .database import Base, get_db

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
    activity_type = Column(String)
    notes = Column(String)
    source = Column(String)
    link = Column(String)


class AuthToken(Base):
    __tablename__ = 'auth_tokens'

    token = Column(String, primary_key=True)
    expiration = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User')


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    pw_hash = Column(String)
