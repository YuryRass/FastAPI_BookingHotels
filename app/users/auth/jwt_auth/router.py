from fastapi import APIRouter, Depends, Response

from app.users.auth.jwt_auth.dependencies import get_current_user, get_user_auth_service
from app.users.auth.jwt_auth.service import UserJWTAuthService
from app.users.models import Users
from app.users.shemas import SUserAuth

router: APIRouter = APIRouter(
    prefix="/jwt-auth",
    tags=["JWT Auth & users"],
)


@router.post("/register", summary="Регистрация пользователя")
async def user_register(
    user_data: SUserAuth,
    user_service: UserJWTAuthService = Depends(get_user_auth_service),
) -> None:
    """Регистрация пользователя

    Args:

        user_data (SUserAuth): логин и пароль пользователя

    Raises:

        HTTPException: пользователь уже зареган
    """
    await user_service.user_register(user_data=user_data)


@router.post("/login", summary="Вход на сайт")
async def login_user(
    response: Response,
    user_data: SUserAuth,
    user_service: UserJWTAuthService = Depends(get_user_auth_service),
) -> str:
    """Вход пользователя на сайт

    Args:

        response (Response): HTTP ответ

        user_data (SUserAuth): данные о пользователе

    Raises:

        HTTPException: User is unauthorized!

    Returns:

        str: JWT токен
    """
    return await user_service.login_user(response, user_data)


@router.post("/logout", summary="Выход из сайта")
async def logout_user(
    response: Response,
    user_service: UserJWTAuthService = Depends(get_user_auth_service),
):
    """Выход пользователя из сайта

    Args:

        response (Response): HTTP ответ
    """
    await user_service.logout_user(response)


@router.get("/me", summary="Информация о пользователе")
async def read_users_me(
    user_service: UserJWTAuthService = Depends(get_user_auth_service),
    current_user: Users = Depends(get_current_user),
):
    """Вывод инфорации о текущем пользователе

    Args:

        current_user (Users, optional): текущий пользователь.

    Returns:

        Users: текущий пользователь
    """
    return await user_service.read_users_me(current_user)
