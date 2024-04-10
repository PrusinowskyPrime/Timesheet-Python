from typing import List
from bson import ObjectId
from motor.core import AgnosticCollection, AgnosticClientSession
from time_sheet.src.core.modules.record.dto.record import RecordDTO
from time_sheet.src.core.modules.record.models.record import Record
from time_sheet.src.core.modules.record.repositories.record_repository import (
    IRecordRepository,
)


class RecordRepository(IRecordRepository):
    def __init__(self, session: AgnosticClientSession):
        self._session: AgnosticCollection = session.client.get_database()[  # type: ignore
            "records"
        ]

    async def save(self, record: RecordDTO) -> RecordDTO:
        model = Record(**record.model_dump())

        result = await self._session.insert_one(model.model_dump(exclude={"id"}))
        record.id = str(result.inserted_id)

        return record

    async def update(self, record: RecordDTO) -> RecordDTO:
        await self._session.update_one(
            {"_id": ObjectId(record.id)}, {"$set": record.model_dump(exclude={"id"})}
        )

        return record

    async def delete(self, record_id: str) -> None:
        await self._session.delete_one({"_id": ObjectId(record_id)})

    async def get_all(self) -> List[RecordDTO]:
        documents = await self._session.find().to_list(length=None)

        return [
            RecordDTO(**document | {"_id": str(document["_id"])})
            for document in documents
        ]

    async def get_by_id(self, record_id: str) -> RecordDTO | None:
        document = await self._session.find_one({"_id": ObjectId(record_id)})

        return RecordDTO(**document | {"_id": str(document["_id"])}) if document else None

    async def get_by_owner_id(self, owner_id: str) -> List[RecordDTO]:
        documents = await self._session.find({"owner_id": owner_id}).to_list(
            length=None
        )

        return [
            RecordDTO(**document | {"_id": str(document["_id"])})
            for document in documents
        ]
