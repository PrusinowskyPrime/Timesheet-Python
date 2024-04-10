from datetime import datetime

from pydantic import BaseModel


class RecordBaseResponse(BaseModel):
    id: str
    name: str
    start: datetime
    end: datetime
    additional_information: str
    owner_id: str
