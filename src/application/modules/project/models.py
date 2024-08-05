from sqlalchemy import String, Text
from sqlalchemy.orm import MappedColumn, mapped_column

from src.application.modules.common.base_model import BaseModel


class ProjectModel(BaseModel):
    __tablename__ = "projects"

    name: MappedColumn[str] = mapped_column(String(255))
    description: MappedColumn[str] = mapped_column(Text(2000))
    # Dodać ownera
    # Dodać constraint (user, nazwa)
