from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from loader.adapters.database.gateway import DatabaseGateway
from loader.adapters.database.models import mapper_registry
from loader.ioc import Container


@pytest.fixture(scope="session")
def async_engine(ioc: Container) -> AsyncEngine:
    return ioc._engine


@pytest.fixture(scope="session", autouse=True)
async def create_all_tables(async_engine: AsyncEngine) -> AsyncIterator[None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield None

    async with async_engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


@pytest.fixture
async def new_session(ioc: Container) -> AsyncIterator[AsyncSession]:
    async with ioc.session_maker() as session:
        yield session


@pytest.fixture
async def database(ioc: Container) -> AsyncIterator[DatabaseGateway]:
    async with ioc.session_maker() as session:
        yield DatabaseGateway(session)
