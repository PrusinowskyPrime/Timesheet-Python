from typing import List

from time_sheet.src.core.modules.record.dto.record import RecordDTO
from time_sheet.src.core.modules.record.repositories.record_repository import (
    IRecordRepository,
)


class RecordGetByOwnerIdUseCase:
    def __init__(self, repository: IRecordRepository):
        self._repository = repository

    async def execute(self, owner_id: str) -> List[RecordDTO]:
        return await self._repository.get_by_owner_id(owner_id)
