# pylint: disable=R0801, R0913
from typing import List
from time_sheet.src.application.modules.record.dto.record import (
    RecordCreateDTO,
    RecordUpdateDTO,
)
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
from time_sheet.src.core.modules.record.dto.record import RecordDTO


class RecordService:
    def __init__(
        self,
        create_use_case: RecordCreateUseCase,
        delete_use_case: RecordDeleteUseCase,
        update_use_case: RecordUpdateUseCase,
        get_all_use_case: RecordGetAllUseCase,
        get_by_id_use_case: RecordGetByIdUseCase,
        get_by_owner_id_use_case: RecordGetByOwnerIdUseCase,
    ):
        self._create_use_case = create_use_case
        self._delete_use_case = delete_use_case
        self._update_use_case = update_use_case
        self._get_all_use_case = get_all_use_case
        self._get_by_id_use_case = get_by_id_use_case
        self._get_by_owner_id_use_case = get_by_owner_id_use_case

    async def create(self, request_dto: RecordCreateDTO) -> RecordDTO:
        return await self._create_use_case.execute(request_dto)

    async def update(self, record_id: str, request_dto: RecordUpdateDTO) -> RecordDTO:
        return await self._update_use_case.execute(
            request_dto=request_dto, record_id=record_id
        )

    async def delete(self, record_id: str) -> None:
        return await self._delete_use_case.execute(record_id)

    async def get_all(self) -> List[RecordDTO]:
        return await self._get_all_use_case.execute()

    async def get_by_id(self, record_id: str) -> RecordDTO:
        return await self._get_by_id_use_case.execute(record_id)

    async def get_by_owner_id(self, owner_id: str) -> List[RecordDTO]:
        return await self._get_by_owner_id_use_case.execute(owner_id)
