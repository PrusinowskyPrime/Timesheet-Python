from typing import List

from bson import ObjectId
from motor.core import AgnosticClientSession, AgnosticCollection

from app.application.modules.user.dtos import UserDTO
from app.application.modules.user.models import User
from app.application.modules.user.repository import (
    IUserRepository,
)


class UserRepository(IUserRepository):
    def __init__(self, session: AgnosticClientSession):
        self._session: AgnosticCollection = session.client.get_database()["users"]  # type: ignore

    async def save(self, user: UserDTO) -> UserDTO:
        model = User(**user.model_dump())

        result = await self._session.insert_one(model.model_dump(exclude={"id"}))
        user.id = str(result.inserted_id)

        return user

    async def update(self, user: UserDTO) -> UserDTO:
        await self._session.update_one(
            {"_id": ObjectId(user.id)}, {"$set": user.model_dump(exclude={"id"})}
        )

        return user

    async def delete(self, user_id: str) -> None:
        await self._session.delete_one({"_id": ObjectId(user_id)})

    async def get_all(self) -> List[UserDTO]:
        documents = await self._session.find().to_list(length=None)

        return [
            UserDTO(**document | {"_id": str(document["_id"])})
            for document in documents
        ]

    async def get_by_id(self, user_id: str) -> UserDTO | None:
        document = await self._session.find_one({"_id": ObjectId(user_id)})

        return UserDTO(**document | {"_id": str(document["_id"])}) if document else None

    async def get_by_email(self, email: str) -> UserDTO | None:
        document = await self._session.find_one({"email": email})

        return UserDTO(**document | {"_id": str(document["_id"])}) if document else None

    async def get_by_username(self, username: str) -> UserDTO | None:
        document = await self._session.find_one({"fullname": username})

        return UserDTO(**document | {"_id": str(document["_id"])}) if document else None
