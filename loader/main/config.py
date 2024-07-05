import configparser
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_redis: bool


@dataclass
class TgClient:
    api_id: int
    api_hash: str


@dataclass
class Config:
    tg_bot: TgBot
    tg_client: TgClient
    db: DbConfig


@lru_cache
def load_config(path: str) -> Config:
    config = read_conf(path)
    tg_bot = config["bot"]
    tg_client = config["client"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("token"),
            admin_id=tg_bot.getint("admin_id"),
            use_redis=tg_bot.getboolean("use_nats"),
        ),
        tg_client=TgClient(
            api_id=tg_client.getint("api_id"),
            api_hash=tg_client.get("api_hash"),
        ),
        db=DbConfig(**config["db"]),
    )


@lru_cache
def read_conf(path: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(path)
    return config
