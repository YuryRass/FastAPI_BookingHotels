from dataclasses import dataclass

import httpx
from fastapi import Depends

from app.config import Settings, get_settings
from app.users.shemas import GoogleUserData


@dataclass
class GoogleClient:
    settings: Settings

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        async with httpx.AsyncClient() as client:
            user_info = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
        return GoogleUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        return response.json()["access_token"]


async def get_google_client(
    settings: Settings = Depends(get_settings),
) -> GoogleClient:
    return GoogleClient(settings)
