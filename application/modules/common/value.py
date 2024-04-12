class PasswordsDoNotMatch(ValueError):
    def __init__(self):
        super().__init__("Passwords do not match")
