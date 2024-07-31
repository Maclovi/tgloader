import argparse
import asyncio
import logging
import sys
from collections.abc import Awaitable
from multiprocessing import Process
from subprocess import run as run_shell
from typing import cast

from aiogram import Bot, Dispatcher
from telethon.tl.types import User

from loader.config import load_config
from loader.tgbot.handlers import fromclient, user
from loader.tgclient.client import get_client
from loader.tgclient.handlers import frombot

logger = logging.getLogger(__name__)


async def tgbot_main() -> None:
    config = load_config("prod.ini")
    level = logging.DEBUG if config.tg_bot.debug else logging.INFO
    logging.basicConfig(level=level, stream=sys.stdout)

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(tg_ids=config.tg_ids)
    dp.include_router(fromclient.router)
    dp.include_router(user.router)

    await dp.start_polling(bot)


async def tgclient_main() -> None:
    config = load_config("prod.ini")
    level = logging.DEBUG if config.tg_client.debug else logging.INFO
    logging.basicConfig(level=level, stream=sys.stdout)
    client = get_client(config.tg_client)
    frombot.include_events_handlers(client, config.tg_ids)

    async with client:
        await client.get_dialogs()  # for cache
        me = cast(User, await client.get_me())
        logger.info(
            f"client is starting! name={me.first_name} username={me.username}"
        )
        await cast(Awaitable[None], client.run_until_disconnected())


def run_tgbot_async() -> None:
    asyncio.run(tgbot_main())


def run_tgclient_async() -> None:
    asyncio.run(tgclient_main())


def run_tgclient_process() -> Process:
    def run() -> None:
        asyncio.run(tgclient_main())

    p = Process(target=run, daemon=True)
    p.start()
    return p


def cli() -> None:
    """Wrapper for command line"""
    parser = argparse.ArgumentParser(description="Process start services")
    parser.add_argument(
        "--run",
        default="all",
        help="how we launch services",
        choices=["all", "bot", "client"],
    )
    args = parser.parse_args()

    if args.run in ("all", "client"):
        run_shell(["python", "loader/auth.py"])

    if args.run == "all":
        _ = run_tgclient_process()
        run_tgbot_async()
    elif args.run == "bot":
        run_tgbot_async()
    elif args.run == "client":
        run_tgclient_async()


if __name__ == "__main__":
    cli()
