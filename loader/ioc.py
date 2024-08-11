from dataclasses import dataclass

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from loader.config import Config, load_config


@dataclass(slots=True)
class Container:
    config: Config
    session_maker: async_sessionmaker[AsyncSession]
    _engine: AsyncEngine


def create_engine(db_uri: str) -> AsyncEngine:
    engine = create_async_engine(
        db_uri,
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return engine


def make_asyncsession(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


def init_container() -> Container:
    conf = load_config()
    engine = create_engine(conf.db.db_uri)
    session_maker = make_asyncsession(engine)

    return Container(config=conf, session_maker=session_maker, _engine=engine)
