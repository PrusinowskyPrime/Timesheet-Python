from datetime import datetime, timedelta

from app.application.modules.user.use_cases import UserGetByEmailOrUsernameUseCase, UserGetByIdUseCase
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.application.modules.auth.dtos import SuccessAuthenticationDTO, AuthenticatedUserDTO, ChangePasswordDTO, \
    CurrentUserDTO
from app.application.modules.common.exceptions import InvalidCredentials
from app.application.modules.user.dtos import UserDTO
from app.application.modules.user.repositories import IUserRepository


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
        get_by_id_use_case: UserGetByIdUseCase,
        hash_service: PasswordHashService,
        verify_service: PasswordVerifyService,
    ):
        self._user_repository = user_repository
        self._get_by_id_use_case = get_by_id_use_case
        self._hash_service = hash_service
        self._verify_service = verify_service

    async def change_password(
        self, user_id: str, request: ChangePasswordDTO
    ) -> UserDTO:
        user = await self._get_by_id_use_case.execute(user_id)

        if not self._verify_service.verify(request.current_password, user.password):
            raise InvalidCredentials()

        user.password = self._hash_service.hash(request.password)
        user = await self._user_repository.update(user)

        return user


class TokenService:
    def __init__(
        self,
        algorithm: str,
        refresh_token_secret_key: str,
        secret_key: str,
        token_expire_minutes: float,
    ):
        self.algorithm = algorithm
        self.refresh_token_secret_key = refresh_token_secret_key
        self.secret_key = secret_key
        self.token_expire_minutes = token_expire_minutes

    def create_access_token(self, data: AuthenticatedUserDTO) -> str:
        to_encode = data.model_copy().model_dump()
        to_encode.update({"exp": self.get_expire_token_datetime()})

        return jwt.encode(  # type: ignore
            claims=to_encode, key=self.secret_key, algorithm=self.algorithm
        )

    def create_refresh_token(self, data: AuthenticatedUserDTO) -> str:
        to_encode = data.model_copy().model_dump()
        to_encode.update({"exp": self.get_expire_token_datetime()})

        return jwt.encode(  # type: ignore
            claims=to_encode,
            key=self.refresh_token_secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> CurrentUserDTO:
        try:
            payload = jwt.decode(
                token=token, key=self.secret_key, algorithms=[self.algorithm]
            )
            email = payload.get("sub")
            user_id = payload.get("id")

            if email is None or user_id is None:
                raise InvalidCredentials()

            return CurrentUserDTO(id=user_id, email=email)
        except JWTError as exc:
            raise InvalidCredentials() from exc

    def get_expire_token_datetime(self) -> datetime:
        return datetime.now() + timedelta(minutes=self.token_expire_minutes)


class RefreshTokenService:
    def __init__(self, token_service: TokenService):
        self._token_service = token_service

    def refresh(self, token: str) -> SuccessAuthenticationDTO:
        decoded_data = self._token_service.decode(token)
        token_data = AuthenticatedUserDTO(id=decoded_data.id, sub=decoded_data.email)

        return SuccessAuthenticationDTO(
            token_type="Bearer",
            access_token=self._token_service.create_access_token(token_data),
            refresh_token=self._token_service.create_refresh_token(token_data),
            expired_at=self._token_service.get_expire_token_datetime(),
        )


class LoginService:
    def __init__(
        self,
        verify_service: PasswordVerifyService,
        token_service: TokenService,
        user_get_by_email_or_username_use_case: UserGetByEmailOrUsernameUseCase,
    ):
        self._verify_service = verify_service
        self._token_service = token_service
        self._user_get_by_email_or_username_use_case = (
            user_get_by_email_or_username_use_case
        )

    async def login(self, username: str, password: str) -> SuccessAuthenticationDTO:
        user = await self._authenticate(username, password)

        return SuccessAuthenticationDTO(
            token_type="Bearer",
            access_token=self._token_service.create_access_token(user),
            refresh_token=self._token_service.create_refresh_token(user),
            expired_at=self._token_service.get_expire_token_datetime(),
        )

    async def _authenticate(self, username: str, password: str) -> AuthenticatedUserDTO:
        user = await self._user_get_by_email_or_username_use_case.execute(username)

        if not self._verify_service.verify(password, user.password):
            raise InvalidCredentials()

        return AuthenticatedUserDTO(id=user.id, sub=user.email)