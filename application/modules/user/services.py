# pylint: disable=R0801, R0913, C0301, R0902:
from typing import List

from app.application.modules.user.dtos import (
    UserCreateDTO,
    UserUpdateDTO, UserDTO,
)


class UserService:
    async def create(self, request_dto: UserCreateDTO) -> UserDTO:
        pass

    async def update(self, user_id: str, request_dto: UserUpdateDTO) -> UserDTO:
        pass

    async def delete(self, user_id: str) -> None:
        pass

    async def get_all(self) -> List[UserDTO]:
        pass

    async def get_by_id(self, user_id: str) -> UserDTO:
        pass

    async def get_by_email_or_username(self, field: str) -> UserDTO:
        pass

    async def check_if_email_exist(self, email: str) -> bool:
        pass
