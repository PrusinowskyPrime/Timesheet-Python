# pylint: disable=R0913
from typing import Annotated

from fastapi import Depends
from motor.core import AgnosticClientSession

from app.application.dependencies.database import get_session
from app.application.modules.project.repositories import (
    ProjectRepository, IProjectRepository,
)
from app.application.modules.project.services import (
    ProjectService,
)


def get_project_repository(
        session: Annotated[AgnosticClientSession, Depends(get_session)]
) -> IProjectRepository:
    return ProjectRepository(session)


def get_project_service(
        repository: Annotated[IProjectRepository, Depends(get_project_repository)],
) -> ProjectService:
    return ProjectService(
        repository=repository
    )
