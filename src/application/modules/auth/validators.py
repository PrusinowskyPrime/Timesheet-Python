from src.application.modules.auth.exceptions import PasswordsAreNotTheSame


class PasswordValidator:
    def validate(self, password: str, password_confirmation: str) -> None:
        if password != password_confirmation:
            raise PasswordsAreNotTheSame()
