from src.application.modules.project.dtos import ProjectDTO, ProjectCreateDTO
from src.application.modules.project.models import ProjectModel


class ProjectDTOToProjectModelMapper:
    def map(self, dto: ProjectDTO) -> ProjectModel:
        return ProjectModel(id=dto.id, name=dto.name, description=dto.description)


class ProjectModelToProjectDTOMapper:
    def map(self, project: ProjectModel | None) -> ProjectDTO | None:
        if project is None:
            return None

        return ProjectDTO(
            id=project.id, name=project.name, description=project.description
        )


class ProjectCreateDTOToProjectDTOMapper:
    def map(self, dto: ProjectCreateDTO) -> ProjectDTO:
        return ProjectDTO(**dto.model_dump())
