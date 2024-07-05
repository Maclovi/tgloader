import asyncio
import logging
import sys
from collections.abc import Awaitable
from typing import cast

from aiogram import Bot, Dispatcher
from telethon import TelegramClient
from telethon.tl.types import User

from loader.main.config import Config, load_config
from loader.tgbot.handlers import user
from loader.tgclient.handlers import from_bot

logger = logging.getLogger(__name__)


async def tgbot_main() -> None:
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    config: Config = load_config("config.ini")

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    dp.include_router(user.router)

    await dp.start_polling(bot)


async def tgclient_main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    config: Config = load_config("config.ini")

    client = TelegramClient(
        "me",
        api_id=config.tg_client.api_id,
        api_hash=config.tg_client.api_hash,
        device_model="iPhone 11 Pro",
        system_version="IOS 100.1",
    )
    from_bot.include_events_handlers(client)

    async with client:
        me = cast(User, await client.get_me())
        logger.info(
            f"client is starting! name={me.first_name} username={me.username}"
        )
        await cast(Awaitable[None], client.run_until_disconnected())


def cli() -> None:
    """Wrapper for command line"""
    asyncio.run(tgclient_main())
    asyncio.run(tgbot_main())


if __name__ == "__main__":
    cli()
