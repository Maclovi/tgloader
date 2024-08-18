import logging
from typing import TYPE_CHECKING, cast

from aiogram import Bot, F, Router
from aiogram.types import Audio, Message, User

from loader.domain.enums import Queue
from loader.domain.schemes import BaseDTO, YouTubeDTO
from loader.tgbot.filters.user import IsClient

if TYPE_CHECKING:
    from loader.ioc import Container

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(IsClient())


@router.message(F.caption.startswith(Queue.YOUTUBE_CACHE.value))
async def pre_cache_youtube(message: Message, ioc: "Container") -> None:
    logger.info(f"starting to do {pre_cache_youtube.__name__}")

    tg_ids = ioc.config.tg_ids
    bot = cast(Bot, message.bot)
    user = cast(User, message.from_user)
    audio = cast(Audio, message.audio)
    yt_dto = YouTubeDTO.to_class(cast(str, message.caption))
    yt_dto.file_id = audio.file_id
    bot_me = await bot.me()

    msg = await bot.send_audio(
        tg_ids.group_cache_id,
        audio.file_id,
        caption=f"{yt_dto.message_for_answer}\n@{bot_me.username}",
        parse_mode="HTML",
    )
    yt_dto.file_msg_id = msg.message_id

    await bot.send_message(
        user.id,
        f"client_proxy:{Queue.FINAL_COMMON_MEDIA.value}{yt_dto.to_json()}",
        disable_web_page_preview=True,
    )


@router.message(F.text.startswith(Queue.FINAL_COMMON_MEDIA.value))
async def send_file_customer(message: Message, ioc: "Container") -> None:
    logger.info("starting to do send_file_customer")

    dto = YouTubeDTO.to_class(cast(str, message.text))
    bot = cast(Bot, message.bot)
    tg_ids = ioc.config.tg_ids

    if dto.file_msg_id is None:
        raise AttributeError("Audio_id is None, should be integer.")

    await bot.forward_message(
        dto.customer_user_id, tg_ids.group_cache_id, dto.file_msg_id
    )

    for message_id in dto.messages_cleanup:
        await bot.delete_message(dto.customer_user_id, message_id)

    await message.answer(f"{Queue.SAVE_YOUTUBE.value}{dto.to_json()}")


@router.message(F.text.startswith(Queue.ERRORS.value))
async def send_errors(message: Message, ioc: "Container") -> None:
    logger.info("starting to do send_errors")

    tg_ids = ioc.config.tg_ids
    bot = cast(Bot, message.bot)
    txt = cast(str, message.text)
    dto = BaseDTO.to_class(txt)
    bot_message_id = dto.messages_cleanup[-1]
    msg_for_user = "something went wrong, sorry, try later"
    msg_for_errgroup = f"error: {dto.error_info!r}\n\n{txt}"

    await bot.edit_message_text(
        msg_for_user, chat_id=dto.customer_user_id, message_id=bot_message_id
    )
    await bot.send_message(
        tg_ids.group_error_id, msg_for_errgroup, disable_web_page_preview=True
    )


@router.message(F.text.startswith("bot_proxy:"))
async def bot_proxy(message: Message) -> None:
    if message.text is None:
        raise AttributeError("message.text should be string")

    await message.answer(message.text.replace("bot_proxy:", "", 1))
