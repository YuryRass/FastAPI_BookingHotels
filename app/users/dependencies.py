"""
Зависимости, которые применяются к пользователям,
заходящим на сайт 'BookingHotels'
"""

from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import COOKIE_KEY, settings
from app.exceptions import (
    IncorrectJWTtokenException,
    JWTtokenExpiredException,
    UserIsNotPresentException,
    UserUnauthorizedException,
)
from app.users.dao import UsersDAO
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
        payload: dict[str, str] = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectJWTtokenException

    expire: str | None = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise JWTtokenExpiredException

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user: Users = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
