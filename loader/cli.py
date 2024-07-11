import asyncio
import logging
import sys
from collections.abc import Awaitable
from multiprocessing import Process
from typing import cast

from aiogram import Bot, Dispatcher
from telethon.tl.types import User

from loader.auth import auth_all
from loader.config import load_config
from loader.tgbot.handlers import from_client, user
from loader.tgclient.client import get_client
from loader.tgclient.handlers import from_bot

logger = logging.getLogger(__name__)


async def tgbot_main() -> None:
    config = load_config("config.ini")
    level = logging.DEBUG if config.tg_bot.debug else logging.INFO
    logging.basicConfig(level=level, stream=sys.stdout)

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(tg_ids=config.tg_ids)
    dp.include_router(from_client.router)
    dp.include_router(user.router)

    await dp.start_polling(bot)


async def tgclient_main() -> None:
    config = load_config("config.ini")
    level = logging.DEBUG if config.tg_client.debug else logging.INFO
    logging.basicConfig(level=level, stream=sys.stdout)
    client = get_client(config.tg_client)
    from_bot.include_events_handlers(client, config.tg_ids)

    async with client:
        await client.get_dialogs()  # for cache
        me = cast(User, await client.get_me())
        logger.info(
            f"client is starting! name={me.first_name} username={me.username}"
        )
        await cast(Awaitable[None], client.run_until_disconnected())


def run_tgbot() -> None:
    asyncio.run(tgbot_main())


def run_tgclient() -> Process:
    def run() -> None:
        asyncio.run(tgclient_main())

    p = Process(target=run, daemon=True)
    p.start()
    return p


def cli() -> None:
    """Wrapper for command line"""
    auth_all()
    _ = run_tgclient()
    run_tgbot()


if __name__ == "__main__":
    cli()
