import random
import string

import datetime as dt
from datetime import timedelta, timezone
from jose import JWTError, jwt
from dataclasses import dataclass

from app.schema.user import UserLoginSchema
from app.repository.user import UserRepository
from app.exceptions import (
    TokenExpired,
    TokenNotCorrect,
    UserNotCorrectPasswordException,
    UserNotFoundException,
)
from app.models.user import UserProfile
from app.settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {"user_id": user_id, "exp": expires_date_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM,
        )
        return token

    def get_user_id_from_access_token(self, accesss_token: str) -> int:
        try:
            payload = jwt.decode(
                accesss_token,
                key=self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALGORITHM],
            )
        except JWTError:
            raise TokenNotCorrect

        if payload["exp"] < dt.datetime.utcnow().timestamp():
            raise TokenExpired

        return payload["user_id"]
