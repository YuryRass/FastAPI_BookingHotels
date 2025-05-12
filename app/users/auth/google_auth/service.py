from dataclasses import dataclass

from app.config import Settings
from app.users.auth.google_auth.google import GoogleClient
from app.users.dao import UsersDAO
from app.users.shemas import GoogleUserData


@dataclass
class AuthService:
    user_dao: UsersDAO
    settings: Settings
    google_client: GoogleClient

    async def google_auth(self, code: str) -> GoogleUserData:
        user_data = await self.google_client.get_user_info(code)
        return user_data

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url
