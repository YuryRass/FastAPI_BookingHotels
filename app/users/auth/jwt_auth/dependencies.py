"""
Зависимости, которые применяются к пользователям,
заходящим на сайт 'BookingHotels'
"""

import datetime as dt
from datetime import datetime
from typing import Any

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import COOKIE_KEY, settings
from app.exceptions import (
    IncorrectJWTtokenException,
    JWTtokenExpiredException,
    UserIsNotPresentException,
    UserUnauthorizedException,
)
from app.users.auth.jwt_auth.service import UserJWTAuthService
from app.users.dao import UsersDAO, get_user_dao
from app.users.models import Users


def get_token(request: Request) -> str | None:
    """Возвращает токен пользователя по его HTTP запросу

    Args:
        request (Request): HTTP запрос

    Raises:
        HTTPException: HTTP_401_UNAUTHORIZED

    Returns:
        str | None: токен пользователя
    """
    token: str | None = request.cookies.get(COOKIE_KEY)
    if not token:
        raise UserUnauthorizedException
    return token


async def get_current_user(token: str = Depends(get_token)) -> Users:
    """Возвращает пользователя по его JWT токену

    Args:
        token (str, optional): токен. Defaults to Depends(get_token).

    Raises:
        HTTPException: IncorrectJWTtokenException
        HTTPException: JWTtokenExpiredException
        HTTPException: UserIsNotPresentException

    Returns:
        Users: пользователь
    """
    try:
        payload: dict[str, Any] = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectJWTtokenException

    expire: int = payload["exp"]
    if (not expire) or (expire < datetime.now(tz=dt.UTC).timestamp()):
        raise JWTtokenExpiredException

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user: Users | None = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user


async def get_user_auth_service(user_dao: UsersDAO = Depends(get_user_dao)):
    return UserJWTAuthService(user_dao=user_dao)
