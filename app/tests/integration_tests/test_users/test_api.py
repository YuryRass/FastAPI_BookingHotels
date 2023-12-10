import pytest
from httpx import AsyncClient, Response

from app.config import COOKIE_KEY


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test_user@mail.ru", "password1", 200),
        ("test_user@mail.ru", "password2", 401),
        ("new_test_user@mail.ru", "password3", 200),
    ],
)
async def test_user_register(
    ac: AsyncClient, email: str, password: str, status_code: int
):
    resp: Response = await ac.post(
        url="/auth/register",
        json={"email": email, "password": password},
    )

    assert resp.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code,exist_token",
    [
        ("test@test.com", "test", 200, True),
        ("not_exist@test.com", "test", 401, False),
        ("incorrect_email", "test", 422, False),
    ],
)
async def test_login_user(
    ac: AsyncClient, email: str, password: str, status_code: int, exist_token: bool
):
    resp: Response = await ac.post(
        url="/auth/login",
        json={"email": email, "password": password},
    )

    assert resp.status_code == status_code
    assert bool(resp.cookies.get(COOKIE_KEY)) is exist_token
