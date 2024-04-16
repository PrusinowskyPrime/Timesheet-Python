from pydantic import Field, model_validator

from app.application.modules.common.base_model import MongoDBModel
from app.application.modules.common.validators import validate_object_id_type


class TimeLog(MongoDBModel):
    start_time: str = Field(...)
    end_time: str = Field(...)
    details: str = Field(...)
    owner_id: str = Field(...)

    @model_validator(mode="before")
    def validate_object_id(self):
        validate_object_id_type(self.owner_id)

        return self
