from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import TYPE_CHECKING, BinaryIO, cast
from urllib.parse import urlparse

import aiohttp
from aiogram.types import Message
from aiogram.types.input_file import InputFile
from pytube import YouTube
from pytube.streams import Stream
from telethon.tl.types import DocumentAttributeAudio

from ..schemes import YouTubeDTO
from .protocols import StreamProto, YouTubeProto

if TYPE_CHECKING:
    from aiogram.client.bot import Bot


@dataclass(slots=True)
class YouTubeAdapter(YouTubeProto):
    def __init__(
        self, url: str, auth: bool = True, cache_auth: bool = True
    ) -> None:
        yt = YouTube(url, use_oauth=auth, allow_oauth_cache=cache_auth)
        yt.bypass_age_gate()
        self.url = url
        self.audio = cast(Stream, yt.streams.get_audio_only())
        self.name = yt.title
        self.thumb_url = yt.thumbnail_url
        self.author = yt.author
        self.file_size = self.audio.filesize
        self.video_id = urlparse(url).query.split("=", 1)[-1]
        self.duration: int = yt.length


class YouTubeInputFileBase:
    def __init__(
        self,
        audio: StreamProto,
        *,
        name: str | None = None,
        chunk_size: int = 9437184,  # 9mb.
    ) -> None:
        self.name = name
        self.chunk_size = chunk_size
        self.audio = audio.get_chunks(chunk_size)

    async def read(self, _: int) -> bytes:
        for chunk in self.audio:
            return chunk
        return b""


class YouTubeInputFile(InputFile):  # type: ignore
    def __init__(
        self,
        yt: YouTubeProto,
        filename: str | None = None,
        chunk_size: int = 9437184,  # 9mb.
    ) -> None:
        super().__init__(filename, chunk_size)
        self.audio = yt.audio.get_chunks(chunk_size)

    async def read(self, bot: "Bot") -> AsyncGenerator[bytes, None]:
        for chunk in self.audio:
            yield chunk


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
