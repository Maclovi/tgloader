import logging
from typing import TYPE_CHECKING, cast

from aiogram import Bot, F, Router
from aiogram.types import Audio, Message

from loader.domain.schemes import BaseDTO, YouTubeDTO
from loader.tgbot.filters.user import IsClient

if TYPE_CHECKING:
    from loader.config import TelegramIds

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(IsClient())


@router.message(F.caption.startswith("youtube"))
async def send_file_id_client(message: Message, tg_ids: "TelegramIds") -> None:
    logger.info("starting to do send_file_id_client")

    bot = cast(Bot, message.bot)
    audio = cast(Audio, message.audio)
    caption = cast(str, message.caption)

    yt_dto = YouTubeDTO.to_dict(caption.replace("youtube", "", 1))
    yt_dto.file_id = audio.file_id

    await bot.send_message(
        tg_ids.client_id,
        "final_common_file" + yt_dto.to_json(),
        disable_web_page_preview=True,
    )


@router.message(F.text.startswith("final_common_file"))
async def send_file_customer(message: Message) -> None:
    logger.info("starting to do send_file_customer")

    txt = cast(str, message.text)
    bot = cast(Bot, message.bot)
    bot_me = await bot.me()
    bot_username = f"@{bot_me.username}"

    dto = BaseDTO.to_dict(txt.replace("final_common_file", "", 1))

    await bot.send_audio(
        dto.customer_user_id,
        dto.file_id,
        caption=f"{dto.message_for_answer}\n{bot_username}",
        parse_mode="HTML",
    )
    for message_id in dto.message_ids:
        await bot.delete_message(dto.customer_user_id, message_id)


@router.message(F.text.startswith("errors"))
async def send_errors(message: Message, tg_ids: "TelegramIds") -> None:
    logger.info("starting to do send_errors")

    bot = cast(Bot, message.bot)
    txt = cast(str, message.text)

    dto = BaseDTO.to_dict(txt.replace("errors", "", 1))
    bot_message_id = dto.message_ids[-1]
    message_for_user = "something went wrong, sorry, try later"
    message_for_group = f"error: {dto.error_info!r}\n\n{txt}"

    await bot.edit_message_text(
        message_for_user,
        chat_id=dto.customer_user_id,
        message_id=bot_message_id,
    )
    await bot.send_message(
        tg_ids.errors_id, message_for_group, disable_web_page_preview=True
    )
