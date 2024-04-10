# pylint: disable=R0801
from abc import ABC, abstractmethod
from typing import List
from time_sheet.src.core.modules.record.dto.record import RecordDTO


class IRecordRepository(ABC):
    @abstractmethod
    async def save(self, record: RecordDTO) -> RecordDTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[RecordDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, record_id: str) -> RecordDTO | None:
        pass

    @abstractmethod
    async def get_by_owner_id(self, owner_id: str) -> List[RecordDTO]:
        pass

    @abstractmethod
    async def delete(self, record_id: str) -> None:
        pass

    @abstractmethod
    async def update(self, record: RecordDTO) -> RecordDTO:
        pass
