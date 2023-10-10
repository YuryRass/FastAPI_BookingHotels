"""Различные HTTP-ошибки"""
from fastapi import HTTPException, status


UserUnauthorizedException: HTTPException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='User is unauthorized',
)

IncorrectJWTtokenException: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='JWT token is incorrect'
)

JWTtokenExpiredException: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='JWT token is expired',
)

UserIsNotPresentException: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
)

UserIsAllredyRegistered: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is allready registered",
)

IncorrectEmailOrPasswordException: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect e-mail or password",
)
