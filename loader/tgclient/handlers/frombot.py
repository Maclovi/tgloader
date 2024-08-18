import logging
from asyncio import Semaphore
from functools import partial
from typing import TYPE_CHECKING, cast

from telethon.events import NewMessage

from loader.application import FileDatabase, UserFileDatabase
from loader.application.youtube import get_music_data
from loader.domain.common import extract_video_id, timer
from loader.domain.enums import Queue
from loader.domain.schemes import YouTubeDTO

if TYPE_CHECKING:
    from telethon import TelegramClient

    from loader.ioc import Container

logger = logging.getLogger(__name__)


async def handle_youtube_url(event: NewMessage.Event, ioc: "Container") -> None:
    logger.info("starting to do send_file_bot")

    bot_id = ioc.config.tg_ids.bot_id
    client = cast("TelegramClient", event.client)
    yt_dto = YouTubeDTO.to_class(event.raw_text)
    yt_dto.video_id = extract_video_id(yt_dto.link)

    async with ioc.new_session() as database:
        file = await FileDatabase(database).get_file_by_videoid(yt_dto.video_id)
        if file:
            yt_dto.file_id = file.file_id
            yt_dto.file_msg_id = file.message_id
            yt_dto.file_has_db = True
            queue = Queue.FINAL_COMMON_MEDIA.value
        else:
            queue = f"bot_proxy:{Queue.DOWNLOAD_YOUTUBE.value}"

    await client.send_message(bot_id, queue + yt_dto.to_json())


async def download_youtube(event: NewMessage.Event, ioc: "Container") -> None:
    async with Semaphore(5):
        client = cast("TelegramClient", event.client)
        yt_dto = YouTubeDTO.to_class(event.raw_text)
        bot_id = ioc.config.tg_ids.bot_id

        try:
            async with timer(logger):
                music = await get_music_data(yt_dto.link, ioc)
                yt_dto.message_for_answer += f" | views: {music.ytube.views:,}"

                file = await client.upload_file(
                    music.audio,
                    file_size=music.ytube.file_size,
                    part_size_kb=512,
                )
                await client.send_file(
                    bot_id,
                    file,
                    attributes=[music.audioattr],
                    caption=f"{Queue.YOUTUBE_CACHE.value}{yt_dto.to_json()}",
                    thumb=music.thumb,
                    allow_cache=False,
                )
        except Exception as e:
            logger.error(e, stack_info=True)
            yt_dto.error_info = str(e)
            await client.send_message(
                bot_id, f"{Queue.ERRORS.value}{yt_dto.to_json()}"
            )


async def client_proxy(event: NewMessage.Event, ioc: "Container") -> None:
    logger.info("starting to do proxy_for_success_files")

    bot_id = ioc.config.tg_ids.bot_id
    client = cast("TelegramClient", event.client)
    txt = event.raw_text.replace("client_proxy:", "", 1)

    await client.send_message(bot_id, txt)


async def save_youtube(event: NewMessage.Event, ioc: "Container") -> None:
    yt_dto = YouTubeDTO.to_class(event.raw_text)

    if yt_dto.file_msg_id is None:
        raise AttributeError("Audio_id is None, should be integer.")

    async with ioc.new_session() as database:
        if not yt_dto.file_has_db:
            await FileDatabase(database).create_file(
                videoid=yt_dto.video_id,
                fileid=yt_dto.file_id,
                msgid=yt_dto.file_msg_id,
            )
        await UserFileDatabase(database).create_userfile(
            yt_dto.customer_user_id, yt_dto.video_id
        )


def include_events_handlers(client: "TelegramClient", ioc: "Container") -> None:
    client.add_event_handler(
        partial(handle_youtube_url, ioc=ioc),
        NewMessage(
            chats=[ioc.config.tg_ids.bot_id],
            incoming=True,
            pattern=rf"^{Queue.PRE_YOUTUBE.value}.",
        ),
    )
    client.add_event_handler(
        partial(client_proxy, ioc=ioc),
        NewMessage(
            chats=[ioc.config.tg_ids.bot_id],
            incoming=True,
            pattern=r"^client_proxy:.",
        ),
    )
    client.add_event_handler(
        partial(save_youtube, ioc=ioc),
        NewMessage(
            chats=[ioc.config.tg_ids.bot_id],
            incoming=True,
            pattern=rf"^{Queue.SAVE_YOUTUBE.value}.",
        ),
    )
    client.add_event_handler(
        partial(download_youtube, ioc=ioc),
        NewMessage(
            chats=[ioc.config.tg_ids.bot_id],
            incoming=True,
            pattern=rf"^{Queue.DOWNLOAD_YOUTUBE.value}.",
        ),
    )
