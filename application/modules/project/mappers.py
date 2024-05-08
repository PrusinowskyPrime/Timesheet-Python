from app.application.modules.project.dtos import (
    ProjectGetDTO,
    ProjectWithOwnerDTO,
    ProjectDTO,
)


class ProjectDTOToGetMapper:
    def map(self, dto: ProjectWithOwnerDTO) -> ProjectGetDTO:
        return ProjectGetDTO(**dto.model_dump())


class ProjectDTOToWithOwnerMapper:
    def map(self, dto: ProjectDTO) -> ProjectWithOwnerDTO:
        return ProjectWithOwnerDTO(**dto.model_dump())
