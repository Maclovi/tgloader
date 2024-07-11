from logging import getLogger
from typing import BinaryIO, NamedTuple, cast

import aiohttp
from telethon.tl.types import DocumentAttributeAudio

from loader.adapters.input_file import InputAudioTube
from loader.adapters.youtube import YouTubeAdapter

logger = getLogger(__name__)


class ComplectedDataForTelethon(NamedTuple):
    ytube: YouTubeAdapter
    audio: BinaryIO
    audioattr: DocumentAttributeAudio
    thumb: bytes


async def get_bytes_photo(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        thumb = await resp.read()
    return cast(bytes, thumb)


async def process_get_needed_data(link: str) -> ComplectedDataForTelethon:
    ytube = YouTubeAdapter(link)
    audio = cast(
        BinaryIO, InputAudioTube(ytube.audio, name="n.mp3", chunk_size=524288)
    )
    audioattr = DocumentAttributeAudio(
        duration=ytube.duration,
        title=ytube.name,
        performer=ytube.author,
    )
    thumb = await get_bytes_photo(ytube.thumb_url)

    return ComplectedDataForTelethon(ytube, audio, audioattr, thumb)
