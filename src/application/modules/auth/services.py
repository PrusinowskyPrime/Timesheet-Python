# pylint: disable=R0913
from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext

from src.application.modules.auth.dtos import (
    SuccessAuthenticationDTO,
    AuthenticatedUserDTO,
    ChangePasswordDTO,
    CurrentUserDTO,
)
from src.application.modules.auth.factories import (
    AuthenticatedUserDTOFactory,
    SuccessAuthenticationDTOFactory,
    CurrentUserDTOFactory,
)
from src.application.modules.auth.validators import PasswordValidator
from src.application.modules.common.exceptions import InvalidCredentials
from src.application.modules.user.dtos import UserDTO
from src.application.modules.user.repositories import IUserRepository
from src.application.modules.user.use_cases import (
    UserGetByEmailOrUsernameUseCase,
    UserGetByIdUseCase,
)


class PasswordHashService:
    def __init__(self, crypt: CryptContext):
        self._crypt = crypt

    def hash(self, password: str) -> str:
        return self._crypt.hash(password)


class PasswordVerifyService:
    def __init__(self, crypt: CryptContext):
        self._crypt = crypt

    def verify(self, password: str, password_hash: str) -> bool:
        return self._crypt.verify(password, password_hash)


class PasswordChangeService:
    def __init__(
        self,
        user_repository: IUserRepository,
        user_get_by_id_use_case: UserGetByIdUseCase,
        password_hash_service: PasswordHashService,
        password_validator: PasswordValidator,
    ):
        self._user_repository = user_repository
        self._user_get_by_id_use_case = user_get_by_id_use_case
        self._password_hash_service = password_hash_service
        self._password_validator = password_validator

    async def change_password(
        self, user_id: int, request: ChangePasswordDTO  # pylint: disable=W0613
    ) -> UserDTO | None:
        self._password_validator.validate(
            request.password, request.password_confirmation
        )

        user = await self._user_get_by_id_use_case.execute(user_id)
        user.password = self._password_hash_service.hash(request.password)

        return await self._user_repository.update(user)


class TokenService:
    def __init__(
        self,
        algorithm: str,
        refresh_token_secret_key: str,
        secret_key: str,
        token_expire_minutes: float,
        current_user_dto_factory: CurrentUserDTOFactory,
    ):
        self._algorithm = algorithm
        self._refresh_token_secret_key = refresh_token_secret_key
        self._secret_key = secret_key
        self._token_expire_minutes = token_expire_minutes
        self._current_user_dto_factory = current_user_dto_factory

    def create_access_token(self, data: AuthenticatedUserDTO) -> str:
        to_encode = data.model_copy().model_dump()
        to_encode.update({"exp": self.get_expire_token_datetime()})

        return jwt.encode(  # type: ignore
            claims=to_encode, key=self._secret_key, algorithm=self._algorithm
        )

    def create_refresh_token(self, data: AuthenticatedUserDTO) -> str:
        to_encode = data.model_copy().model_dump()
        to_encode.update({"exp": self.get_expire_token_datetime()})

        return jwt.encode(  # type: ignore
            claims=to_encode,
            key=self._refresh_token_secret_key,
            algorithm=self._algorithm,
        )

    def decode(self, token: str) -> CurrentUserDTO:
        try:
            payload = jwt.decode(
                token=token, key=self._secret_key, algorithms=[self._algorithm]
            )
            email = payload.get("sub")
            user_id = payload.get("id")

            if email is None or user_id is None:
                raise InvalidCredentials()

            return self._current_user_dto_factory.create(user_id=user_id, email=email)
        except JWTError as exc:
            raise InvalidCredentials() from exc

    def get_expire_token_datetime(self) -> datetime:
        return datetime.now() + timedelta(minutes=self._token_expire_minutes)


class RefreshTokenService:
    def __init__(
        self,
        token_service: TokenService,
        authenticated_user_dto_factory: AuthenticatedUserDTOFactory,
        success_authentication_dto_factory: SuccessAuthenticationDTOFactory,
    ):
        self._token_service = token_service
        self._authenticated_user_dto_factory = authenticated_user_dto_factory
        self._success_authentication_dto_factory = success_authentication_dto_factory

    def refresh(self, token: str) -> SuccessAuthenticationDTO:
        decoded_data = self._token_service.decode(token)
        token_data = self._authenticated_user_dto_factory.create(
            user_id=decoded_data.id, email=decoded_data.email
        )

        return self._success_authentication_dto_factory.create(
            token_type="Bearer",
            access_token=self._token_service.create_access_token(token_data),
            refresh_token=self._token_service.create_refresh_token(token_data),
            expired_at=self._token_service.get_expire_token_datetime(),
        )


class LoginService:
    def __init__(
        self,
        token_service: TokenService,
        password_verify_service: PasswordVerifyService,
        user_get_by_email_or_username_use_case: UserGetByEmailOrUsernameUseCase,
        authenticated_user_dto_factory: AuthenticatedUserDTOFactory,
        success_authentication_dto_factory: SuccessAuthenticationDTOFactory,
    ):
        self._token_service = token_service
        self._password_verify_service = password_verify_service
        self._user_get_by_email_or_username_use_case = (
            user_get_by_email_or_username_use_case
        )
        self._authenticated_user_dto_factory = authenticated_user_dto_factory
        self._success_authentication_dto_factory = success_authentication_dto_factory

    async def login(self, username: str, password: str) -> SuccessAuthenticationDTO:
        user = await self._authenticate(username, password)

        return self._success_authentication_dto_factory.create(
            token_type="Bearer",
            access_token=self._token_service.create_access_token(user),
            refresh_token=self._token_service.create_refresh_token(user),
            expired_at=self._token_service.get_expire_token_datetime(),
        )

    async def _authenticate(self, username: str, password: str) -> AuthenticatedUserDTO:
        user = await self._user_get_by_email_or_username_use_case.execute(username)

        if not self._password_verify_service.verify(password, user.password):
            raise InvalidCredentials()

        return self._authenticated_user_dto_factory.create(
            user_id=user.id, email=user.email
        )
