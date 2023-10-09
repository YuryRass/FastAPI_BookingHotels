"""
Зависимости, которые применяются к пользователям,
заходящим на сайт 'BookingHotels'
"""

from datetime import datetime
from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from app.config import settings
from app.users.models import Users
from app.users.dao import UsersDAO


def get_token(request: Request) -> str | None:
    """Возвращает токен пользователя по его HTTP запросу

    Args:
        request (Request): HTTP запрос

    Raises:
        HTTPException: HTTP_401_UNAUTHORIZED

    Returns:
        str | None: токен пользователя
    """
    token: str = request.cookies.get('booking_access_token')
    print(token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User is unauthorized'
        )
    return token


async def get_current_user(token: str = Depends(get_token)) -> Users:
    """Возвращает пользователя по его JWT токену

    Args:
        token (str, optional): токен. Defaults to Depends(get_token).

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        Users: пользователь
    """
    try:
        payload: dict[str, str] = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=settings.JWT_ALGORITHM
        )
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=1)

    expire: str | None = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=2)

    user_id: str | None = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=3)

    user: Users = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=3)

    return user
