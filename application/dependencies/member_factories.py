# pylint: disable=R0913,C0301
from typing import Annotated

from fastapi import Depends
from motor.core import AgnosticClientSession

from app.application.modules.member.repository import (
    MemberRepository,
)
from app.application.modules.member.mappers import (
    MemberDTOToWithUserAndProjectMapper,
)
from app.application.modules.member.services import (
    MemberService,
)
from app.application.modules.member.use_cases.send_request import (
    MemberSendRequestUseCase,
)
from app.application.modules.member.use_cases.delete import (
    MemberDeleteUseCase,
)
from app.application.modules.member.use_cases.get_all_for_project import (
    MemberGetAllForProjectUseCase,
)
from app.application.modules.member.use_cases.get_by_id import (
    MemberGetByIdUseCase,
)
from app.application.modules.member.use_cases.get_by_user_id import (
    MemberGetByUserIdUseCase,
)
from app.application.modules.member.use_cases.load_user_and_project import (
    MemberLoadUserAndProjectUseCase,
)
from app.application.modules.member.use_cases.status_change import (
    MemberStatusChangeUseCase,
)
from app.application.modules.project.mappers import (
    ProjectDTOToGetMapper,
)
from app.application.modules.project.use_cases import ProjectGetByIdUseCase, ProjectLoadOwnerUseCase
from app.application.modules.user.mappers import (
    UserDTOToGetMapper,
)
from app.application.modules.user.use_cases import UserGetByIdUseCase
from app.domain.member.repository import (
    IMemberRepository,
)
from app.application.dependencies.database import get_session
from app.application.dependencies.project_factories import (
    get_project_dto_to_get_mapper,
    get_project_get_by_id_use_case,
    get_project_load_owner_use_case,
)
from app.application.dependencies.user_factories import (
    get_user_dto_to_get_mapper,
    get_user_get_by_id_use_case,
)


def get_member_dto_to_with_user_and_project_mapper() -> (
    MemberDTOToWithUserAndProjectMapper
):
    return MemberDTOToWithUserAndProjectMapper()


def get_member_repository(
    session: Annotated[AgnosticClientSession, Depends(get_session)]
) -> IMemberRepository:
    return MemberRepository(session)


def get_member_send_request_use_case(
    repository: Annotated[IMemberRepository, Depends(get_member_repository)]
) -> MemberSendRequestUseCase:
    return MemberSendRequestUseCase(repository)


def get_member_get_by_id_use_case(
    repository: Annotated[IMemberRepository, Depends(get_member_repository)]
) -> MemberGetByIdUseCase:
    return MemberGetByIdUseCase(repository)


def get_member_get_all_for_project_use_case(
    repository: Annotated[IMemberRepository, Depends(get_member_repository)]
) -> MemberGetAllForProjectUseCase:
    return MemberGetAllForProjectUseCase(repository)


def get_member_get_by_user_id_use_case(
    repository: Annotated[IMemberRepository, Depends(get_member_repository)]
) -> MemberGetByUserIdUseCase:
    return MemberGetByUserIdUseCase(repository)


def get_member_status_change_use_case(
    repository: Annotated[IMemberRepository, Depends(get_member_repository)],
    get_by_id_use_case: Annotated[
        MemberGetByIdUseCase, Depends(get_member_get_by_id_use_case)
    ],
) -> MemberStatusChangeUseCase:
    return MemberStatusChangeUseCase(
        repository=repository, get_by_id_use_case=get_by_id_use_case
    )


def get_member_delete_use_case(
    repository: Annotated[IMemberRepository, Depends(get_member_repository)],
    get_by_id_use_case: Annotated[
        MemberGetByIdUseCase, Depends(get_member_get_by_id_use_case)
    ],
) -> MemberDeleteUseCase:
    return MemberDeleteUseCase(
        repository=repository, get_by_id_use_case=get_by_id_use_case
    )


def get_member_load_user_and_project_use_case(
    member_dto_to_with_user_and_project_mapper: Annotated[
        MemberDTOToWithUserAndProjectMapper,
        Depends(get_member_dto_to_with_user_and_project_mapper),
    ],
    user_dto_to_get_mapper: Annotated[
        UserDTOToGetMapper, Depends(get_user_dto_to_get_mapper)
    ],
    project_dto_to_get_mapper: Annotated[
        ProjectDTOToGetMapper, Depends(get_project_dto_to_get_mapper)
    ],
    user_get_by_id_use_case: Annotated[
        UserGetByIdUseCase, Depends(get_user_get_by_id_use_case)
    ],
    project_get_by_id_use_case: Annotated[
        ProjectGetByIdUseCase, Depends(get_project_get_by_id_use_case)
    ],
    project_load_owner_use_case: Annotated[
        ProjectLoadOwnerUseCase, Depends(get_project_load_owner_use_case)
    ],
) -> MemberLoadUserAndProjectUseCase:
    return MemberLoadUserAndProjectUseCase(
        member_dto_to_with_user_and_project_mapper=member_dto_to_with_user_and_project_mapper,
        user_get_by_id_use_case=user_get_by_id_use_case,
        user_dto_to_get_mapper=user_dto_to_get_mapper,
        project_get_by_id_use_case=project_get_by_id_use_case,
        project_dto_to_get_mapper=project_dto_to_get_mapper,
        project_load_owner_use_case=project_load_owner_use_case,
    )


def get_member_service(
    member_send_request_use_case: Annotated[
        MemberSendRequestUseCase, Depends(get_member_send_request_use_case)
    ],
    member_status_change_use_case: Annotated[
        MemberStatusChangeUseCase, Depends(get_member_status_change_use_case)
    ],
    member_delete_use_case: Annotated[
        MemberDeleteUseCase, Depends(get_member_delete_use_case)
    ],
    member_get_by_id_use_case: Annotated[
        MemberGetByIdUseCase, Depends(get_member_get_by_id_use_case)
    ],
    member_get_all_for_project_use_case: Annotated[
        MemberGetAllForProjectUseCase, Depends(get_member_get_all_for_project_use_case)
    ],
    member_get_by_user_id_use_case: Annotated[
        MemberGetByUserIdUseCase, Depends(get_member_get_by_user_id_use_case)
    ],
    load_user_and_project_use_case: Annotated[  # pylint: disable=C0301
        MemberLoadUserAndProjectUseCase,
        Depends(get_member_load_user_and_project_use_case),
    ],
) -> MemberService:
    return MemberService(
        member_send_request_use_case=member_send_request_use_case,
        member_status_change_use_case=member_status_change_use_case,
        delete_use_case=member_delete_use_case,
        get_all_for_project_use_case=member_get_all_for_project_use_case,
        get_by_id_use_case=member_get_by_id_use_case,
        get_by_user_id=member_get_by_user_id_use_case,
        load_user_and_project_use_case=load_user_and_project_use_case,
    )
