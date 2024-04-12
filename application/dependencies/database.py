from typing import Annotated, AsyncGenerator

from fastapi import Depends
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticClientSession
from motor.motor_asyncio import AsyncIOMotorClient

from app.settings.database import MONGO_DB_URL, MONGO_INITDB_DATABASE


def get_client() -> AgnosticClient:
    return AsyncIOMotorClient(MONGO_DB_URL)


def get_database(
    client: Annotated[AgnosticClient, Depends(get_client)]
) -> AgnosticDatabase:
    return client[MONGO_INITDB_DATABASE]


async def get_session(
    database: Annotated[AgnosticDatabase, Depends(get_database)]
) -> AsyncGenerator[AgnosticClientSession, None]:
    session = await database.client.start_session()
    async with session.start_transaction():
        try:
            yield session
            await session.commit_transaction()
            await session.end_session()
        except Exception as e:
            await session.abort_transaction()
            raise e
