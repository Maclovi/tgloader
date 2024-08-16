import logging
from typing import TYPE_CHECKING, cast

from aiogram import Bot, F, Router
from aiogram.types import Audio, Message, User

from loader.domain.schemes import BaseDTO, YouTubeDTO
from loader.tgbot.filters.user import IsClient

if TYPE_CHECKING:
    from loader.ioc import Container

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(IsClient())


@router.message(F.caption.startswith("prepare_cache"))
async def send_file_id_client(message: Message, ioc: "Container") -> None:
    logger.info("starting to do send_file_id_client")

    tg_ids = ioc.config.tg_ids
    bot = cast(Bot, message.bot)
    user = cast(User, message.from_user)
    audio = cast(Audio, message.audio)
    caption = cast(str, message.caption)
    yt_dto = YouTubeDTO.to_dict(caption.replace("prepare_cache", "", 1))
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
        "client_proxy:final_common_file" + yt_dto.to_json(),
        disable_web_page_preview=True,
    )


@router.message(F.text.startswith("final_common_file"))
async def send_file_customer(message: Message, ioc: "Container") -> None:
    logger.info("starting to do send_file_customer")

    json_raw = cast(str, message.text).replace("final_common_file", "", 1)
    dto = YouTubeDTO.to_dict(json_raw)
    bot = cast(Bot, message.bot)
    tg_ids = ioc.config.tg_ids

    if dto.file_msg_id is None:
        raise AttributeError("Audio_id is None, should be integer.")

    await bot.forward_message(
        dto.customer_user_id, tg_ids.group_cache_id, dto.file_msg_id
    )

    for message_id in dto.messages_cleanup:
        await bot.delete_message(dto.customer_user_id, message_id)

    await message.answer("save_youtube" + dto.to_json())


@router.message(F.text.startswith("errors"))
async def send_errors(message: Message, ioc: "Container") -> None:
    logger.info("starting to do send_errors")

    tg_ids = ioc.config.tg_ids
    bot = cast(Bot, message.bot)
    txt = cast(str, message.text)

    dto = BaseDTO.to_dict(txt.replace("errors", "", 1))
    bot_message_id = dto.messages_cleanup[-1]
    message_for_user = "something went wrong, sorry, try later"
    message_for_group = f"error: {dto.error_info!r}\n\n{txt}"

    await bot.edit_message_text(
        message_for_user,
        chat_id=dto.customer_user_id,
        message_id=bot_message_id,
    )
    await bot.send_message(
        tg_ids.group_error_id, message_for_group, disable_web_page_preview=True
    )


@router.message(F.text.startswith("bot_proxy:"))
async def bot_proxy(message: Message) -> None:
    if message.text is None:
        raise AttributeError("message.text should be string")
    await message.answer(message.text.replace("bot_proxy:", "", 1))
