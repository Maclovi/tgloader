from collections.abc import AsyncGenerator
from typing import Any, cast

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    create_async_engine,
)

from loader.config import Config, load_config


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="my option: dev or prod",
    )


@pytest.fixture(scope="session")
def env(request: pytest.FixtureRequest) -> str:
    return cast(str, request.config.getoption("--env"))


@pytest.fixture(scope="session")
def config(env: str) -> Config:
    return load_config(env + ".ini")


@pytest.fixture(scope="session")
def engine(config: Config) -> AsyncEngine:
    db = config.db
    engine = create_async_engine(f"postgresql+psycopg://{db.get_uri()}")
    return engine


@pytest.fixture
async def conn(engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, Any]:
    async with engine.connect() as conn:
        yield conn
