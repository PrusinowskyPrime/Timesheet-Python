from src.application.modules.common.exceptions import ObjectDoesNotExist
from src.application.modules.user.dtos import UserDTO
from src.application.modules.user.repositories import IUserRepository


class UserGetByEmailOrUsernameUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def execute(self, field: str) -> UserDTO:
        dto = await self._user_repository.get_by_email(field)
        if dto is not None:
            return dto

        dto = await self._user_repository.get_by_fullname(field)
        if dto is not None:
            return dto

        raise ObjectDoesNotExist()


class UserGetByIdUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def execute(self, user_id: int) -> UserDTO:
        dto = await self._user_repository.get_by_id(user_id)

        if dto is None:
            raise ObjectDoesNotExist

        return dto
