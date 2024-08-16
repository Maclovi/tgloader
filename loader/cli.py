import argparse
import asyncio
import logging
import sys
from collections.abc import Awaitable
from multiprocessing import Process
from subprocess import run as run_shell
from typing import Final, cast

from aiogram import Bot, Dispatcher
from telethon.tl.types import User

from loader.ioc import init_container
from loader.tgbot.handlers import fromclient, user
from loader.tgclient.client import get_client
from loader.tgclient.handlers import frombot

logger = logging.getLogger(__name__)
FORMAT: Final = "[%(asctime)s] [%(name)s]" "[%(levelname)s] > %(message)s"


async def tgbot_main() -> None:
    container = init_container()

    level = logging.INFO
    if container.config.tg_bot.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level, stream=sys.stdout, format=FORMAT)

    bot = Bot(token=container.config.tg_bot.token)
    dp = Dispatcher(ioc=container)
    dp.include_router(fromclient.router)
    dp.include_router(user.router)

    try:
        await dp.start_polling(bot)
    finally:
        await container.aclose()


async def tgclient_main() -> None:
    container = init_container()

    level = logging.INFO
    if container.config.tg_bot.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level, stream=sys.stdout, format=FORMAT)
    client = get_client(container.config.tg_client)
    frombot.include_events_handlers(client, container)

    async with client:
        await client.get_dialogs()  # for cache
        me = cast(User, await client.get_me())
        logger.info(
            f"client is starting! name={me.first_name} username={me.username}"
        )
        await cast(Awaitable[None], client.run_until_disconnected())

    await container.aclose()


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
        run_shell(["python", "loader/auth.py"], check=True)

    if args.run == "all":
        _ = run_tgclient_process()
        asyncio.run(tgbot_main())
    elif args.run == "bot":
        asyncio.run(tgbot_main())
    elif args.run == "client":
        asyncio.run(tgclient_main())


if __name__ == "__main__":
    cli()
