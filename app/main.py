from datetime import date

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .database import engine, get_db
from .auth import get_current_user, authenticate_user, oauth2_scheme
from .auth import hash_pw, create_token_payload
from .schemas.activity import ActivityIn, ActivityOut
from .schemas.user import UserIn, UserOut
from .schemas.token import Token
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


@app.get('/user', response_model=list[UserOut])
async def get_users(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[UserOut]:
    return db.query(models.User).all()


@app.get('/user/me', response_model=UserOut)
async def get_my_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    return current_user


@app.post('/user', response_model=UserOut)
async def create_user(
    user: UserIn,
    db: Session = Depends(get_db)
) -> models.User:
    pw_hash = hash_pw(user.username, user.password)
    user_model = models.User(
        username=user.username,
        email=user.email,
        pw_hash=pw_hash
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model


@app.get('/activity/count', response_model=int)
async def activity_count(
    db: Session = Depends(get_db)
) -> int:
    return db.query(models.Activity).count()


@app.get('/activity', response_model=list[ActivityOut])
async def get_activities(
    activity_type: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    current_user: models.User = Depends(get_current_user),
) -> list[ActivityOut]:
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
    activity: ActivityIn,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_token_payload(user.username, form_data, db)
