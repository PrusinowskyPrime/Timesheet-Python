from datetime import datetime

from pydantic import Field, model_validator

from time_sheet.src.core.modules.common.models.base_model import MongoDBModel
from time_sheet.src.infrastructure.ports.api.v1.common.validators import (
    validate_object_id_type,
    validate_date_range,
    validate_date_format_from_date_time,
)


class Record(MongoDBModel):
    name: str = Field(..., min_length=5, max_length=50)
    start: datetime
    end: datetime
    additional_information: str = Field(..., min_length=5, max_length=100)
    owner_id: str

    @model_validator(mode="after")
    def validate_record_fields(self):
        validate_object_id_type(self.owner_id)
        validate_date_format_from_date_time(self.start)
        validate_date_format_from_date_time(self.end)
        validate_date_range(self.start, self.end)
