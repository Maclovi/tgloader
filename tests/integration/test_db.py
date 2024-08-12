from collections.abc import AsyncIterator

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from loader.adapters.database.gateway import DatabaseGateway
from loader.adapters.database.models import mapper_registry
from loader.domain.models import File, User, UserFile
from loader.ioc import Container


@pytest.fixture(scope="session", autouse=True)
async def create_all_tables(async_engine: AsyncEngine) -> AsyncIterator[None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield None

    async with async_engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


@pytest.fixture(scope="session")
def async_engine(ioc: Container) -> AsyncEngine:
    return ioc._engine


@pytest.fixture()
async def new_session(ioc: Container) -> AsyncIterator[AsyncSession]:
    async with ioc.session_maker() as session:
        yield session


@pytest.fixture()
async def database(ioc: Container) -> AsyncIterator[DatabaseGateway]:
    async with ioc.session_maker() as session:
        yield DatabaseGateway(session)


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
        await database.add_user(user)
        await database.session.commit()

    @pytest.mark.asyncio()
    async def test_add_already_exists(self, database: DatabaseGateway) -> None:
        user = User(1, "Sergey", "Yavorsky", "somenick", "active")
        await database.add_if_possible(user)

    @pytest.mark.asyncio()
    async def test_get_user(self, database: DatabaseGateway) -> None:
        user = await database.get_user_by_id(1)
        assert user == User(1, "Sergey", "Yavorsky", "somenick", "active")

    @pytest.mark.asyncio()
    async def test_do_update(self, database: DatabaseGateway) -> None:
        await database.update_user_status(1, "inactive")
        await database.session.commit()

    @pytest.mark.asyncio()
    async def test_user_update(self, database: DatabaseGateway) -> None:
        user = await database.get_user_by_id(1)
        assert user == User(1, "Sergey", "Yavorsky", "somenick", "inactive")


@pytest.mark.db_file()
class TestFile:
    @pytest.mark.asyncio()
    async def test_add_file(self, database: DatabaseGateway) -> None:
        file = File("dasf", "dafsgd", 321)
        await database.add_file(file)
        await database.session.commit()

    @pytest.mark.asyncio()
    async def test_add_already_exists(self, database: DatabaseGateway) -> None:
        file = File("dasf", "dafsgd", 321)
        await database.add_if_possible(file)

    @pytest.mark.asyncio()
    async def test_file_by_video_id(self, database: DatabaseGateway) -> None:
        file = await database.get_file_by_video_id("dasf")
        assert file == File("dasf", "dafsgd", 321)


@pytest.mark.db_userfile()
class TestUserFile:
    @pytest.mark.asyncio()
    async def test_add_userfile(self, database: DatabaseGateway) -> None:
        userfile = UserFile(1, "dasf")
        await database.add_userfile(userfile)
        await database.session.commit()

    @pytest.mark.asyncio()
    async def test_add_already_exists(self, database: DatabaseGateway) -> None:
        userfile = UserFile(1, "dasf")
        await database.add_if_possible(userfile)

    @pytest.mark.xfail(raises=IntegrityError)
    @pytest.mark.asyncio()
    async def test_add_user_no_exists(self, database: DatabaseGateway) -> None:
        userfile = UserFile(2, "dasf")
        await database.add_userfile(userfile)
        await database.session.commit()
