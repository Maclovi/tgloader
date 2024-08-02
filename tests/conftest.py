from collections.abc import AsyncIterable
from typing import TYPE_CHECKING, Literal, TypeAlias, cast

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
)

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
def engine(ioc: Container) -> AsyncEngine:
    return ioc._engine


@pytest.fixture
async def new_session(ioc: Container) -> AsyncIterable[AsyncSession]:
    async with ioc.session_maker() as session:
        yield session
