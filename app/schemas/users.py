from typing import Optional

from pydantic import BaseModel
from datetime import date


class UserCreate(BaseModel):
    fio: str
    password: str
    login: str
    mail: str
    phone_number: str

class UserProfile(BaseModel):
    fio: str
    login: str
    mail: str
    phone_number: str
    date_created: date
    roles: list
    locked: bool



class UserOut(BaseModel):
    id: int
    login: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    login: str
    password: str

class GettingToken(BaseModel):
    username: str
    password: str
    #scopes: list[str] = []

class GettingRefreshToken(BaseModel):
    refresh_token: str
