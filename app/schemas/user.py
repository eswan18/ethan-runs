from uuid import UUID

from pydantic import BaseModel


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
