import logging
import time
from functools import partial
from typing import TYPE_CHECKING, cast

from telethon import TelegramClient
from telethon.events import NewMessage

from loader.application.youtube import process_get_needed_data
from loader.domain.schemes import YouTubeDTO

if TYPE_CHECKING:
    from loader.ioc import Container

logger = logging.getLogger(__name__)


async def send_file_bot(event: NewMessage.Event, ioc: "Container") -> None:
    logger.info("starting to do send_file_bot")

    client = cast(TelegramClient, event.client)
    yt_dto = YouTubeDTO.to_dict(event.raw_text.replace("youtube", "", 1))
    bot_id = ioc.config.tg_ids.bot_id

    try:
        start = time.time()
        datas = await process_get_needed_data(yt_dto.link)
        yt_dto.message_for_answer += f" | views: {datas.ytube.views:,}"
        file = await client.upload_file(
            datas.audio, file_size=datas.ytube.file_size, part_size_kb=512
        )
        await client.send_file(
            bot_id,
            file,
            attributes=[datas.audioattr],
            caption="youtube" + yt_dto.to_json(),
            thumb=datas.thumb,
            allow_cache=False,
        )
        logger.info(f"audio downloaded for {time.time() - start:.3f} seconds")
    except Exception as e:
        logger.error(e, stack_info=True)
        yt_dto.error_info = str(e)
        await client.send_message(bot_id, "errors" + yt_dto.to_json())


async def proxy_for_success_files(
    event: NewMessage.Event, ioc: "Container"
) -> None:
    logger.info("starting to do proxy_for_success_files")

    bot_id = ioc.config.tg_ids.bot_id
    client = cast(TelegramClient, event.client)
    await client.send_message(bot_id, event.raw_text)


def include_events_handlers(client: TelegramClient, ioc: "Container") -> None:
    client.add_event_handler(
        partial(send_file_bot, ioc=ioc),
        NewMessage(
            chats=[ioc.config.tg_ids.bot_id],
            incoming=True,
            pattern=r"^youtube.",
        ),
    )
    client.add_event_handler(
        partial(proxy_for_success_files, ioc=ioc),
        NewMessage(
            chats=[ioc.config.tg_ids.bot_id],
            incoming=True,
            pattern=r"^final_common_file.",
        ),
    )
