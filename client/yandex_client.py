from dataclasses import dataclass
import httpx

from app.schema.user import YandexUserData
from app.settings import Settings


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str):
        access_token = await self._get_user_access_token(code=code)
        user_info = await self.async_client.get(
                "https://login.yandex.ru/info?format=json",
                headers={"Authorization": f"OAuth {access_token}"},
            )
        # print("Response from Yandex:", user_info.json())
        return YandexUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        response = await self.async_client.post(  # <- Без `async with`
            self.settings.YANDEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.settings.YANDEX_CLIENT_ID,
                "client_secret": self.settings.YANDEX_SECRET_KEY,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        return response.json()["access_token"]