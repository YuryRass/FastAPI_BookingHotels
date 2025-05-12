from dataclasses import dataclass

from fastapi import Response

from app.config import COOKIE_KEY
from app.exceptions import IncorrectEmailOrPasswordException, UserIsAllredyRegistered
from app.tasks.tasks import send_message_to_telegram_user
from app.users.auth.jwt_auth.jwt import (
    authentication_user,
    create_jwt_token,
    get_password_hash,
)
from app.users.dao import UsersDAO
from app.users.models import Users
from app.users.shemas import SUserAuth


@dataclass
class UserJWTAuthService:
    user_dao: UsersDAO

    async def user_register(self, user_data: SUserAuth) -> None:
        existing_user: Users | None = await self.user_dao.find_one_or_none(
            email=user_data.email
        )
        # Если пользователь уже есть в БД (т.е. он зарегитсрирован),
        # то мы вызываем исключение (повторная регистрация нам не нужна)
        if existing_user:
            raise UserIsAllredyRegistered
        password_hash: str = get_password_hash(password=user_data.password)
        await UsersDAO.add(email=user_data.email, hashed_password=password_hash)
        message_for_telegram_user = (
            f"Пользователь {user_data.email} зарегистрировался "
            "на сайте 'Booking hotels'"
        )

        await send_message_to_telegram_user(message_for_telegram_user)

    async def login_user(self, response: Response, user_data: SUserAuth):
        user: Users | None = await authentication_user(
            user_data.email, user_data.password
        )
        if not user:
            raise IncorrectEmailOrPasswordException
        else:
            jwt_token: str = create_jwt_token({"sub": str(user.id)})
            response.set_cookie(key=COOKIE_KEY, value=jwt_token, httponly=True)
            return jwt_token

    async def logout_user(self, response: Response):
        response.delete_cookie(key=COOKIE_KEY)

    async def read_users_me(
        self,
        current_user: Users,
    ):
        return current_user
