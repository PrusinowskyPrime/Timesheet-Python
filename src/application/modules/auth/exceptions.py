from http import HTTPStatus

from src.application.modules.common.exceptions import BaseHttpException


class PasswordsAreNotTheSame(BaseHttpException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    detail = "Passwords are not the same"
