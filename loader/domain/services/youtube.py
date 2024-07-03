from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, cast

from aiogram.types.input_file import DEFAULT_CHUNK_SIZE, InputFile
from pytube import YouTube
from pytube.streams import ImproveStream

if TYPE_CHECKING:
    from aiogram.client.bot import Bot


class YouTubeAdapter:
    def __init__(
        self, url: str, auth: bool = False, cache: bool = False
    ) -> None:
        self.url = url
        self.yt = YouTube(url, use_oauth=auth, allow_oauth_cache=cache)
        self.yt.bypass_age_gate()
        self.audio = cast(ImproveStream, self.yt.streams.get_audio_only())


class YouTubeFile(InputFile):  # type: ignore
    def __init__(
        self,
        url: str,
        filename: str | None = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ):
        super().__init__(filename, chunk_size)
        self.yt = YouTubeAdapter(url, auth=True, cache=True)

    async def read(self, bot: "Bot") -> AsyncGenerator[bytes, None]:
        data = self.yt.audio.get_chunks()
        for chunk in data:
            yield chunk
