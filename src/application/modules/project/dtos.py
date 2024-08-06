from typing import Optional

from pydantic import BaseModel


class ProjectBaseDTO(BaseModel):
    name: str
    description: str


class ProjectDTO(ProjectBaseDTO):
    id: Optional[int]


class ProjectCreateDTO(ProjectBaseDTO):
    pass


class ProjectUpdateDTO(ProjectBaseDTO):
    pass
