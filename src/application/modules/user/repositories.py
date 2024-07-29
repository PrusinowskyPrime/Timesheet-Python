from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.modules.user.dtos import UserDTO
from src.application.modules.user.mappers import UserModelToDomainMapper, UserDomainToModelMapper
from src.application.modules.user.models import UserModel


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: UserDTO) -> UserDTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[UserDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserDTO | None:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> None: ...

    @abstractmethod
    async def update(self, user: UserDTO) -> UserDTO: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDTO | None: ...

    @abstractmethod
    async def get_by_fullname(self, fullname: str) -> UserDTO | None: ...


class UserRepository(IUserRepository):
    def __init__(
        self,
        session: AsyncSession,
        user_domain_to_model_mapper: UserDomainToModelMapper,
        user_model_to_domain_mapper: UserModelToDomainMapper
    ):
        self._session = session
        self._user_domain_to_model_mapper = user_domain_to_model_mapper
        self._user_model_to_domain_mapper = user_model_to_domain_mapper

    async def save(self, user: UserDTO) -> UserDTO:
        model = self._user_domain_to_model_mapper.map(user)

        self._session.add(model)
        await self._session.commit()

        return self._user_model_to_domain_mapper.map(model)

    async def update(self, user: UserDTO) -> UserDTO:
        model = self._user_domain_to_model_mapper.map(user)

        await self._session.merge(model)
        await self._session.commit()

        return user

    async def delete(self, user: UserDTO) -> None:
        query = delete(UserModel).where(UserModel.id == user.id)

        await self._session.execute(query)
        await self._session.commit()

    async def get_all(self) -> List[UserDTO]:
        result = await self._session.execute(select(UserModel))
        data = []

        for user in result.scalars().all():
            data.append(self._user_model_to_domain_mapper.map(user))

        return data

    async def get_by_id(self, user_id: int) -> UserDTO | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )

        return self._user_model_to_domain_mapper.map(result.scalars().first())

    async def get_by_email(self, email: str) -> UserDTO | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)

        )

        return self._user_model_to_domain_mapper.map(result.scalars().first())

    async def get_by_fullname(self, fullname: str) -> UserDTO | None:
        result = await self._session.execute(
            select(UserModel)
            .where(UserModel.fullname == fullname)
        )

        return self._user_model_to_domain_mapper.map(result.scalars().first())
