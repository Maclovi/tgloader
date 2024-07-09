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
async def send_youtube_audio(message: Message) -> None:
    logger.info("starting to do send_youtube_audio")

    audio = cast(Audio, message.audio)
    file_id = audio.file_id
    bot = cast(Bot, message.bot)
    caption = cast(str, message.caption)
    raw_json = caption.replace("youtube", "", 1)

    youtube_dto = YouTubeDTO.to_dict(raw_json)

    customer_id = youtube_dto.customer_user_id
    link_html = f"<a href={youtube_dto.link!r}>link</a>"

    await bot.send_audio(customer_id, file_id, caption=link_html)
    await bot.delete_message(customer_id, youtube_dto.message_id)


@router.message(F.text.startswith("yterror"))
async def send_errors(message: Message) -> None:
    logger.info("starting to do send_errors")

    bot = cast(Bot, message.bot)
    txt = cast(str, message.text)
    yt_dto = YouTubeDTO.to_dict(txt.replace("yterror", "", 1))

    await bot.send_message(yt_dto.customer_user_id, yt_dto.error_info)
