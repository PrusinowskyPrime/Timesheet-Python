# pylint: disable=R0801, R0913, C0301, R0902:
from typing import List

from src.application.modules.user.dtos import (
    UserCreateDTO,
    UserUpdateDTO, UserDTO,
)
from src.application.modules.user.mappers import UserCreateDTOToDomainMapper
from src.application.modules.user.repositories import IUserRepository

from src.application.modules.auth.services import PasswordHashService
from src.application.modules.common.exceptions import ObjectDoesNotExist
from src.application.modules.user.use_cases import UserGetByEmailOrUsernameUseCase, UserGetByIdUseCase


class UserService:
    def __init__(
        self,
        user_repository: IUserRepository,
        user_create_dto_to_domain_mapper: UserCreateDTOToDomainMapper,
        password_hasher: PasswordHashService,
        user_get_by_email_or_username_use_case: UserGetByEmailOrUsernameUseCase,
        user_get_by_id_use_case: UserGetByIdUseCase
    ):
        self._user_repository = user_repository
        self._user_create_dto_to_domain_mapper = user_create_dto_to_domain_mapper
        self._password_hasher = password_hasher
        self._user_get_by_email_or_username_use_case = user_get_by_email_or_username_use_case
        self._user_get_by_id_use_case = user_get_by_id_use_case

    async def create(self, create_dto: UserCreateDTO) -> UserDTO:
        if await self._check_if_user_with_email_exists(create_dto.email):
            raise ObjectDoesNotExist # AlreadyExists

        dto = self._user_create_dto_to_domain_mapper.map(create_dto)
        dto.password = self._password_hasher.hash(create_dto.password)

        return await self._user_repository.save(dto)

    async def update(self, user_id: int, request_dto: UserUpdateDTO) -> UserDTO:
        dto = await self.get_by_id(user_id)
        dto.fullname = request_dto.fullname

        return await self._user_repository.update(dto)

    async def delete(self, user_id: int) -> None:
        dto = await self._user_get_by_id_use_case.execute(user_id)

        await self._user_repository.delete(dto)

    async def get_all(self) -> List[UserDTO]:
        return await self._user_repository.get_all()

    async def get_by_id(self, user_id: int) -> UserDTO:
        return await self._user_get_by_id_use_case.execute(user_id)

    async def get_by_email_or_username(self, field: str) -> UserDTO:
        return await self._user_get_by_email_or_username_use_case.execute(field)

    async def _check_if_user_with_email_exists(self, email: str) -> bool:
        return self._user_repository.get_by_email(email) is None
