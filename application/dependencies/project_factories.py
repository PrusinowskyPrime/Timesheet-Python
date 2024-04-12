# pylint: disable=R0913
from typing import Annotated

from fastapi import Depends
from motor.core import AgnosticClientSession

from app.application.modules.project.repositories import (
    ProjectRepository, IProjectRepository,
)
from app.application.modules.project.mappers import (
    ProjectDTOToGetMapper, ProjectDTOToWithOwnerMapper,
)
from app.application.modules.project.services import (
    ProjectService,
)
from app.application.modules.project.use_cases import ProjectCreateUseCase, ProjectDeleteUseCase, ProjectGetAllUseCase, \
    ProjectGetByIdUseCase, ProjectGetByOwnerIdUseCase, ProjectLoadOwnerUseCase, ProjectUpdateUseCase
from app.application.modules.user.mappers import (
    UserDTOToGetMapper,
)
from app.application.modules.user.use_cases import UserGetByIdUseCase
from app.application.dependencies.database import get_session
from app.application.dependencies.user_factories import (
    get_user_dto_to_get_mapper,
    get_user_get_by_id_use_case,
)


def get_project_dto_to_with_owner_mapper() -> ProjectDTOToWithOwnerMapper:
    return ProjectDTOToWithOwnerMapper()


def get_project_dto_to_get_mapper() -> ProjectDTOToGetMapper:
    return ProjectDTOToGetMapper()


def get_project_repository(
    session: Annotated[AgnosticClientSession, Depends(get_session)]
) -> IProjectRepository:
    return ProjectRepository(session)


def get_project_create_use_case(
    repository: Annotated[IProjectRepository, Depends(get_project_repository)]
) -> ProjectCreateUseCase:
    return ProjectCreateUseCase(repository)


def get_project_get_by_id_use_case(
    repository: Annotated[IProjectRepository, Depends(get_project_repository)]
) -> ProjectGetByIdUseCase:
    return ProjectGetByIdUseCase(repository)


def get_project_get_all_use_case(
    repository: Annotated[IProjectRepository, Depends(get_project_repository)]
) -> ProjectGetAllUseCase:
    return ProjectGetAllUseCase(repository)


def get_project_get_by_owner_id_use_case(
    repository: Annotated[IProjectRepository, Depends(get_project_repository)]
) -> ProjectGetByOwnerIdUseCase:
    return ProjectGetByOwnerIdUseCase(repository)


def get_project_update_use_case(
    repository: Annotated[IProjectRepository, Depends(get_project_repository)],
    get_by_id_use_case: Annotated[
        ProjectGetByIdUseCase, Depends(get_project_get_by_id_use_case)
    ],
) -> ProjectUpdateUseCase:
    return ProjectUpdateUseCase(
        repository=repository, get_by_id_use_case=get_by_id_use_case
    )


def get_project_delete_use_case(
    repository: Annotated[IProjectRepository, Depends(get_project_repository)],
    get_by_id_use_case: Annotated[
        ProjectGetByIdUseCase, Depends(get_project_get_by_id_use_case)
    ],
) -> ProjectDeleteUseCase:
    return ProjectDeleteUseCase(
        repository=repository, get_by_id_use_case=get_by_id_use_case
    )


def get_project_load_owner_use_case(
    project_dto_to_with_owner_mapper: Annotated[
        ProjectDTOToWithOwnerMapper, Depends(get_project_dto_to_with_owner_mapper)
    ],
    user_dto_to_get_mapper: Annotated[
        UserDTOToGetMapper, Depends(get_user_dto_to_get_mapper)
    ],
    user_get_by_id_use_case: Annotated[
        UserGetByIdUseCase, Depends(get_user_get_by_id_use_case)
    ],
) -> ProjectLoadOwnerUseCase:
    return ProjectLoadOwnerUseCase(
        project_dto_to_with_owner_mapper=project_dto_to_with_owner_mapper,
        user_get_by_id_use_case=user_get_by_id_use_case,
        user_dto_to_get_mapper=user_dto_to_get_mapper,
    )


def get_project_service(
    project_create_use_case: Annotated[
        ProjectCreateUseCase, Depends(get_project_create_use_case)
    ],
    project_update_use_case: Annotated[
        ProjectUpdateUseCase, Depends(get_project_update_use_case)
    ],
    project_delete_use_case: Annotated[
        ProjectDeleteUseCase, Depends(get_project_delete_use_case)
    ],
    project_get_by_id_use_case: Annotated[
        ProjectGetByIdUseCase, Depends(get_project_get_by_id_use_case)
    ],
    project_get_all_use_case: Annotated[
        ProjectGetAllUseCase, Depends(get_project_get_all_use_case)
    ],
    project_get_by_owner_id_use_case: Annotated[
        ProjectGetByOwnerIdUseCase, Depends(get_project_get_by_owner_id_use_case)
    ],
    load_owner_use_case: Annotated[  # pylint: disable=C0301
        ProjectLoadOwnerUseCase, Depends(get_project_load_owner_use_case)
    ],
) -> ProjectService:
    return ProjectService(
        create_use_case=project_create_use_case,
        update_use_case=project_update_use_case,
        delete_use_case=project_delete_use_case,
        get_all_use_case=project_get_all_use_case,
        get_by_id_use_case=project_get_by_id_use_case,
        get_by_owner_id=project_get_by_owner_id_use_case,
        load_owner_use_case=load_owner_use_case,
    )
