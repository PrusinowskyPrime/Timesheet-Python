from typing import Optional, List

from pydantic import BaseModel, Field

from app.application.modules.log.dtos import LogDTO
from app.application.modules.user.dtos import UserGetDTO


class ProjectBaseDTO(BaseModel):
    name: str
    description: str


class ProjectCreateDTO(ProjectBaseDTO):
    owner_id: str


class ProjectUpdateDTO(ProjectBaseDTO):
    pass


class ProjectGetDTO(ProjectBaseDTO):
    id: str
    owner: UserGetDTO | None = None


class ProjectWithOwnerDTO(ProjectBaseDTO):
    id: str
    owner: UserGetDTO | None = None


class ProjectDTO(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    description: str
    records: List[LogDTO]
    owner_id: str
