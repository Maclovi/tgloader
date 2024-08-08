import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from loader.adapters.database.gateway import DatabaseGateway
from loader.domain.models import File, User


@pytest.mark.engine
class TestEngine:
    def test_engine_name(self, async_engine: AsyncEngine) -> None:
        assert async_engine.name == "postgresql"

    def test_engine_driver(self, async_engine: AsyncEngine) -> None:
        assert async_engine.driver == "psycopg"

    @pytest.mark.asyncio
    async def test_version(self, async_engine: AsyncEngine) -> None:
        async with async_engine.connect() as conn:
            result = (await conn.execute(text("select version()"))).one()
            assert "PostgreSQL 16.3" in result[0]

    @pytest.mark.asyncio
    async def test_ping_db(self, async_engine: AsyncEngine) -> None:
        async with async_engine.connect() as conn:
            result = (await conn.execute(text("select 'hello world'"))).one()
            assert result[0] == "hello world"


@pytest.mark.db_user
class TestUser:
    @pytest.mark.asyncio
    async def test_add_user(self, database: DatabaseGateway) -> None:
        user = User(1, "Sergey", "Yavorsky", "somenick", "active")
        await database.add_user(user)

    @pytest.mark.asyncio
    async def test_add_already_exists(self, database: DatabaseGateway) -> None:
        user = User(1, "Sergey", "Yavorsky", "somenick", "active")
        await database.add_user(user)

    @pytest.mark.asyncio
    async def test_get_user(self, database: DatabaseGateway) -> None:
        user = await database.get_user_by_id(1)
        assert user == User(1, "Sergey", "Yavorsky", "somenick", "active")

    @pytest.mark.asyncio
    async def test_do_update(self, database: DatabaseGateway) -> None:
        await database.update_user_status(1, "inactive")

    @pytest.mark.asyncio
    async def test_user_update(self, database: DatabaseGateway) -> None:
        user = await database.get_user_by_id(1)
        assert user == User(1, "Sergey", "Yavorsky", "somenick", "inactive")


@pytest.mark.db_file
class TestFile:
    @pytest.mark.asyncio
    async def test_add_file(self, database: DatabaseGateway) -> None:
        file = File("dasf", "dafsgd", 321)
        await database.add_file(file)

    @pytest.mark.asyncio
    async def test_add_already_exists(self, database: DatabaseGateway) -> None:
        file = File("dasf", "dafsgd", 321)
        await database.add_file(file)

    @pytest.mark.asyncio
    async def test_file_by_video_id(self, database: DatabaseGateway) -> None:
        file = await database.get_file_by_video_id("dasf")
        assert file == File("dasf", "dafsgd", 321)
