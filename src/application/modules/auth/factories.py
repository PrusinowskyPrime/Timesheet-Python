from datetime import datetime

from src.application.modules.auth.dtos import (
    AuthenticatedUserDTO,
    SuccessAuthenticationDTO,
    CurrentUserDTO,
)


class AuthenticatedUserDTOFactory:
    def create(self, user_id: int | None, email: str) -> AuthenticatedUserDTO:
        return AuthenticatedUserDTO(id=user_id, sub=email)


class SuccessAuthenticationDTOFactory:
    def create(
        self,
        token_type: str,
        access_token: str,
        refresh_token: str,
        expired_at: datetime,
    ) -> SuccessAuthenticationDTO:
        return SuccessAuthenticationDTO(
            token_type=token_type,
            access_token=access_token,
            refresh_token=refresh_token,
            expired_at=expired_at,
        )


class CurrentUserDTOFactory:
    def create(self, user_id: int, email: str) -> CurrentUserDTO:
        return CurrentUserDTO(id=user_id, email=email)
