import logging
from functools import partial
from typing import TYPE_CHECKING, cast

from telethon import TelegramClient, events

from loader.domain.schemes import YouTubeDto

if TYPE_CHECKING:
    from loader.main.config import TelegramIds

logger = logging.Logger(__name__)


async def send_to_group(
    event: events.NewMessage.Event,
    ids: "TelegramIds",
) -> None:
    logger.info("I'm starting to do send_to_group")

    # TODO: implementing loads youtube audio and send it

    json_raw = event.raw_text.replace("youtube", "", 1)
    yd = YouTubeDto.from_json(json_raw)
    client = cast(TelegramClient, event.client)

    await client.send_message(ids.group_id, event.raw_text)
    await client.send_message(ids.bot_id, event.raw_text)


def include_events_handlers(client: TelegramClient, ids: "TelegramIds") -> None:
    client.add_event_handler(
        partial(send_to_group, ids=ids),
        events.NewMessage(
            chats=[ids.bot_id], incoming=True, pattern=r"youtube.+"
        ),
    )
