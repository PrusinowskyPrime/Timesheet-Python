from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.modules.project.dtos import ProjectDTO
from src.application.modules.project.mappers import (
    ProjectDTOToProjectModelMapper,
    ProjectModelToProjectDTOMapper,
)
from src.application.modules.project.models import ProjectModel


class IProjectRepository(ABC):
    @abstractmethod
    async def save(self, project: ProjectDTO) -> ProjectDTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[ProjectDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, project_id: int) -> ProjectDTO | None:
        pass

    @abstractmethod
    async def delete(self, project: ProjectDTO) -> None:
        pass

    @abstractmethod
    async def update(self, project: ProjectDTO) -> ProjectDTO:
        pass


class ProjectRepository(IProjectRepository):
    def __init__(
        self,
        session: AsyncSession,
        project_dto_to_project_model_mapper: ProjectDTOToProjectModelMapper,
        project_model_to_project_dto_mapper: ProjectModelToProjectDTOMapper,
    ):
        self._session = session
        self._project_dto_to_project_model_mapper = project_dto_to_project_model_mapper
        self._project_model_to_project_dto_mapper = project_model_to_project_dto_mapper

    async def save(self, project: ProjectDTO) -> ProjectDTO:
        model = self._project_dto_to_project_model_mapper.map(project)

        self._session.add(model)
        await self._session.commit()

        return self._project_model_to_project_dto_mapper.map(model)  # type: ignore

    async def update(self, project: ProjectDTO) -> ProjectDTO:
        model = self._project_dto_to_project_model_mapper.map(project)

        await self._session.merge(model)
        await self._session.commit()

        return self._project_model_to_project_dto_mapper.map(model)  # type: ignore

    async def delete(self, project: ProjectDTO) -> None:
        query = delete(ProjectModel).where(ProjectModel.id == project.id)

        await self._session.execute(query)
        await self._session.commit()

    async def get_all(self) -> List[ProjectDTO]:
        result = await self._session.execute(select(ProjectModel))
        data = []

        for project in result.scalars().all():
            data.append(self._project_model_to_project_dto_mapper.map(project))

        return data  # type: ignore

    async def get_by_id(self, project_id: int) -> ProjectDTO | None:
        result = await self._session.execute(
            select(ProjectModel).where(ProjectModel.id == project_id)
        )

        return self._project_model_to_project_dto_mapper.map(result.scalars().first())
