from abc import ABC, abstractmethod
from typing import List

from time_sheet.src.core.modules.user.dto.user import UserDTO


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: UserDTO) -> UserDTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[UserDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> UserDTO:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        ...

    @abstractmethod
    async def update(self, user: UserDTO) -> UserDTO:
        ...