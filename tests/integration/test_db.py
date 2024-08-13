from collections.abc import AsyncIterator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from loader.adapters.database.gateway import DatabaseGateway
from loader.adapters.database.models import mapper_registry
from loader.application import FileDatabase, UserDatabase, UserFileDatabase
from loader.domain.models import File, User, UserFile
from loader.ioc import Container


@pytest.fixture(scope="module", autouse=True)
async def create_all_tables(async_engine: AsyncEngine) -> AsyncIterator[None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield None

    async with async_engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


@pytest.fixture(scope="module")
def async_engine(ioc: Container) -> AsyncEngine:
    return ioc._engine


@pytest.fixture()
async def database(ioc: Container) -> AsyncIterator[DatabaseGateway]:
    async with ioc.new_session() as session:
        yield session


@pytest.mark.engine()
class TestEngine:
    def test_engine_name(self, async_engine: AsyncEngine) -> None:
        assert async_engine.name == "postgresql"

    def test_engine_driver(self, async_engine: AsyncEngine) -> None:
        assert async_engine.driver == "psycopg"

    @pytest.mark.asyncio()
    async def test_version(self, async_engine: AsyncEngine) -> None:
        async with async_engine.connect() as conn:
            result = (await conn.execute(text("select version()"))).one()
            assert "PostgreSQL 16.3" in result[0]

    @pytest.mark.asyncio()
    async def test_ping_db(self, async_engine: AsyncEngine) -> None:
        async with async_engine.connect() as conn:
            result = (await conn.execute(text("select 'hello world'"))).one()
            assert result[0] == "hello world"


@pytest.mark.db_user()
class TestUser:
    @pytest.mark.asyncio()
    async def test_add_user(self, database: DatabaseGateway) -> None:
        user = User(1, "Sergey", "Yavorsky", "somenick", "active")
        await UserDatabase(database).create_user(user)

    @pytest.mark.asyncio()
    async def test_add_already_exists(self, database: DatabaseGateway) -> None:
        user = User(1, "Sergey", "Yavorsky", "somenick", "active")
        await UserDatabase(database).create_user(user)

    @pytest.mark.asyncio()
    async def test_get_user(self, database: DatabaseGateway) -> None:
        user = User(1, "Sergey", "Yavorsky", "somenick", "active")
        user_from_db = await database.get_user_by_id(1)

        assert user == user_from_db

    @pytest.mark.asyncio()
    async def test_user_update(self, database: DatabaseGateway) -> None:
        user = User(1, "Sergey", "Yavorsky", "somenick", "inactive")
        await UserDatabase(database).update_status(1, "inactive")
        user_from_db = await database.get_user_by_id(1)

        assert user == user_from_db

    @pytest.mark.asyncio()
    async def test_add_user_status(self, database: DatabaseGateway) -> None:
        user = User(1, "Sergey", "Yavorsky", "somenick", "active")
        await UserDatabase(database).create_user(user)
        user_from_db = await database.get_user_by_id(1)

        assert user == user_from_db


@pytest.mark.db_file()
class TestFile:
    @pytest.mark.asyncio()
    async def test_add_file(self, database: DatabaseGateway) -> None:
        file = File("dasf", "dafsgd", 321)
        await FileDatabase(database).create_file(file)

    @pytest.mark.asyncio()
    async def test_add_already_exists(self, database: DatabaseGateway) -> None:
        file = File("dasf", "dafsgd", 321)
        await FileDatabase(database).create_file(file)

    @pytest.mark.asyncio()
    async def test_file_by_video_id(self, database: DatabaseGateway) -> None:
        file = File("dasf", "dafsgd", 321)
        file_from_db = await FileDatabase(database).get_file_by_videoid("dasf")
        assert file == file_from_db


@pytest.mark.db_userfile()
class TestUserFile:
    @pytest.mark.asyncio()
    async def test_add_userfile(self, database: DatabaseGateway) -> None:
        userfile = UserFile(1, "dasf")
        await UserFileDatabase(database).create_userfile(userfile)

    @pytest.mark.asyncio()
    async def test_add_already_exists(self, database: DatabaseGateway) -> None:
        userfile = UserFile(1, "dasf")
        await UserFileDatabase(database).create_userfile(userfile)
