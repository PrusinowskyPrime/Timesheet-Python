# pylint: disable=C0301
from typing import Annotated

from fastapi import Depends

from src.application.modules.auth.factories import (
    AuthenticatedUserDTOFactory,
    SuccessAuthenticationDTOFactory,
)
from src.application.modules.auth.services import (
    LoginService,
    PasswordHashService,
    PasswordVerifyService,
    PasswordChangeService,
    TokenService,
)
from src.application.modules.auth.validators import PasswordValidator
from src.application.modules.user.repositories import IUserRepository
from src.application.modules.user.use_cases import (
    UserGetByEmailOrUsernameUseCase,
    UserGetByIdUseCase,
)
from src.dependencies.auth.creators import (
    get_password_hash_service,
    get_password_verify_service,
    get_token_service,
    get_authenticated_user_dto_factory,
    get_success_authentication_dto_factory,
)
from src.dependencies.user_factories import (
    get_user_repository,
    get_user_get_by_id_use_case,
    get_user_get_by_email_or_username_use_case,
)


def get_password_validator() -> PasswordValidator:
    return PasswordValidator()


def get_password_change_service(
    user_get_by_id_use_case: Annotated[
        UserGetByIdUseCase, Depends(get_user_get_by_id_use_case)
    ],
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
    password_hash_service: Annotated[
        PasswordHashService, Depends(get_password_hash_service)
    ],
    password_validator: Annotated[PasswordValidator, Depends(get_password_validator)],
) -> PasswordChangeService:
    return PasswordChangeService(
        user_repository=user_repository,
        user_get_by_id_use_case=user_get_by_id_use_case,
        password_hash_service=password_hash_service,
        password_validator=password_validator,
    )


def get_login_service(
    password_verify_service: Annotated[
        PasswordVerifyService, Depends(get_password_verify_service)
    ],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    user_get_by_email_or_username_use_case: Annotated[
        UserGetByEmailOrUsernameUseCase,
        Depends(get_user_get_by_email_or_username_use_case),
    ],
    authenticated_user_dto_factory: Annotated[
        AuthenticatedUserDTOFactory, Depends(get_authenticated_user_dto_factory)
    ],
    success_authentication_dto_factory: Annotated[
        SuccessAuthenticationDTOFactory, Depends(get_success_authentication_dto_factory)
    ],
) -> LoginService:
    return LoginService(
        password_verify_service=password_verify_service,
        token_service=token_service,
        user_get_by_email_or_username_use_case=user_get_by_email_or_username_use_case,
        authenticated_user_dto_factory=authenticated_user_dto_factory,
        success_authentication_dto_factory=success_authentication_dto_factory,
    )
