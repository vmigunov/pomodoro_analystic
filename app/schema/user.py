from typing import Optional
from pydantic import BaseModel, Field


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str


class UserCreateSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None


class GoogleUserData(BaseModel):
    id: int
    email: str
    verified_email: bool
    name: str
    access_token: str


class YandexUserData(BaseModel):
    id: int
    login: str
    name: str = Field(alias="real_name")
    default_email: str
    access_token: str
