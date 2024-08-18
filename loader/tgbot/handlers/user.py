import logging
from typing import TYPE_CHECKING, cast

from aiogram import Bot, F, Router
from aiogram.types import ChatMemberUpdated, Message, User

from loader.application import UserDatabase
from loader.domain.enums import Queue
from loader.domain.models import User as UserDomain
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
    d_user = UserDomain(
        id=tg_user.id,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
        username=tg_user.username,
        status="active",
    )
    async with ioc.new_session() as database:
        await UserDatabase(database).create_user(d_user)

    await message.answer(f"Hello, {tg_user.first_name}!\nSend me youtube url")


@router.message(RegexFullMatch("Помощь🚒"))
async def send_info(message: Message) -> None:
    logger.info("starting to do send_info")

    await message.answer("helping")


@router.message(RegexSearch(r"youtu(\.be|be\.com)"), flags={"media": "youtube"})
async def send_youtube_link(message: Message, ioc: "Container") -> None:
    logger.info("starting to do send_youtube_link")

    tg_ids = ioc.config.tg_ids
    bot_msg_id = (await message.answer("I got it! downloading...")).message_id
    user = cast(User, message.from_user)
    bot = cast(Bot, message.bot)
    link = cast(str, message.text)

    youtube_transfer_data = YouTubeDTO(
        customer_user_id=user.id,
        link=link,
        messages_cleanup=[message.message_id, bot_msg_id],
    )

    await bot.send_message(
        tg_ids.client_id,
        f"{Queue.PRE_YOUTUBE.value}{youtube_transfer_data.to_json()}",
        disable_web_page_preview=True,
    )


@router.my_chat_member(IF_KICKED)
async def user_blocked(event: ChatMemberUpdated, ioc: "Container") -> None:
    logger.info("starting to do process_user_blocked_bot")

    tg_user = event.from_user
    domain_user = UserDomain(
        id=tg_user.id,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
        username=tg_user.username,
        status="active",
    )

    async with ioc.new_session() as database:
        await UserDatabase(database).update_user(domain_user)


@router.message()
async def send_echo(message: Message) -> None:
    logger.info("starting to do send_echo")

    await message.answer("Мне не удалось вас понять :(")
