from sqlalchemy import String
from sqlalchemy.orm import MappedColumn, mapped_column

from src.application.modules.common.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    fullname: MappedColumn[str] = mapped_column(String(255))
    email: MappedColumn[str] = mapped_column(String(255), unique=True)
    password: MappedColumn[str] = mapped_column(String(255))
