import logging
import time
from functools import partial
from typing import TYPE_CHECKING, cast

from telethon import TelegramClient
from telethon.events import NewMessage

from loader.domain.schemes import YouTubeDTO
from loader.domain.services.youtube import process_get_needed_data

if TYPE_CHECKING:
    from loader.main.config import TelegramIds

logger = logging.getLogger(__name__)


async def send_file_bot(event: NewMessage.Event, tg_ids: "TelegramIds") -> None:
    logger.info("starting to do send_file_bot")

    txt = event.raw_text
    client = cast(TelegramClient, event.client)
    yt_dto = YouTubeDTO.to_dict(txt.replace("youtube", "", 1))
    try:
        start = time.time()
        (ytube, audio, audioattr, thumb) = await process_get_needed_data(
            yt_dto.link
        )
        file = await client.upload_file(
            audio, file_size=ytube.file_size, part_size_kb=512
        )
        await client.send_file(
            tg_ids.bot_id,
            file,
            attributes=[audioattr],
            caption=txt,
            thumb=thumb,
        )
        logger.info(f"audio downloaded for {time.time() - start:.3f} seconds")
    except Exception as e:
        logger.error(e)
        yt_dto.status = "bad"
        yt_dto.error_info = str(e)
        await client.send_message(tg_ids.bot_id, "errors" + yt_dto.to_json())


async def proxy_for_success_files(
    event: NewMessage.Event, tg_ids: "TelegramIds"
) -> None:
    logger.info("starting to do proxy_for_success_files")

    client = cast(TelegramClient, event.client)
    await client.send_message(tg_ids.bot_id, event.raw_text)


def include_events_handlers(
    client: TelegramClient, tg_ids: "TelegramIds"
) -> None:
    client.add_event_handler(
        partial(send_file_bot, tg_ids=tg_ids),
        NewMessage(chats=[tg_ids.bot_id], incoming=True, pattern=r"^youtube."),
    )
    client.add_event_handler(
        partial(proxy_for_success_files, tg_ids=tg_ids),
        NewMessage(
            chats=[tg_ids.bot_id], incoming=True, pattern=r"^final_common_file."
        ),
    )
