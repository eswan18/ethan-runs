from datetime import date

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .database import engine, get_db
from .auth import get_current_user, authenticate_user, oauth2_scheme
from .auth import hash_pw, create_token_payload
from . import schemas, models

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


@app.get('/user', response_model=list[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)) -> list[schemas.UserOut]:
    return db.query(models.User).all()


@app.get('/user/me', response_model=schemas.UserOut)
async def get_my_user(
        current_user: schemas.UserOut = Depends(get_current_user),
) -> schemas.UserOut:
    return current_user


@app.post('/user', response_model=schemas.UserOut)
async def create_user(
    user: schemas.UserIn,
    db: Session = Depends(get_db)
):
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
async def activity_count(db: Session = Depends(get_db)) -> int:
    return db.query(models.Activity).count()


@app.get('/activity', response_model=list[schemas.ActivityOut])
async def get_activities(
    activity_type: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    current_user: schemas.UserOut = Depends(get_current_user),
) -> list[schemas.ActivityOut]:
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
    activity: schemas.ActivityIn,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user),
):
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


@app.post("/token", response_model=schemas.Token)
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
