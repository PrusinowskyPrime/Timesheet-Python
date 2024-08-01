import os
from dotenv import load_dotenv

load_dotenv()

ALGORITHM: str = "HS256"  # type: ignore
ACCESS_TOKEN_EXPIRE_MINUTES: float = float(  # type: ignore
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)
LOGIN_URL: str = "/api/v1/auth/login"
REFRESH_TOKEN_SECRET_KEY: str = "your-refresh-secret-key"  # type: ignore
SECRET_KEY: str = "your-secret-key"  # type: ignore
