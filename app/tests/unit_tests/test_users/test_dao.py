import pytest

from app.users.dao import UsersDAO
from app.users.models import Users


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email,is_exist",
    [
        ("test@test.com", True),
        ("yury@example.com", True),
        ("...", False),
    ],
)
async def test_find_user_by_email(email, is_exist):
    user: Users | None = await UsersDAO.find_one_or_none(email=email)
    if is_exist:
        assert user
        assert user.email == email
    else:
        assert not user
