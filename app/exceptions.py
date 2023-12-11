"""Различные HTTP-ошибки"""
from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserUnauthorizedException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User is unauthorized"


class IncorrectJWTtokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "JWT token is incorrect"


class JWTtokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "JWT token is expired"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ""


class UserIsAllredyRegistered(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User is allready registered"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect e-mail or password"


class NoFreeRoomsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "No free rooms"


class IncorrectDateValuesException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect date values: Departure date >= Arrival date"


class BookingMoreThirtyDaysException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Arrival date - Departure date > 30 days"
