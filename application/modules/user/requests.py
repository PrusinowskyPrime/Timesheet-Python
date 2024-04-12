from typing import Dict, Any

from pydantic import BaseModel, EmailStr, Field, model_validator

from app.application.modules.common.value import (
    PasswordsDoNotMatch,
)


class UserBaseRequest(BaseModel):
    fullname: str = Field(..., min_length=5, max_length=50)


class UserCreateRequest(UserBaseRequest):
    email: EmailStr = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=8, max_length=20)
    password_confirmation: str = Field(..., min_length=8, max_length=20)

    @model_validator(mode="before")
    @classmethod
    def validate_passwords(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if data["password"] != data["password_confirmation"]:
            raise PasswordsDoNotMatch()

        return data


class UserUpdateRequest(UserBaseRequest):
    pass
