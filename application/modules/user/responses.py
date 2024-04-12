from pydantic import BaseModel


class UserBaseResponse(BaseModel):
    id: str
    fullname: str
    email: str
