from typing import BinaryIO, cast

import aiohttp
from telethon.tl.types import DocumentAttributeAudio

from loader.adapters.input_file import YouTubeInputFileBase
from loader.adapters.youtube import YouTubeAdapter


async def process_get_needed_data(
    link: str,
) -> tuple[YouTubeAdapter, BinaryIO, DocumentAttributeAudio, bytes]:
    ytube = YouTubeAdapter(link)
    audio = cast(
        BinaryIO,
        YouTubeInputFileBase(ytube.audio, name="n.mp3", chunk_size=524288),
    )
    audioattr = DocumentAttributeAudio(
        duration=ytube.duration,
        title=ytube.name,
        performer=ytube.author,
    )
    async with aiohttp.ClientSession() as session:
        resp = await session.get(ytube.thumb_url)
        thumb = await resp.read()

    return ytube, audio, audioattr, thumb
