from pydantic import Field, EmailStr

from app.application.modules.common.base_model import MongoDBModel


class User(MongoDBModel):
    fullname: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=8)
