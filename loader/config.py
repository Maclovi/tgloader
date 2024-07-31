import configparser
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class DbConfig:
    user: str
    password: str
    database: str
    host: str
    port: str

    def get_uri(self) -> str:
        return (
            f"{self.user}:{self.password}@{self.host}:{self.port}/"
            f"{self.database}?sslmode=require"
        )


@dataclass(frozen=True)
class TgBot:
    token: str
    use_redis: bool
    debug: bool


@dataclass(frozen=True)
class TgClient:
    api_id: int
    api_hash: str
    debug: bool


@dataclass(frozen=True)
class TelegramIds:
    bot_id: int
    boss_id: int
    client_id: int
    group_error_id: int
    group_cache_id: int


@dataclass(frozen=True)
class Config:
    tg_bot: TgBot
    tg_client: TgClient
    db: DbConfig
    tg_ids: TelegramIds


@lru_cache
def load_config(path: str = "prod.ini") -> Config:
    config = read_conf(path)

    tg_bot = config["bot"]
    tg_client = config["client"]
    tg_ids = config["telegram_ids"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("token"),
            use_redis=tg_bot.getboolean("use_redis"),
            debug=tg_bot.getboolean("debug"),
        ),
        tg_client=TgClient(
            api_id=tg_client.getint("api_id"),
            api_hash=tg_client.get("api_hash"),
            debug=tg_client.getboolean("debug"),
        ),
        tg_ids=TelegramIds(
            bot_id=tg_ids.getint("bot_id"),
            boss_id=tg_ids.getint("boss_id"),
            client_id=tg_ids.getint("client_id"),
            group_error_id=tg_ids.getint("group_error_id"),
            group_cache_id=tg_ids.getint("group_cache_id"),
        ),
        db=DbConfig(**config["db"]),
    )


def read_conf(path: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(path)
    return config
