import asyncio
import logging
import sys
from collections.abc import Awaitable
from multiprocessing import Process
from typing import cast

from aiogram import Bot, Dispatcher
from telethon import TelegramClient
from telethon.tl.types import User

from loader.main.config import load_config
from loader.tgbot.handlers import from_client, user
from loader.tgclient.handlers import from_bot

logger = logging.getLogger(__name__)


async def tgbot_main() -> None:
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    config = load_config("config.ini")
    client_id = config.tg_ids.client_id

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(client_id=client_id)
    dp.include_router(from_client.router)
    dp.include_router(user.router)

    await dp.start_polling(bot)


async def tgclient_main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    config = load_config("config.ini")

    client = TelegramClient(
        "me",
        api_id=config.tg_client.api_id,
        api_hash=config.tg_client.api_hash,
        device_model="iPhone 11 Pro",
        system_version="IOS 100.1",
    )
    from_bot.include_events_handlers(client, config.tg_ids)

    async with client:
        me = cast(User, await client.get_me())
        logger.info(
            f"client is starting! name={me.first_name} username={me.username}"
        )
        await cast(Awaitable[None], client.run_until_disconnected())


def run_tgbot() -> None:
    asyncio.run(tgbot_main())


def run_tgclient() -> None:
    def run() -> None:
        asyncio.run(tgclient_main())

    p = Process(target=run)
    p.start()


def cli() -> None:
    """Wrapper for command line"""
    run_tgclient()
    run_tgbot()


if __name__ == "__main__":
    cli()
