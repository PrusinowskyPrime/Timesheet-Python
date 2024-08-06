# pylint: disable=R0913
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.modules.project.mappers import (
    ProjectModelToProjectDTOMapper,
    ProjectDTOToProjectModelMapper,
    ProjectCreateDTOToProjectDTOMapper,
)
from src.application.modules.project.repositories import (
    ProjectRepository,
    IProjectRepository,
)
from src.application.modules.project.services import (
    ProjectService,
)
from src.dependencies.database import get_session


def get_project_create_dto_to_project_dto_mapper() -> (
    ProjectCreateDTOToProjectDTOMapper
):
    return ProjectCreateDTOToProjectDTOMapper()


def get_project_model_to_project_dto_mapper() -> ProjectModelToProjectDTOMapper:
    return ProjectModelToProjectDTOMapper()


def get_project_dto_to_project_model_mapper() -> ProjectDTOToProjectModelMapper:
    return ProjectDTOToProjectModelMapper()


def get_project_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
    project_dto_to_project_model_mapper: Annotated[
        ProjectDTOToProjectModelMapper, Depends(get_project_dto_to_project_model_mapper)
    ],
    project_model_to_project_dto_mapper: Annotated[
        ProjectModelToProjectDTOMapper, Depends(get_project_model_to_project_dto_mapper)
    ],
) -> IProjectRepository:
    return ProjectRepository(
        session=session,
        project_dto_to_project_model_mapper=project_dto_to_project_model_mapper,
        project_model_to_project_dto_mapper=project_model_to_project_dto_mapper,
    )


def get_project_service(
    project_repository: Annotated[IProjectRepository, Depends(get_project_repository)],
    project_create_dto_to_project_dto_mapper: Annotated[
        ProjectCreateDTOToProjectDTOMapper,
        Depends(get_project_create_dto_to_project_dto_mapper),
    ],
) -> ProjectService:
    return ProjectService(
        project_repository=project_repository,
        project_create_dto_to_project_dto_mapper=project_create_dto_to_project_dto_mapper,
    )
