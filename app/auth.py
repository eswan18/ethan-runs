import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import get_db
from . import models, schemas

SECRET_KEY = os.environ['APP_SECRET']
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, username: str) -> schemas.UserOut:
    user = Session.query(models.User).filter_by(username=username).first()
    return schemas.UserInDB(**user)

def verify_pw(
    username: str,
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(username + plain_password, hashed_password)

def hash_pw(username: str, password: str):
    return pwd_context.hash(username + password)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> schemas.UserOut:
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
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def authenticate_user(
    username: str,
    password: str,
    db: Session=Depends(get_db)
) -> schemas.UserOut | None:
    user = get_user(db, username)
    if not user:
        return None
    if not verify_pw(username, password, user.hashed_password):
        return None
    return user
