from pydantic import Field, model_validator
from typing_extensions import List

from time_sheet.src.core.modules.common.models.base_model import MongoDBModel
from time_sheet.src.core.modules.record.models.record import Record
from time_sheet.src.infrastructure.ports.api.v1.common.validators import (
    validate_object_id_type,
)


class Project(MongoDBModel):
    name: str = Field(..., min_length=5, max_length=50)
    description: str = Field(..., min_length=5, max_length=200)
    records: List[Record]
    owner_id: str

    @model_validator(mode="after")
    def validate_owner_id(self):
        validate_object_id_type(self.owner_id)
