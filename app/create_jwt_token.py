from jose import jwt
from datetime import datetime, timedelta


def create_jwt_token(data: dict[str, str]) -> str:
    to_encode: dict[str, str] = data.copy()
    to_encode.update(
        {
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
    )
    jwt_token: str = jwt.encode(
        claims=to_encode, key="bhfoierjf[oierfoer]", algorithm="HS256"
    )
    return jwt_token


if __name__ == "__main__":
    print(create_jwt_token({"name": "Yury"}))
