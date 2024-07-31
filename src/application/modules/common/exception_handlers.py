# pylint: disable=W0613, R0911
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.application.modules.auth.exceptions import PasswordsAreNotTheSame
from src.application.modules.common.exceptions import (
    BaseHttpException,
    ObjectDoesNotExist,
    InvalidDateFormat,
    InvalidDateRange,
    InvalidCredentials,
    PasswordDoesNotMatch,
    ObjectAlreadyExists,
)


def http_exception_handler(request: Request, exception: BaseHttpException):
    if isinstance(exception, ObjectDoesNotExist):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exception.detail},
        )

    if isinstance(exception, InvalidDateFormat):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exception.detail},
        )

    if isinstance(exception, InvalidDateRange):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exception.detail},
        )

    if isinstance(exception, InvalidCredentials):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exception.detail},
        )

    if isinstance(exception, PasswordDoesNotMatch):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exception.detail},
        )

    if isinstance(exception, ObjectAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exception.detail},
        )

    if isinstance(exception, PasswordsAreNotTheSame):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exception.detail},
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
