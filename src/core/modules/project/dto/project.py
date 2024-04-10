from typing import Optional

from pydantic import BaseModel, Field
from typing_extensions import List

from time_sheet.src.core.modules.record.dto.record import RecordDTO


class ProjectDTO(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    description: str
    records: List[RecordDTO]
    owner_id: str
