from typing import Optional

from pydantic import BaseModel, Field

from app.application.modules.common.object_id import ObjectId


class MongoDBModel(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)

    class ConfigDict:
        json_encoders = {
            ObjectId: lambda value: str(value),  # pylint: disable=W0108
        }
