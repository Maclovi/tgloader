import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine


def test_engine_name(engine: AsyncEngine) -> None:
    assert engine.name == "postgresql"


def test_engine_driver(engine: AsyncEngine) -> None:
    assert engine.driver == "psycopg"


@pytest.mark.asyncio
async def test_ping_db(new_session: AsyncConnection) -> None:
    result = await new_session.execute(text("select 'hello world'"))
    assert result.one()[0] == "hello world"


@pytest.mark.asyncio
async def test_version(new_session: AsyncConnection) -> None:
    result = await new_session.execute(text("select version()"))
    assert "PostgreSQL 16.3" in result.one()[0]
