from time_sheet.src.application.modules.record.dto.record import (
    RecordUpdateDTO,
)
from time_sheet.src.application.modules.record.use_cases.record_get_by_id_use_case import (
    RecordGetByIdUseCase,
)
from time_sheet.src.core.modules.record.dto.record import RecordDTO
from time_sheet.src.core.modules.record.repositories.record_repository import (
    IRecordRepository,
)


class RecordUpdateUseCase:
    def __init__(
        self, repository: IRecordRepository, get_by_id_use_case: RecordGetByIdUseCase
    ):
        self._repository = repository
        self._get_by_id_use_case = get_by_id_use_case

    async def execute(self, request_dto: RecordUpdateDTO, record_id: str) -> RecordDTO:
        record_dto = await self._get_by_id_use_case.execute(record_id)
        for key, value in request_dto.model_dump().items():
            setattr(record_dto, key, value)

        return await self._repository.update(record_dto)
