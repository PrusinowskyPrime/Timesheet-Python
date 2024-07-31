from http import HTTPStatus


class BaseHttpException(Exception):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    detail = "Internal server error"


class ObjectDoesNotExist(BaseHttpException):
    status_code = HTTPStatus.NOT_FOUND
    detail = "Object does not exist"


class ObjectAlreadyExists(BaseHttpException):
    status_code = HTTPStatus.CONFLICT
    detail = "Object already exists"


class InvalidDateFormat(BaseHttpException):
    status_code = HTTPStatus.BAD_REQUEST
    detail = "Invalid date format. It must be in the format %Y-%m-%dT%H:%M:%S.%fZ"


class InvalidDateRange(BaseHttpException):
    status_code = HTTPStatus.BAD_REQUEST
    detail = "Invalid date range"


class InvalidCredentials(BaseHttpException):
    status_code = HTTPStatus.NOT_FOUND
    detail = "Invalid login data"


class PasswordDoesNotMatch(BaseHttpException):
    status_code = HTTPStatus.CONFLICT
    detail = "Passwords does not match"
