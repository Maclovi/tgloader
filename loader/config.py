from dataclasses import dataclass
from os import environ as env


@dataclass(frozen=True, slots=True)
class DbConfig:
    user: str
    password: str
    database: str
    host: str
    port: str
    db_uri: str


@dataclass(frozen=True, slots=True)
class TgBot:
    token: str
    use_redis: bool
    debug: bool


@dataclass(frozen=True, slots=True)
class TgClient:
    api_id: int
    api_hash: str
    debug: bool


@dataclass(frozen=True, slots=True)
class TelegramIds:
    bot_id: int
    client_id: int
    group_error_id: int
    group_cache_id: int


@dataclass(frozen=True, slots=True)
class Config:
    tg_bot: TgBot
    tg_client: TgClient
    db: DbConfig
    tg_ids: TelegramIds


def load_config() -> Config:
    return Config(
        tg_bot=TgBot(
            token=env["TOKEN"],
            use_redis=env["USE_REDIS"] == "true",
            debug=env["DEBUG"] == "true",
        ),
        tg_client=TgClient(
            api_id=int(env["API_ID"]),
            api_hash=env["API_HASH"],
            debug=env["DEBUG"] == "true",
        ),
        tg_ids=TelegramIds(
            bot_id=int(env["BOT_ID"]),
            client_id=int(env["CLIENT_ID"]),
            group_error_id=int(env["GROUP_ERROR_ID"]),
            group_cache_id=int(env["GROUP_CACHE_ID"]),
        ),
        db=DbConfig(
            env["DB_USER"],
            env["DB_PASSWORD"],
            env["DB_DATABASE"],
            env["DB_HOST"],
            env["DB_PORT"],
            "postgresql+psycopg" + env["DB_URI"].replace("postgres", "", 1),
        ),
    )
