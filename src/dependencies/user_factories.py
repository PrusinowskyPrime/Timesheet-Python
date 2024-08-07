# pylint: disable=R0913, C0301
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.modules.user.use_cases import UserGetByEmailOrUsernameUseCase, UserGetByIdUseCase
from src.dependencies.auth.creators import (
    get_password_hash_service,
)
from src.dependencies.database import get_session
from src.application.modules.auth.services import PasswordHashService
from src.application.modules.user.mappers import UserCreateDTOToDomainMapper, UserDomainToModelMapper
from src.application.modules.user.mappers import UserModelToDomainMapper
from src.application.modules.user.repositories import (
    UserRepository, IUserRepository,
)
from src.application.modules.user.services import UserService


def get_user_create_dto_to_domain_mapper() -> UserCreateDTOToDomainMapper:
    return UserCreateDTOToDomainMapper()


def get_user_domain_to_model_mapper() -> UserDomainToModelMapper:
    return UserDomainToModelMapper()


def get_user_model_to_domain_mapper() -> UserModelToDomainMapper:
    return UserModelToDomainMapper()


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_domain_to_model_mapper: Annotated[UserDomainToModelMapper, Depends(get_user_domain_to_model_mapper)],
    user_model_to_domain_mapper: Annotated[UserModelToDomainMapper, Depends(get_user_model_to_domain_mapper)]
) -> IUserRepository:
    return UserRepository(
        session=session,
        user_domain_to_model_mapper=user_domain_to_model_mapper,
        user_model_to_domain_mapper=user_model_to_domain_mapper
    )


def get_user_get_by_email_or_username_use_case(
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)]
) -> UserGetByEmailOrUsernameUseCase:
    return UserGetByEmailOrUsernameUseCase(user_repository)


def get_user_get_by_id_use_case(
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)]
) -> UserGetByIdUseCase:
    return UserGetByIdUseCase(user_repository)


def get_user_service(
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
    user_create_dto_to_domain_mapper: Annotated[
        UserCreateDTOToDomainMapper, Depends(get_user_create_dto_to_domain_mapper)
    ],
    password_hasher: Annotated[PasswordHashService, Depends(get_password_hash_service)],
    user_get_by_email_or_username_use_case: Annotated[
        UserGetByEmailOrUsernameUseCase, Depends(get_user_get_by_email_or_username_use_case)
    ],
    user_get_by_id_use_case: Annotated[UserGetByIdUseCase, Depends(get_user_get_by_id_use_case)]
) -> UserService:
    return UserService(
        user_repository=user_repository,
        user_create_dto_to_domain_mapper=user_create_dto_to_domain_mapper,
        password_hasher=password_hasher,
        user_get_by_email_or_username_use_case=user_get_by_email_or_username_use_case,
        user_get_by_id_use_case=user_get_by_id_use_case
    )
