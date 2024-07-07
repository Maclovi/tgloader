import logging
from typing import cast

from aiogram import Bot, F, Router
from aiogram.types import Message

from loader.domain.schemes import YouTubeDto
from loader.tgbot.filters.user import IsClient

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(IsClient())


@router.message(F.text.startswith("youtube"))
async def send_youtube_audio(message: Message) -> None:
    logger.info("I'm starting to do send_youtube_audio")

    raw_json = cast(str, message.text).replace("youtube", "", 1)
    bot = cast(Bot, message.bot)
    yd = YouTubeDto.from_json(raw_json)
    await bot.send_message(yd.user_id, raw_json, disable_web_page_preview=True)
