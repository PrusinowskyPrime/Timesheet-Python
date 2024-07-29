from pydantic import BaseModel, EmailStr


class UserBaseDTO(BaseModel):
    fullname: str


class UserCreateDTO(UserBaseDTO):
    email: EmailStr
    password: str


class UserUpdateDTO(UserBaseDTO):
    pass


class UserGetDTO(UserBaseDTO):
    id: int
    email: EmailStr


class UserDTO(BaseModel):
    id: int | None
    fullname: str
    email: str
    password: str
