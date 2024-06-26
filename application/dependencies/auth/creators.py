from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext

from app.application.modules.auth.services import PasswordHashService, PasswordVerifyService, RefreshTokenService, \
    TokenService
from app.settings.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    REFRESH_TOKEN_SECRET_KEY,
)


def get_crypt_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash_service(
    crypt_context: Annotated[CryptContext, Depends(get_crypt_context)]
) -> PasswordHashService:
    return PasswordHashService(crypt_context)


def get_password_verify_service(
    crypt_context: Annotated[CryptContext, Depends(get_crypt_context)]
) -> PasswordVerifyService:
    return PasswordVerifyService(crypt_context)


def get_token_service() -> TokenService:
    return TokenService(
        algorithm=ALGORITHM,
        secret_key=SECRET_KEY,
        refresh_token_secret_key=REFRESH_TOKEN_SECRET_KEY,
        token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def get_refresh_token_service(
    token_service: Annotated[TokenService, Depends(get_token_service)]
) -> RefreshTokenService:
    return RefreshTokenService(token_service)
