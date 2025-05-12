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
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(
    "/google",
    response_model=GoogleUserData,
)
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str,
):
    return await auth_service.google_auth(code=code)
