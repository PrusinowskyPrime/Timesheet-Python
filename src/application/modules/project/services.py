# pylint: disable=R0801, R0913
from typing import List

from src.application.modules.common.exceptions import ObjectDoesNotExist
from src.application.modules.project.dtos import (
    ProjectCreateDTO,
    ProjectUpdateDTO,
    ProjectDTO,
)
from src.application.modules.project.mappers import ProjectCreateDTOToProjectDTOMapper
from src.application.modules.project.repositories import IProjectRepository


class ProjectService:
    def __init__(
        self,
        project_repository: IProjectRepository,
        project_create_dto_to_project_dto_mapper: ProjectCreateDTOToProjectDTOMapper,
    ):
        self._project_repository = project_repository
        self._project_create_dto_to_project_dto_mapper = (
            project_create_dto_to_project_dto_mapper
        )

    async def create(self, request_dto: ProjectCreateDTO) -> ProjectDTO:
        project_dto = self._project_create_dto_to_project_dto_mapper.map(request_dto)

        return await self._project_repository.save(project_dto)

    async def update(
        self, project_id: int, request_dto: ProjectUpdateDTO
    ) -> ProjectDTO:
        dto = await self.get_by_id(project_id)
        dto.name = request_dto.name
        dto.description = request_dto.description

        return await self._project_repository.update(dto)

    async def delete(self, project_id: int) -> None:
        project = await self.get_by_id(project_id)

        return await self._project_repository.delete(project)

    async def get_all(self) -> List[ProjectDTO]:
        return await self._project_repository.get_all()

    async def get_by_id(self, project_id: int) -> ProjectDTO:
        project = await self._project_repository.get_by_id(project_id)

        if project is None:
            raise ObjectDoesNotExist()

        return project
