from datetime import datetime
from pydantic import BaseModel


class RecordBaseDTO(BaseModel):
    name: str
    start: datetime
    end: datetime
    additional_information: str


class RecordCreateDTO(RecordBaseDTO):
    owner_id: str


class RecordUpdateDTO(RecordBaseDTO):
    pass
