from sqlalchemy import Integer
from sqlalchemy.orm import MappedColumn, mapped_column
from sqlalchemy.orm import declarative_base


# pylint: disable=not-callable
class Base:
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, index=True)

BaseModel = declarative_base(cls=Base)
