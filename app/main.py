from datetime import date, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .database import engine, get_db
from .schemas import Activity, ActivityCreate, User
from .auth import get_current_user, authenticate_user, verify_pw, hash_pw, oauth2_scheme
from . import models

ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def hello():
    return 'Hello Ethan!'

@app.get('/hello/{name}')
async def hello_name(name: str):
    return f'Hello {name}'

@app.get('/activity/count')
async def activity_count(db: Session = Depends(get_db)):
    return db.query(models.Activity).count()

@app.get('/activity', response_model=list[Activity])
async def get_activities(
    activity_type: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    current_user = Depends(get_current_user),
) -> list[Activity]:
    activities = db.query(models.Activity)
    # TODO: Some validating that there are no query params except those used
    # in filters below.
    if activity_type:
        activities = activities.filter_by(activity_type=activity_type)
    if start_date:
        activities = activities.filter(models.Activity.workout_date > start_date)
    if end_date:
        activities = activities.filter(models.Activity.workout_date < end_date)
    return activities.all()

@app.post('/activity')
async def create_activity(
    activity: ActivityCreate,
    token: str = Depends(oauth2_scheme),
    current_user = Depends(get_current_user),
):
    db_activity = models.Activity(**activity)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
