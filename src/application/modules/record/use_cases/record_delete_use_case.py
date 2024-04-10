from time_sheet.src.application.modules.record.use_cases.record_get_by_id_use_case import (
    RecordGetByIdUseCase,
)
from time_sheet.src.core.modules.record.repositories.record_repository import (
    IRecordRepository,
)


class RecordDeleteUseCase:
    def __init__(
        self, repository: IRecordRepository, get_by_id_use_case: RecordGetByIdUseCase
    ):
        self._repository = repository
        self._get_by_id_use_case = get_by_id_use_case

    async def execute(self, record_id: str) -> None:
        await self._get_by_id_use_case.execute(record_id)

        return await self._repository.delete(record_id=record_id)
