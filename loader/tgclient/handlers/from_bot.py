import logging
from functools import partial
from typing import TYPE_CHECKING, cast

from telethon import TelegramClient, events

from loader.domain.schemes import YouTubeDTO
from loader.domain.services.youtube import process_get_needed_data

if TYPE_CHECKING:
    from loader.main.config import TelegramIds

logger = logging.Logger(__name__)


async def send_file_to_bot(
    event: events.NewMessage.Event, ids: "TelegramIds"
) -> None:
    logger.info("starting to do send_to_group")

    txt = event.raw_text
    client = cast(TelegramClient, event.client)
    yt_dto = YouTubeDTO.to_dict(txt.replace("youtube", "", 1))
    try:
        (ytube, audio, audioattr, thumb) = await process_get_needed_data(
            yt_dto.link
        )
        file = await client.upload_file(
            audio, file_size=ytube.file_size, part_size_kb=512
        )
        await client.send_file(
            ids.bot_id, file, attributes=[audioattr], caption=txt, thumb=thumb
        )
    except Exception as e:
        logger.error(e)
        yt_dto.status = "bad"
        await client.send_message(ids.bot_id, "yterror" + yt_dto.to_json())


def include_events_handlers(client: TelegramClient, ids: "TelegramIds") -> None:
    client.add_event_handler(
        partial(send_file_to_bot, ids=ids),
        events.NewMessage(
            chats=[ids.bot_id], incoming=True, pattern=r"youtube.+"
        ),
    )
