# pylint: disable=R0801
from datetime import datetime
from typing import Optional, Self

from pydantic import BaseModel, model_validator, Field

from src.application.modules.common.exceptions import PasswordDoesNotMatch


class AuthenticatedUserDTO(BaseModel):
    id: Optional[int] = None
    sub: str


class CurrentUserDTO(BaseModel):
    id: int
    email: str

    class ConfigDict:
        frozen = True


class ChangePasswordDTO(BaseModel):
    current_password: str = Field(min_length=8, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    password_confirmation: str = Field(min_length=8, max_length=20)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        password1 = self.password
        password2 = self.password_confirmation

        if password1 is not None and password2 is not None and password1 != password2:
            raise PasswordDoesNotMatch()

        return self

    class ConfigDict:
        frozen = True


class SuccessAuthenticationDTO(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expired_at: datetime

    class ConfigDict:
        frozen = True
