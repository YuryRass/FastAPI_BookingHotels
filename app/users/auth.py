"""Модуль отвечает за хеширование и сверку пользоватльских паролей"""
from datetime import datetime, timedelta
from jose import jwt
from pydantic import EmailStr
from passlib.context import CryptContext

from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Возвращает захешированный пароль

    Args:
        password (str): пароль

    Returns:
        str: захешированный пароль
    """
    return pwd_context.hash(secret=password)


def verify_password(secret: str, hash: str) -> bool:
    """Сверяет пароль с его хешем

    Args:
        secret (str): пароль
        hash (str): захешированный пароль

    Returns:
        bool: возвращает True, если при расхешировании пароли
    соответсвуют друг другу
    """
    return pwd_context.verify(secret, hash)


async def authentication_user(
    user_email: EmailStr, user_password: str
) -> Users | None:
    """Аутентификация пользователя.

    Args:
        user_email (EmailStr): e-mail пользователя
        user_password (str): пароль пользователя

    Returns: Users | None
    """
    user_from_db: Users | None
    user_from_db = await UsersDAO.find_one_or_none(
        email=user_email
    )

    # если e-mail пользователя или
    # хеш его пароля отсутствует в БД,
    # то возвращаем None значение
    if (
        not user_from_db or
        not verify_password(user_password, user_from_db.hashed_password)
    ):
        return None
    # в противном случае, возвращаем данного пользователя
    else:
        return user_from_db


def create_jwt_token(data: dict[str, str]) -> str:
    """Создание JWT токена для пользователя

    Args:
        data (dict[str, str]): полезная нагрузка

    Returns:
        str: JWT токен
    """
    to_encode: dict[str, str] = data.copy()

    # добавляем в полезную нагрузку
    # время жизни JWT токена пользователя
    expire: datetime = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    jwt_token: str = jwt.encode(
        claims=to_encode, key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return jwt_token
