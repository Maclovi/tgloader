import logging
import time
from functools import partial
from typing import TYPE_CHECKING, cast

from telethon import TelegramClient
from telethon.events import NewMessage

from loader.domain.schemes import YouTubeDTO
from loader.domain.services.youtube import process_get_needed_data

if TYPE_CHECKING:
    from loader.config import TelegramIds

logger = logging.getLogger(__name__)


async def send_file_bot(event: NewMessage.Event, ids: "TelegramIds") -> None:
    logger.info("starting to do send_file_bot")

    client = cast(TelegramClient, event.client)
    yt_dto = YouTubeDTO.to_dict(event.raw_text.replace("youtube", "", 1))

    try:
        start = time.time()
        datas = await process_get_needed_data(yt_dto.link)
        yt_dto.message_for_answer += f" | views: {datas.ytube.views:,}"
        file = await client.upload_file(
            datas.audio, file_size=datas.ytube.file_size, part_size_kb=512
        )
        await client.send_file(
            ids.bot_id,
            file,
            attributes=[datas.audioattr],
            caption="youtube" + yt_dto.to_json(),
            thumb=datas.thumb,
            allow_cache=False,
        )
        logger.info(f"audio downloaded for {time.time() - start:.3f} seconds")
    except Exception as e:
        logger.error(e)
        yt_dto.status = "bad"
        yt_dto.error_info = str(e)
        await client.send_message(ids.bot_id, "errors" + yt_dto.to_json())


async def proxy_for_success_files(
    event: NewMessage.Event, ids: "TelegramIds"
) -> None:
    logger.info("starting to do proxy_for_success_files")

    client = cast(TelegramClient, event.client)
    await client.send_message(ids.bot_id, event.raw_text)


def include_events_handlers(
    client: TelegramClient, tg_ids: "TelegramIds"
) -> None:
    client.add_event_handler(
        partial(send_file_bot, ids=tg_ids),
        NewMessage(chats=[tg_ids.bot_id], incoming=True, pattern=r"^youtube."),
    )
    client.add_event_handler(
        partial(proxy_for_success_files, ids=tg_ids),
        NewMessage(
            chats=[tg_ids.bot_id], incoming=True, pattern=r"^final_common_file."
        ),
    )
