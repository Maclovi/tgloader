import logging
from typing import cast

from aiogram import Bot, F, Router
from aiogram.types import Audio, Message

from loader.domain.schemes import YouTubeDTO
from loader.tgbot.filters.user import IsClient

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(IsClient())


@router.message(F.caption.startswith("youtube"))
async def save_file_id(message: Message) -> None:
    logger.info("starting to do send_youtube_audio")

    audio = cast(Audio, message.audio)
    file_id = audio.file_id

    bot = cast(Bot, message.bot)
    caption = cast(str, message.caption)
    raw_json = caption.replace("youtube", "", 1)

    yt_dto = YouTubeDTO.to_dict(raw_json)
    customer_chat_id = yt_dto.customer_user_id

    await bot.send_audio(
        customer_chat_id, file_id, caption=yt_dto.link_html, parse_mode="HTML"
    )
    for message_id in yt_dto.message_ids:
        await bot.delete_message(customer_chat_id, message_id)


@router.message(F.text.startswith("yterror"))
async def send_errors(message: Message) -> None:
    logger.info("starting to do send_errors")

    bot = cast(Bot, message.bot)
    txt = cast(str, message.text)
    ytube_dto = YouTubeDTO.to_dict(txt.replace("yterror", "", 1))
    bot_answer_id = ytube_dto.message_ids[-1]

    await bot.send_message(ytube_dto.customer_user_id, ytube_dto.error_info)
    await bot.delete_message(ytube_dto.customer_user_id, bot_answer_id)
