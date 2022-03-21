from pydantic import BaseModel

class ActivityBase(BaseModel):
    date_submitted: date
    workout_date: date
    avg_speed_in_mi_per_h: float
    max_speed_in_mi_per_h: float
    avg_heart_rate: int
    steps: int
    calories_burned_in_kcal: int
    distance_in_mi: float
    workout_time_in_seconds: int
    avg_pace_in_min_per_mi: float
    max_pace_in_min_per_mi: float
    activity_type: str
    notes: str
    source: str
    link: str

class ActivityCreate(ActivityBase):
    ...
