from datetime import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from loader.domain.models import File, User


def test_engine_name(async_engine: AsyncEngine) -> None:
    assert async_engine.name == "postgresql"


def test_engine_driver(async_engine: AsyncEngine) -> None:
    assert async_engine.driver == "psycopg"


@pytest.mark.asyncio
async def test_ping_db(new_session: AsyncSession) -> None:
    result = await new_session.execute(text("select 'hello world'"))
    assert result.one()[0] == "hello world"


@pytest.mark.asyncio
async def test_version(new_session: AsyncSession) -> None:
    result = await new_session.execute(text("select version()"))
    assert "PostgreSQL 16.3" in result.one()[0]


@pytest.mark.asyncio
async def test_add_user(new_session: AsyncSession) -> None:
    user = User(
        1,
        "Sergey",
        "Yavorsky",
        "somenick",
        "active",
        datetime.now(),
        updated_at=datetime.now(),
    )
    new_session.add(user)
    await new_session.commit()


@pytest.mark.asyncio
async def test_add_file(new_session: AsyncSession) -> None:
    file = File("dasf", "dafsgd", 321, datetime.now(), datetime.now())
    new_session.add(file)
    await new_session.commit()
