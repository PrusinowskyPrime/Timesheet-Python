# pylint: disable=R0913
from typing import Annotated

from fastapi import Depends
from motor.core import AgnosticClientSession

from app.application.modules.record.record_repository import (
    RecordRepository,
)
from app.application.modules.record.services import RecordService
from app.application.modules.record.use_cases.create import (
    RecordCreateUseCase,
)
from app.application.modules.record.use_cases.delete import (
    RecordDeleteUseCase,
)
from app.application.modules.record.use_cases.get_all import (
    RecordGetAllUseCase,
)
from app.application.modules.record.use_cases.get_by_id import (
    RecordGetByIdUseCase,
)
from app.application.modules.record.use_cases.get_by_owner_id import (
    RecordGetByOwnerIdUseCase,
)
from app.application.modules.record.use_cases.update import (
    RecordUpdateUseCase,
)
from app.application.modules.log import (
    IRecordRepository,
)
from app.application.dependencies.database import get_session


def get_record_repository(
    session: Annotated[AgnosticClientSession, Depends(get_session)]
) -> IRecordRepository:
    return RecordRepository(session)


def get_record_create_use_case(
    repository: Annotated[IRecordRepository, Depends(get_record_repository)]
) -> RecordCreateUseCase:
    return RecordCreateUseCase(repository)


def get_record_get_by_id_use_case(
    repository: Annotated[IRecordRepository, Depends(get_record_repository)]
) -> RecordGetByIdUseCase:
    return RecordGetByIdUseCase(repository)


def get_record_get_all_use_case(
    repository: Annotated[IRecordRepository, Depends(get_record_repository)]
) -> RecordGetAllUseCase:
    return RecordGetAllUseCase(repository)


def get_record_get_by_owner_id_use_case(
    repository: Annotated[IRecordRepository, Depends(get_record_repository)]
) -> RecordGetByOwnerIdUseCase:
    return RecordGetByOwnerIdUseCase(repository)


def get_record_update_use_case(
    repository: Annotated[IRecordRepository, Depends(get_record_repository)],
    get_by_id_use_case: Annotated[
        RecordGetByIdUseCase, Depends(get_record_get_by_id_use_case)
    ],
) -> RecordUpdateUseCase:
    return RecordUpdateUseCase(
        repository=repository, get_by_id_use_case=get_by_id_use_case
    )


def get_record_delete_use_case(
    repository: Annotated[IRecordRepository, Depends(get_record_repository)],
    get_by_id_use_case: Annotated[
        RecordGetByIdUseCase, Depends(get_record_get_by_id_use_case)
    ],
) -> RecordDeleteUseCase:
    return RecordDeleteUseCase(
        repository=repository, get_by_id_use_case=get_by_id_use_case
    )


def get_record_service(
    record_create_use_case: Annotated[
        RecordCreateUseCase, Depends(get_record_create_use_case)
    ],
    record_update_use_case: Annotated[
        RecordUpdateUseCase, Depends(get_record_update_use_case)
    ],
    record_delete_use_case: Annotated[
        RecordDeleteUseCase, Depends(get_record_delete_use_case)
    ],
    record_get_by_id_use_case: Annotated[
        RecordGetByIdUseCase, Depends(get_record_get_by_id_use_case)
    ],
    record_get_all_use_case: Annotated[
        RecordGetAllUseCase, Depends(get_record_get_all_use_case)
    ],
    record_get_by_owner_id_use_case: Annotated[
        RecordGetByOwnerIdUseCase, Depends(get_record_get_by_owner_id_use_case)
    ],
) -> RecordService:
    return RecordService(
        create_use_case=record_create_use_case,
        update_use_case=record_update_use_case,
        delete_use_case=record_delete_use_case,
        get_all_use_case=record_get_all_use_case,
        get_by_id_use_case=record_get_by_id_use_case,
        get_by_owner_id_use_case=record_get_by_owner_id_use_case,
    )
