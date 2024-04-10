# pylint: disable=R0801
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RecordDTO(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    start: datetime
    end: datetime
    additional_information: str
    owner_id: str
