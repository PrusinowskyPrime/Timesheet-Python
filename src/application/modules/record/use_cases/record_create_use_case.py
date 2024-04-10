from time_sheet.src.application.modules.record.dto.record import RecordCreateDTO
from time_sheet.src.core.modules.record.dto.record import RecordDTO
from time_sheet.src.core.modules.record.repositories.record_repository import (
    IRecordRepository,
)


class RecordCreateUseCase:
    def __init__(self, repository: IRecordRepository):
        self._repository = repository

    async def execute(self, request_dto: RecordCreateDTO) -> RecordDTO:
        record_dto = RecordDTO(**request_dto.model_dump(), _id=None)
        return await self._repository.save(record_dto)
