import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from ..tgbot.handlers import user
from .config import Config, load_config

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    config: Config = load_config("bot.ini")

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    dp.include_router(user.router)

    await dp.start_polling(bot)


def cli() -> None:
    """Wrapper for command line"""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
