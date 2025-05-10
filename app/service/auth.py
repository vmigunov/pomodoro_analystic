import random
import string
import secrets

import datetime as dt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dataclasses import dataclass

from app.schema.user import UserCreateSchema, UserLoginSchema
from app.repository.user import UserRepository
from app.exceptions import (
    TokenExpired,
    TokenNotCorrect,
    UserNotCorrectPasswordException,
    UserNotFoundException,
)
from app.models.user import UserProfile
from app.settings import Settings
from client.google_client import GoogleClient
from app.schema.user import GoogleUserData


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    async def google_auth(self, code: str) -> UserLoginSchema:
        user_data: GoogleUserData = await self.google_client.get_user_info(code=code)
        print(user_data)
        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)

            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            username=user_data.email.split("@")[0],
            password="oauth_user_no_password",
            email=user_data.email,
            name=user_data.name,
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)

        access_token = self.generate_access_token(user_id=user.id)  # Генерируем токен
        return UserLoginSchema(
            user_id=user.id, access_token=access_token
        )  # Возвращаем новый токен, а не user.access_token

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException("Пользователь не найден")
        if user.password != password:
            raise UserNotCorrectPasswordException("Неверный пароль")

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
