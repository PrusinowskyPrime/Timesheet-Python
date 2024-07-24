import os

from dotenv import load_dotenv

load_dotenv()

DB_ROOT_PASSWORD: str | None = "root_password"
DB_USER: str | None = "my_user"
DB_PASSWORD: str | None = "my_password"
DB_HOST: str | None = "localhost"
DB_PORT: str | None = "3306"
DB_NAME: str | None = "my_database"

DATABASE_URL: str = (
    f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)