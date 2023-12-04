from fastapi import APIRouter, Depends, Response

from app.config import COOKIE_KEY
from app.exceptions import IncorrectEmailOrPasswordException, UserIsAllredyRegistered
from app.users.auth import authentication_user, create_jwt_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.shemas import SUserAuth

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["Auth & users"]
)


@router.post("/register")
async def user_register(user_data: SUserAuth) -> None:
    """Регистрация пользователя

    Args:

        user_data (SUserAuth): логин и пароль пользователя

    Raises:

        HTTPException: пользователь уже зареган
    """
    existing_user: Users | None = await UsersDAO.find_one_or_none(
        email=user_data.email
    )
    # Если пользователь уже есть в БД (т.е. он зарегитсрирован),
    # то мы вызываем исключение (повторная регистрация нам не нужна)
    if existing_user:
        raise UserIsAllredyRegistered
    password_hash: str = get_password_hash(
        password=user_data.password
    )
    await UsersDAO.add(
        email=user_data.email,
        hashed_password=password_hash
    )


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    """Вход пользователя на сайт

    Args:

        response (Response): HTTP ответ

        user_data (SUserAuth): данные о пользователе

    Raises:

        HTTPException: User is unauthorized!

    Returns:

        str: JWT токен
    """
    user: Users | None = await authentication_user(
        user_data.email, user_data.password
    )
    if not user:
        raise IncorrectEmailOrPasswordException
    else:
        jwt_token: str = create_jwt_token({"sub": str(user.id)})
        response.set_cookie(
            key=COOKIE_KEY,
            value=jwt_token,
            httponly=True
        )
        return jwt_token


@router.post('/logout')
async def logout_user(response: Response):
    """Выход пользователя из сайта

    Args:

        response (Response): HTTP ответ
    """
    response.delete_cookie(key=COOKIE_KEY)


@router.get('/me')
async def read_users_me(current_user: Users = Depends(get_current_user)):
    """Вывод инфорации о текущем пользователе

    Args:

        current_user (Users, optional): текущий пользователь.

    Returns:

        Users: текущий пользователь
    """
    return current_user
