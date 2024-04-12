import os

from dotenv import load_dotenv

load_dotenv()

MONGO_INITDB_ROOT_USERNAME: str | None = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD: str | None = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_INITDB_DATABASE: str = os.getenv("MONGO_INITDB_DATABASE")  # type: ignore
MONGO_INITDB_USERNAME: str | None = os.getenv("MONGO_INITDB_USERNAME")
MONGO_INITDB_PASSWORD: str | None = os.getenv("MONGO_INITDB_PASSWORD")
MONGO_DB_URL: str = (
    f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}"
    f"@localhost:27017/{MONGO_INITDB_DATABASE}?authMechanism=DEFAULT&authSource=admin"
)
