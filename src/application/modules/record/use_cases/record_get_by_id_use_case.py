from time_sheet.src.core.modules.common.exceptions.domain import ObjectDoesNotExist

from time_sheet.src.core.modules.record.dto.record import RecordDTO
from time_sheet.src.core.modules.record.repositories.record_repository import (
    IRecordRepository,
)


class RecordGetByIdUseCase:
    def __init__(self, repository: IRecordRepository):
        self._repository = repository

    async def execute(self, record_id: str) -> RecordDTO:
        record = await self._repository.get_by_id(record_id=record_id)

        if record is None:
            raise ObjectDoesNotExist

        return record
