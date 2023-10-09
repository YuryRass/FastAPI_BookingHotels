from fastapi import APIRouter, HTTPException, Response, status
from app.users.shemas import SUserAuth
from app.users.dao import UsersDAO
from app.users.models import Users
from app.users.auth import \
    authentication_user, create_jwt_token, get_password_hash

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
        HTTPException: если пользователь уже зареган
    """
    existing_user: Users | None = await UsersDAO.find_one_or_none(
        email=user_data.email
    )
    # Если пользователь уже есть в БД (т.е. он зарегитсрирован),
    # то мы вызываем исключение (повторная регистрация нам не нужна)
    if existing_user:
        raise HTTPException(
            status_code=500, detail="User is allready registered"
        )
    password_hash: str = get_password_hash(
        password=user_data.password
    )
    await UsersDAO.add(
        email=user_data.email,
        hashed_password=password_hash
    )


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user: Users | None = await authentication_user(
        user_data.email, user_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized!"
        )
    else:
        jwt_token: str = create_jwt_token({"sub": str(user.id)})
        response.set_cookie(
            key="booking_access_token",
            value=jwt_token,
            httponly=True
        )
        return jwt_token
