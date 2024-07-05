from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import TYPE_CHECKING, NamedTuple, cast

from aiogram.types.input_file import InputFile, URLInputFile
from pytube import YouTube
from pytube.streams import Stream

from .protocols import YouTubeProto

if TYPE_CHECKING:
    from aiogram.client.bot import Bot


@dataclass(slots=True)
class YouTubeAdapter(YouTubeProto):
    def __init__(
        self, url: str, auth: bool = False, cache_auth: bool = False
    ) -> None:
        yt = YouTube(url, use_oauth=auth, allow_oauth_cache=cache_auth)
        yt.bypass_age_gate()
        self.url = url
        self.audio = cast(Stream, yt.streams.get_audio_only())
        self.name = yt.title
        self.thumb_url = yt.thumbnail_url
        self.author = yt.author
        self.file_size = self.audio.filesize_mb


class YouTubeInputFile(InputFile):  # type: ignore
    def __init__(
        self,
        yt: YouTubeProto,
        filename: str | None = None,
        chunk_size: int = 9437184,  # 9mb.
    ) -> None:
        super().__init__(filename, chunk_size)
        self.yt = yt

    async def read(self, bot: "Bot") -> AsyncGenerator[bytes, None]:
        chunk_size = None if self.chunk_size == 9437184 else self.chunk_size
        audio = self.yt.audio.get_chunks(chunk_size)
        for chunk in audio:
            yield chunk


class FileDto(NamedTuple):
    file: YouTubeInputFile | str
    caption: str | None = None
    thumbnail: URLInputFile | None = None


def get_file(url: str) -> FileDto:
    yt = YouTubeAdapter(url, auth=True, cache_auth=True)
    file = YouTubeInputFile(yt, yt.name)
    thumb = URLInputFile(yt.thumb_url)

    return FileDto(file=file, thumbnail=thumb)
