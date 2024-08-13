import logging
from typing import TYPE_CHECKING, cast

from aiogram import Bot, F, Router
from aiogram.types import ChatMemberUpdated, Message, User

from loader.application import UserDatabase
from loader.domain.models import User as DBUser
from loader.domain.schemes import YouTubeDTO

from ..filters.user import (
    IF_KICKED,
    CommandStart,
    RegexFullMatch,
    RegexSearch,
)

if TYPE_CHECKING:
    from loader.ioc import Container

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")


@router.message(CommandStart())
async def proccess_cmd_start(message: Message, ioc: "Container") -> None:
    logger.info("starting to do proccess_cmd_start")

    tg_user = cast(User, message.from_user)
    domain_user = DBUser(
        id=tg_user.id,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
        username=tg_user.username,
        status="active",
    )
    async with ioc.new_session() as database:
        await UserDatabase(database).create_user(domain_user)

    await message.answer("Hello")


@router.message(RegexFullMatch("Помощь🚒"))
async def send_info(message: Message) -> None:
    logger.info("starting to do send_info")

    await message.answer("helping")


@router.message(RegexFullMatch("Легально?⚠"))
async def send_about_legal(message: Message) -> None:
    logger.info("starting to do send_about_legal")

    await message.answer("legal")


@router.message(RegexFullMatch("Свой бот🤖"))
async def send_info_own(message: Message) -> None:
    logger.info("starting to do send_info_own")

    await message.answer("own")


@router.message(RegexSearch(r"youtu(\.be|be\.com)"))
async def send_youtube_link(message: Message, ioc: "Container") -> None:
    logger.info("starting to do send_youtube_link")

    tg_ids = ioc.config.tg_ids
    bot_msg_id = (await message.answer("I got it! downloading...")).message_id

    user = cast(User, message.from_user)
    bot = cast(Bot, message.bot)
    link = cast(str, message.text)

    json_serialized = YouTubeDTO(
        customer_user_id=cast(int, user.id),
        link=link,
        message_ids=[message.message_id, bot_msg_id],
    )

    await bot.send_message(
        tg_ids.client_id,
        f"youtube{json_serialized.to_json()}",
        disable_web_page_preview=True,
    )


@router.my_chat_member(IF_KICKED)
async def user_blocked(event: ChatMemberUpdated, ioc: "Container") -> None:
    logger.info("starting to do process_user_blocked_bot")

    user_id = event.from_user.id
    async with ioc.new_session() as database:
        await UserDatabase(database).update_status(user_id, "inactive")


@router.message()
async def send_echo(message: Message) -> None:
    logger.info("starting to do send_echo")

    await message.answer("Мне не удалось вас понять :(")
