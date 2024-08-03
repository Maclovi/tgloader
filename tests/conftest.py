from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Literal, TypeAlias, cast

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from loader.adapters.database.models import mapper_registry
from loader.ioc import Container, init_container

if TYPE_CHECKING:
    from loader.config import Config

Env: TypeAlias = Literal["dev", "prod"]


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="my option: dev or prod",
        choices=["prod", "dev"],
    )


@pytest.fixture(scope="session")
def env(request: pytest.FixtureRequest) -> Env:
    return cast(Env, request.config.getoption("--env"))


@pytest.fixture(scope="session")
def ioc(env: Env) -> Container:
    return init_container(env=env)


@pytest.fixture(scope="session")
def config(ioc: Container) -> "Config":
    return ioc.config


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
