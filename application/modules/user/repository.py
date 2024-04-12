from abc import ABC, abstractmethod
from typing import List

from app.application.modules.user.dtos import UserDTO


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
    async def get_by_username(self, username: str) -> UserDTO | None: ...
