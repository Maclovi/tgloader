import logging
from functools import partial
from typing import TYPE_CHECKING, cast

from telethon import TelegramClient
from telethon.events import NewMessage

from loader.application import FileDatabase, UserFileDatabase
from loader.application.youtube import process_get_needed_data
from loader.domain.common import timer
from loader.domain.schemes import YouTubeDTO

if TYPE_CHECKING:
    from loader.ioc import Container

logger = logging.getLogger(__name__)


async def send_file_bot(event: NewMessage.Event, ioc: "Container") -> None:
    logger.info("starting to do send_file_bot")

    client = cast(TelegramClient, event.client)
    yt_dto = YouTubeDTO.to_dict(event.raw_text.replace("youtube", "", 1))
    bot_id = ioc.config.tg_ids.bot_id

    async with ioc.new_session() as database:
        file = await FileDatabase(database).get_file_by_videoid(yt_dto.video_id)
        if file:
            yt_dto.file_id = file.file_id
            yt_dto.file_msg_id = file.message_id
            await client.send_message(
                bot_id, "final_common_file" + yt_dto.to_json()
            )
            return

    try:
        async with timer(logger):
            datas = await process_get_needed_data(yt_dto.link)
            yt_dto.message_for_answer += f" | views: {datas.ytube.views:,}"

            file = await client.upload_file(
                datas.audio, file_size=datas.ytube.file_size, part_size_kb=512
            )
            await client.send_file(
                bot_id,
                file,
                attributes=[datas.audioattr],
                caption="prepare_cache" + yt_dto.to_json(),
                thumb=datas.thumb,
                allow_cache=False,
            )
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


async def save_youtube(event: NewMessage.Event, ioc: "Container") -> None:
    dto = YouTubeDTO.to_dict(event.raw_text.replace("save_youtube", "", 1))

    if dto.file_msg_id is None:
        raise AttributeError("Audio_id is None, should be integer.")

    async with ioc.new_session() as database:
        await FileDatabase(database).create_file(
            videoid=dto.video_id, fileid=dto.file_id, msgid=dto.file_msg_id
        )
        await UserFileDatabase(database).create_userfile(
            dto.customer_user_id, dto.video_id
        )


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
    client.add_event_handler(
        partial(save_youtube, ioc=ioc),
        NewMessage(
            chats=[ioc.config.tg_ids.bot_id],
            incoming=True,
            pattern=r"^save_youtube.",
        ),
    )
