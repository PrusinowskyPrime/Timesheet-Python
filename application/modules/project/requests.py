from pydantic import BaseModel, Field


class ProjectBaseRequest(BaseModel):
    name: str = Field(..., min_length=5, max_length=50)
    description: str = Field(..., min_length=5, max_length=200)


class ProjectCreateRequest(ProjectBaseRequest):
    pass


class ProjectUpdateRequest(ProjectBaseRequest):
    pass
