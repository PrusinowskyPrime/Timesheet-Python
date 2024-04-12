from pydantic import Field, model_validator

from app.application.modules.common.validators import validate_object_id_type
from app.application.modules.common.base_model import MongoDBModel


class Log(MongoDBModel):
    user_id: str = Field(...)
    action: str = Field(...)
    description: str = Field(...)
    data: dict = Field(...)

    @model_validator(mode="before")
    def validate_object_id(self):
        validate_object_id_type(self.user_id)

        return self