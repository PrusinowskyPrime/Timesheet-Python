# pylint: disable=R0913
from typing import Annotated

from fastapi import Depends
from motor.core import AgnosticClientSession

from time_sheet.src.adapters.modules.record.repositories.record_repository import (
    RecordRepository,
)
from time_sheet.src.application.modules.record.services.record_service import RecordService
from time_sheet.src.application.modules.record.use_cases.record_create_use_case import (
    RecordCreateUseCase,
)
from time_sheet.src.application.modules.record.use_cases.record_delete_use_case import (
    RecordDeleteUseCase,
)
from time_sheet.src.application.modules.record.use_cases.record_get_all_use_case import (
    RecordGetAllUseCase,
)
from time_sheet.src.application.modules.record.use_cases.record_get_by_id_use_case import (
    RecordGetByIdUseCase,
)
from time_sheet.src.application.modules.record.use_cases.record_get_by_owner_id import (
    RecordGetByOwnerIdUseCase,
)
from time_sheet.src.application.modules.record.use_cases.record_update_use_case import (
    RecordUpdateUseCase,
)
from time_sheet.src.core.modules.record.repositories.record_repository import (
    IRecordRepository,
)
from time_sheet.src.infrastructure.dependencies.database.setup import get_session


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
