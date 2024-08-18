from collections.abc import AsyncIterator
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from dataclasses import dataclass
from functools import partial

from aiohttp import ClientSession
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from loader.adapters.database.gateway import DatabaseGateway
from loader.adapters.stub_http import ClientSessionStub
from loader.config import Config, load_config

IterDatabaseGateway = AsyncIterator[DatabaseGateway]


@dataclass(slots=True, kw_only=True)
class Container:
    config: Config
    new_session: partial[_AsyncGeneratorContextManager[DatabaseGateway]]
    http_client: ClientSession
    redis: Redis  # type: ignore
    _engine: AsyncEngine

    async def aclose(self) -> None:
        await self.http_client.close()
        await self.redis.aclose()  # type: ignore


def create_engine(db_uri: str, echo: bool = True) -> AsyncEngine:
    engine = create_async_engine(
        db_uri,
        echo=echo,
        pool_size=15,
        max_overflow=15,
        connect_args={"connect_timeout": 5},
    )
    return engine


def maker_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


@asynccontextmanager
async def new_session(
    session_maker: async_sessionmaker[AsyncSession],
) -> IterDatabaseGateway:
    async with session_maker() as session:
        yield DatabaseGateway(session)


def init_container(*, resolve_httpclient: bool = False) -> Container:
    conf = load_config()
    engine = create_engine(conf.db.db_uri, conf.db.debug)
    session_maker = maker_session(engine)
    session = partial(new_session, session_maker)

    http_client = ClientSessionStub() if resolve_httpclient else ClientSession()

    return Container(
        config=conf,
        new_session=session,
        http_client=http_client,
        redis=Redis.from_url(conf.redis.redis_uri),
        _engine=engine,
    )
