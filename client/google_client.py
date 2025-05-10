import requests
import httpx
from dataclasses import dataclass

from app.settings import Settings
from app.schema.user import GoogleUserData


# @dataclass
# class GoogleClient:
#     settings: Settings

#     def get_user_info(self, code: str) -> GoogleUserData:
#         access_token = self._get_user_access_token(code=code)
#         user_info = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
#                                  headers={'Authorization': f'Bearer {access_token}'})
#         return GoogleUserData(**user_info.json(), access_token=access_token)

#     def _get_user_access_token(self, code: str) -> str:
#         data = {
#             'code': code,
#             'client_id': self.settings.GOOGLE_CLIENT_ID,
#             'client_secret': self.settings.GOOGLE_CLIENT_SECRET,
#             'redirect_uri': self.settings.GOOGLE_REDIRECT_URI,
#             'grant_type': 'authorization_code',
#         }

#         response = requests.post(self.settings.GOOGLE_TOKEN_URL, data=data)
#         access_token = response.json()['access_token']
#         return access_token


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        # async with self.async_client as client:
        user_info = await self.async_client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return GoogleUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        # async with self.async_client as client:
        response = await self.async_client.post(
            self.settings.GOOGLE_TOKEN_URL, data=data
        )
        access_token = response.json()["access_token"]
        return access_token
