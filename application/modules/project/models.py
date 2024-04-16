from pydantic import Field, model_validator
from typing_extensions import List

from app.application.modules.common.base_model import MongoDBModel
from app.application.modules.common.validators import (
    validate_object_id_type,
)
from app.application.modules.time_log.models import TimeLog


class Project(MongoDBModel):
    name: str = Field(..., min_length=5, max_length=50)
    description: str = Field(..., min_length=5, max_length=200)
    time_logs: List[TimeLog] = Field(...)
    owner_id: str = Field(...)

    @model_validator(mode="after")
    def validate_owner_id(self):
        validate_object_id_type(self.owner_id)
