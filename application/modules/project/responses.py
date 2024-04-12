from pydantic import BaseModel

from app.application.modules.user.responses import UserBaseResponse


class ProjectBaseResponse(BaseModel):
    id: str
    name: str
    description: str
    owner: UserBaseResponse
