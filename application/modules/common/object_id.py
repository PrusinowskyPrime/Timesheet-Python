from bson import ObjectId as ObjectIdBson
from bson.errors import InvalidId


class ObjectId(ObjectIdBson):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        try:
            return cls(v)
        except InvalidId as exception:
            raise ValueError("Not a valid ObjectId") from exception
