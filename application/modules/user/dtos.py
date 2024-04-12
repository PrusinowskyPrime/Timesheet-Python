from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBaseDTO(BaseModel):
    fullname: str


class UserCreateDTO(UserBaseDTO):
    email: EmailStr
    password: str


class UserUpdateDTO(UserBaseDTO):
    pass


class UserGetDTO(UserBaseDTO):
    id: str
    email: EmailStr


class UserDTO(BaseModel):
    id: Optional[str] = Field(alias="_id")
    fullname: str
    email: str
    password: str
