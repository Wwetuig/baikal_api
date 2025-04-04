from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    fio: str
    password: str
    login: str
    mail: str
    phone_number: str


class UserOut(BaseModel):
    id: int
    login: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    login: str
    password: str