"""Различные HTTP-ошибки"""
from fastapi import HTTPException, status


class UserUnauthorizedException(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User is unauthorized'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectJWTtokenException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'JWT token is incorrect'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class JWTtokenExpiredException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'JWT token is expired'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserIsNotPresentException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserIsAllredyRegistered(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User is allready registered"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectEmailOrPasswordException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Incorrect e-mail or password"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NoFreeRoomsException(HTTPException):
    status_code = status.HTTP_409_CONFLICT,
    detail = 'No free rooms'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
