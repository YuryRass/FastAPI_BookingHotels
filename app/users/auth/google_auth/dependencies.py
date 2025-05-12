from fastapi import Depends

from app.config import Settings, get_settings
from app.users.auth.google_auth.google import GoogleClient, get_google_client
from app.users.auth.google_auth.service import AuthService
from app.users.dao import UsersDAO, get_user_dao


async def get_auth_service(
    user_dao: UsersDAO = Depends(get_user_dao),
    google_client: GoogleClient = Depends(get_google_client),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    return AuthService(
        user_dao,
        settings,
        google_client,
    )
