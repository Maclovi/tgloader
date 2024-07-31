import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine


def test_engine_name(engine: AsyncEngine) -> None:
    assert engine.name == "postgresql"


def test_engine_driver(engine: AsyncEngine) -> None:
    assert engine.driver == "psycopg"


@pytest.mark.asyncio
async def test_ping_db(conn: AsyncConnection) -> None:
    result = await conn.execute(text("select 'hello world'"))
    assert result.one()[0] == "hello world"
