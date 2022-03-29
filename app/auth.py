import os
from configparser import ConfigParser
from datetime import timedelta, datetime
from pathlib import Path

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt  # type: ignore
from sqlalchemy.orm import Session

from .database import get_db
from . import models

if 'APP_SECRET' in os.environ:
    SECRET_KEY = os.environ['APP_SECRET']
elif Path('./secrets.ini').exists():
    parser = ConfigParser()
    parser.read('./secrets.ini')
    SECRET_KEY = parser['DEVELOPMENT']['APP_SECRET']
else:
    raise RuntimeError('No app secret key found')

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRATION_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(
    db: Session,
    username: str,
) -> models.User:
    user = db.query(models.User).filter_by(username=username).first()
    if user is None:
        raise ValueError(f'Username {username} does not exist')
    return user


def verify_pw(
    username: str,
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(username.lower() + plain_password, hashed_password)


def hash_pw(
    username: str,
    password: str
) -> str:
    return pwd_context.hash(username.lower() + password)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token_data = schemas.token.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def authenticate_user(
    username: str,
    password: str,
    db: Session = Depends(get_db)
) -> models.User | None:
    try:
        user = get_user(db, username)
    except ValueError:
        return None
    if not verify_pw(username, password, user.pw_hash):
        return None
    return user


def create_token_payload(
    username: str,
    form_data: OAuth2PasswordRequestForm,
    db: Session,
    expiration_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES),
) -> dict[str, str]:
    access_token = create_access_token(
        data={"sub": username}, expiration_delta=expiration_delta
    )
    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(
    data: dict[str, str],
    expiration_delta: timedelta,
) -> str:
    expire_time = datetime.utcnow() + expiration_delta
    to_encode = data | {'exp': expire_time}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
