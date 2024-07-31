from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext

from src.application.modules.auth.factories import (
    AuthenticatedUserDTOFactory,
    CurrentUserDTOFactory,
    SuccessAuthenticationDTOFactory,
)
from src.application.modules.auth.services import (
    PasswordHashService,
    PasswordVerifyService,
    RefreshTokenService,
    TokenService,
)
from src.settings.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    REFRESH_TOKEN_SECRET_KEY,
)


def get_crypt_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_authenticated_user_dto_factory() -> AuthenticatedUserDTOFactory:
    return AuthenticatedUserDTOFactory()


def get_success_authentication_dto_factory() -> SuccessAuthenticationDTOFactory:
    return SuccessAuthenticationDTOFactory()


def get_current_user_dto_factory() -> CurrentUserDTOFactory:
    return CurrentUserDTOFactory()


def get_password_hash_service(
    crypt_context: Annotated[CryptContext, Depends(get_crypt_context)]
) -> PasswordHashService:
    return PasswordHashService(crypt_context)


def get_password_verify_service(
    crypt_context: Annotated[CryptContext, Depends(get_crypt_context)]
) -> PasswordVerifyService:
    return PasswordVerifyService(crypt_context)


def get_token_service(
    current_user_dto_factory: Annotated[
        CurrentUserDTOFactory, Depends(get_current_user_dto_factory)
    ]
) -> TokenService:
    return TokenService(
        algorithm=ALGORITHM,
        secret_key=SECRET_KEY,
        refresh_token_secret_key=REFRESH_TOKEN_SECRET_KEY,
        token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        current_user_dto_factory=current_user_dto_factory,
    )


def get_refresh_token_service(
    token_service: Annotated[TokenService, Depends(get_token_service)],
    authenticated_user_dto_factory: Annotated[
        AuthenticatedUserDTOFactory, Depends(get_authenticated_user_dto_factory)
    ],
    success_authentication_dto_factory: Annotated[
        SuccessAuthenticationDTOFactory, Depends(get_success_authentication_dto_factory)
    ],
) -> RefreshTokenService:
    return RefreshTokenService(
        token_service=token_service,
        authenticated_user_dto_factory=authenticated_user_dto_factory,
        success_authentication_dto_factory=success_authentication_dto_factory,
    )
