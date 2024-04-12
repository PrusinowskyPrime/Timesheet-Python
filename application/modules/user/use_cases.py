from typing import List

from app.application.modules.user.dtos import UserCreateDTO, UserUpdateDTO, UserDTO
from app.application.modules.common.exceptions import ObjectDoesNotExist
from app.application.modules.user.repository import IUserRepository


class UserCheckIfEmailExistUseCase:
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def execute(self, field: str) -> bool:
        user = await self._repository.get_by_email(field)
        if user is not None:
            return True

        return False


class UserCreateUseCase:
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def execute(self, request_dto: UserCreateDTO) -> UserDTO:
        return await self._repository.save(
            UserDTO(**request_dto.model_dump(), _id=None)
        )


class UserGetAllUseCase:
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def execute(self) -> List[UserDTO]:
        return await self._repository.get_all()


class UserGetByEmailOrUsernameUseCase:
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def execute(self, field: str) -> UserDTO:
        user = await self._repository.get_by_email(field)
        if user is not None:
            return user

        user = await self._repository.get_by_username(field)
        if user is not None:
            return user

        raise ObjectDoesNotExist()


class UserGetByIdUseCase:
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def execute(self, user_id: str) -> UserDTO:
        user = await self._repository.get_by_id(user_id=user_id)

        if user is None:
            raise ObjectDoesNotExist

        return user


class UserUpdateUseCase:
    def __init__(
        self, repository: IUserRepository, get_by_id_use_case: UserGetByIdUseCase
    ):
        self._repository = repository
        self._get_by_id_use_case = get_by_id_use_case

    async def execute(self, request_dto: UserUpdateDTO, user_id: str) -> UserDTO:
        user_dto = await self._get_by_id_use_case.execute(user_id)
        for key, value in request_dto.model_dump().items():
            setattr(user_dto, key, value)

        return await self._repository.update(user_dto)


class UserDeleteUseCase:
    def __init__(
        self, repository: IUserRepository, get_by_id_use_case: UserGetByIdUseCase
    ):
        self._repository = repository
        self._get_by_id_use_case = get_by_id_use_case

    async def execute(self, user_id: str) -> None:
        await self._get_by_id_use_case.execute(user_id)

        return await self._repository.delete(user_id=user_id)
