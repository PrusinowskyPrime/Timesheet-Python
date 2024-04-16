# pylint: disable=R0801, R0913, C0301, R0902:
from typing import List

from app.application.modules.user.use_cases import UserCheckIfEmailExistUseCase, UserCreateUseCase, UserDeleteUseCase, \
    UserGetAllUseCase, UserGetByEmailOrUsernameUseCase, UserGetByIdUseCase, UserUpdateUseCase

from app.application.modules.auth.services import PasswordHashService
from app.application.modules.common.exceptions import EmailAlreadyExists
from app.application.modules.user.dtos import (
    UserCreateDTO,
    UserUpdateDTO, UserDTO,
)


class UserService:
    def __init__(
        self,
        create_use_case: UserCreateUseCase,
        delete_use_case: UserDeleteUseCase,
        update_use_case: UserUpdateUseCase,
        get_all_use_case: UserGetAllUseCase,
        get_by_id_use_case: UserGetByIdUseCase,
        get_by_email_or_username_use_case: UserGetByEmailOrUsernameUseCase,
        password_hash_service: PasswordHashService,
        check_if_email_exist_use_case: UserCheckIfEmailExistUseCase,
    ):
        self._create_use_case = create_use_case
        self._delete_use_case = delete_use_case
        self._update_use_case = update_use_case
        self._get_all_use_case = get_all_use_case
        self._get_by_id_use_case = get_by_id_use_case
        self._get_by_email_or_username_use_case = get_by_email_or_username_use_case
        self._password_hash_service = password_hash_service
        self._check_if_email_exist_use_case = check_if_email_exist_use_case

    async def create(self, request_dto: UserCreateDTO) -> UserDTO:
        request_dto.password = self._password_hash_service.hash(request_dto.password)

        if await self._check_if_email_exist_use_case.execute(request_dto.email):
            raise EmailAlreadyExists()

        return await self._create_use_case.execute(request_dto)

    async def update(self, user_id: str, request_dto: UserUpdateDTO) -> UserDTO:
        return await self._update_use_case.execute(
            request_dto=request_dto, user_id=user_id
        )

    async def delete(self, user_id: str) -> None:
        return await self._delete_use_case.execute(user_id)

    async def get_all(self) -> List[UserDTO]:
        return await self._get_all_use_case.execute()

    async def get_by_id(self, user_id: str) -> UserDTO:
        return await self._get_by_id_use_case.execute(user_id)

    async def get_by_email_or_username(self, field: str) -> UserDTO:
        return await self._get_by_email_or_username_use_case.execute(field)

    async def check_if_email_exist(self, email: str) -> bool:
        return await self._check_if_email_exist_use_case.execute(email)
