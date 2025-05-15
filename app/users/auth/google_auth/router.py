from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.users.auth.google_auth.dependencies import get_auth_service
from app.users.auth.google_auth.service import AuthService
from app.users.shemas import GoogleUserData

router = APIRouter(prefix="/auth", tags=["Google auth"])


@router.get("/login/google", response_class=RedirectResponse)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url) # ссылка для ввода гугл учетки
    return RedirectResponse(redirect_url)


@router.get(
    "/google",
    response_model=GoogleUserData,
)
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str,
):
    """
    Демо вариант гугл авторизации.
    В реальных случаях учетная запись пользователя (с зашифрованным паролем)
    сохранеятся в БД, создается JWT токен, который добавляется в куки.
    """
    return await auth_service.google_auth(code=code)
