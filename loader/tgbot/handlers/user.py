import logging
from typing import cast

from aiogram import Bot, F, Router
from aiogram.types import ChatMemberUpdated, Message, User

from loader.domain.schemes import YouTubeDTO

from ..filters.user import (
    IF_KICKED,
    IF_MEMBER,
    CommandStart,
    RegexFullMatch,
    RegexSearch,
)

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")


@router.message(CommandStart())
async def proccess_cmd_start(message: Message) -> None:
    logger.info("starting to do proccess_cmd_start")

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


@router.message(RegexFullMatch("Предсказания🎱"))
async def send_prediction(message: Message) -> None:
    logger.info("starting to do send_prediction")

    await message.answer("guess")


@router.message(RegexFullMatch("Ответ на вопрос🎱"))
async def send_ball_response(message: Message) -> None:
    logger.info("starting to do send_ball_response")

    await message.answer("magic ball")


@router.message(RegexSearch(r"youtu(\.be|be\.com)"))
async def send_youtube_link(message: Message, client_id: int) -> None:
    logger.info("starting to do send_youtube_link")

    bot_answer = await message.answer("I got it! downloading...")
    bot_answer_id = bot_answer.message_id

    user = cast(User, message.from_user)
    user_id = cast(int, user.id)
    link = cast(str, message.text)
    bot = cast(Bot, message.bot)
    json_serialized = YouTubeDTO(
        customer_user_id=user_id,
        link=link,
        message_ids=[message.message_id, bot_answer_id],
    ).to_json()

    await bot.send_message(
        client_id, f"youtube{json_serialized}", disable_web_page_preview=True
    )


@router.my_chat_member(IF_KICKED)
async def process_user_blocked_bot(_: ChatMemberUpdated) -> None:
    logger.info("starting to do process_user_blocked_bot")


@router.my_chat_member(IF_MEMBER)
async def process_user_unblocked_bot(event: ChatMemberUpdated) -> None:
    logger.info("starting to do process_user_unblocked_bot")

    await event.answer("Zdarov")


@router.message()
async def send_echo(message: Message) -> None:
    logger.info("starting to do send_echo")

    await message.answer("Мне не удалось вас понять :(")
