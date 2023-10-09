"""Модуль отвечает за хеширование и сверку пользоватльских паролей"""

from passlib.context import CryptContext

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
        bool: возвращает True, если пароли соответсвуют друг другу
    """
    return pwd_context.verify(secret, hash)


